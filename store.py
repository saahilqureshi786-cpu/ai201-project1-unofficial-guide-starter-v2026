"""
Stages 3 and 4 of the pipeline: embedding chunks and retrieving them.

Three things in here are worth knowing about, because they'd quietly break the
rest of the project if they were wrong:

1. The Chroma collection is created with cosine distance, explicitly. Chroma
   defaults to squared L2, and the 0.6 threshold the course uses is calibrated
   against cosine. Getting this wrong makes every distance number meaningless.

2. `search` returns the semantic distance alongside each chunk. The final
   ordering can use both semantic similarity and BM25 keyword matching, but
   the cosine distance is still preserved for the relevance gate.

3. The embedding model is the one Chroma bundles, not one loaded through
   `sentence-transformers`. It is the same model — `all-MiniLM-L6-v2`, 384
   dimensions — but it arrives as an ONNX build from Chroma's own CDN, so the
   install needs neither PyTorch nor a reachable Hugging Face. See `_embedder`.
"""

import os
import re
import shutil
from dataclasses import dataclass

# Must be set BEFORE chromadb is imported. Without it, some Chroma versions
# print "Failed to send telemetry event ..." on every single call.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb  # noqa: E402
from rank_bm25 import BM25Okapi

import config
from chunker import Chunk


@dataclass
class Result:
    """One retrieved chunk and how far it was from the question."""

    text: str
    source: str
    label: str
    distance: float  # LOWER IS BETTER. 0.3 is close, 0.9 is unrelated.
    produced_by: str


_model = None

# The model Chroma bundles. Anything else in config.EMBEDDING_MODEL means
# "fetch that one from Hugging Face instead" — see `_embedder`.
BUNDLED_MODEL = "all-MiniLM-L6-v2"


class _OnnxEmbedder:
    """
    Chroma's built-in embedder, wrapped to look like the other two.

    Chroma's embedding functions are called directly and hand back numpy
    arrays. The rest of this file wants `.encode(texts)`, so the adapter lives
    here rather than making every caller care which embedder it got.
    """

    def __init__(self):
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

        self._ef = ONNXMiniLM_L6_V2()

    def encode(self, texts, show_progress_bar: bool = False):
        return [vector.tolist() for vector in self._ef(list(texts))]


def _sentence_transformer(name: str):
    """
    The escape hatch: any model that isn't the bundled one.

    Unit 2's "try a second embedding model" stretch option comes through here,
    and so does anything you set `EMBEDDING_MODEL` to. This path *does* need
    `sentence-transformers` and a reachable Hugging Face, neither of which the
    default install has.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            f"config.EMBEDDING_MODEL is set to {name!r}, which isn't the model "
            f"Chroma bundles ({BUNDLED_MODEL!r}), so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'\n"
            f"Or set EMBEDDING_MODEL back to {BUNDLED_MODEL!r}."
        ) from exc

    return SentenceTransformer(name)


def _embedder():
    """
    Load the embedding model once and keep it.

    First call is slow — it downloads about 80 MB. That's why setup happens
    before class.
    """
    global _model

    if _model is not None:
        return _model

    # Used only by this repo's own smoke test.
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        from _smoke_embedder import FakeEmbedder

        _model = FakeEmbedder()
    elif config.EMBEDDING_MODEL == BUNDLED_MODEL:
        _model = _OnnxEmbedder()
    else:
        _model = _sentence_transformer(config.EMBEDDING_MODEL)

    return _model


def embed(texts: list[str]) -> list[list[float]]:
    """Turn text into vectors. Runs on your machine, costs no API quota."""
    vectors = _embedder().encode(texts, show_progress_bar=False)

    # sentence-transformers and the smoke stand-in return something with a
    # .tolist(); _OnnxEmbedder has already done that conversion itself.
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def _client():
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=chromadb.config.Settings(anonymized_telemetry=False),
    )


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Embed every chunk and store it.

    `variant` lets you keep more than one index of the same corpus at the same
    time. In unit 2, when you compare two chunking strategies, index the second
    one as variant="v2" and you can query both instead of deleting the first
    and starting over.
    """
    name = config.collection_name(corpus, variant)
    client = _client()

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        # Do not remove. Chroma defaults to squared L2, and every distance
        # number in this course assumes cosine.
        metadata={"hnsw:space": "cosine"},
    )

    batch = 256

    for start in range(0, len(chunks), batch):
        window = chunks[start : start + batch]

        collection.add(
            ids=[f"{c.source}#{c.index}" for c in window],
            documents=[c.text for c in window],
            embeddings=embed([c.text for c in window]),
            metadatas=[
                {
                    "source": c.source,
                    "index": c.index,
                    "produced_by": c.produced_by,
                }
                for c in window
            ],
        )

    return len(chunks)


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
) -> list[Result]:
    """
    Retrieve chunks using hybrid semantic + BM25 search.

    Semantic retrieval finds chunks that are close in meaning.
    BM25 rewards chunks that contain important exact words from the question.
    Reciprocal Rank Fusion combines both rankings.

    Each returned Result keeps its original semantic cosine distance so the
    existing relevance gate can still use the same 0.6 threshold.
    """
    top_k = top_k or config.TOP_K
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    count = collection.count()

    if count == 0:
        return []

    # Retrieve the whole corpus in semantic order so that both the semantic
    # rank and BM25 rank can be compared over the same set of chunks.
    raw = collection.query(
        query_embeddings=embed([question]),
        n_results=count,
    )

    ids = raw["ids"][0]
    documents = raw["documents"][0]
    metadatas = raw["metadatas"][0]
    distances = raw["distances"][0]

    # Semantic ranking: rank 1 is the most semantically similar document.
    semantic_rank = {
        doc_id: rank
        for rank, doc_id in enumerate(ids, start=1)
    }

    # Simple tokenizer for BM25 keyword matching.
    def tokenize(text: str) -> list[str]:
        return re.findall(r"[a-z0-9$]+", text.lower())

    tokenized_documents = [
        tokenize(document)
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)
    bm25_scores = bm25.get_scores(tokenize(question))

    # Highest BM25 score receives rank 1.
    bm25_order = sorted(
        range(len(ids)),
        key=lambda index: float(bm25_scores[index]),
        reverse=True,
    )

    bm25_rank = {
        ids[index]: rank
        for rank, index in enumerate(bm25_order, start=1)
    }

    # Build the Result objects while preserving each chunk's semantic distance.
    results_by_id: dict[str, Result] = {}

    for doc_id, text, meta, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        meta = meta or {}

        results_by_id[doc_id] = Result(
            text=text,
            source=str(meta.get("source", "unknown")),
            label=f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}",
            distance=float(distance),
            produced_by=str(meta.get("produced_by", "unknown")),
        )

    # Reciprocal Rank Fusion combines semantic and keyword rankings.
    #
    # A document receives credit for ranking highly in either system.
    # 60 is a common RRF constant and prevents one extremely high rank from
    # completely dominating the combined score.
    rrf_k = 60

    def hybrid_score(doc_id: str) -> float:
        semantic_part = 1 / (rrf_k + semantic_rank[doc_id])
        keyword_part = 1 / (rrf_k + bm25_rank[doc_id])

        return semantic_part + keyword_part

    ranked_ids = sorted(
        ids,
        key=hybrid_score,
        reverse=True,
    )

    return [
        results_by_id[doc_id]
        for doc_id in ranked_ids[:top_k]
    ]


def index_exists(
    corpus: str | None = None,
    variant: str = "default",
) -> bool:
    """
    Is there an index here to search, without searching it?

    `serve.py`'s health check asks this. It deliberately does not embed
    anything: loading the embedding model takes 80 MB and a few seconds.
    """
    try:
        collection = _client().get_collection(
            config.collection_name(corpus, variant)
        )
        return collection.count() > 0
    except Exception:
        return False


def reset():
    """Delete every index. Occasionally the fastest way out of a mess."""
    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)