# The Unofficial Guide

Saahil Qureshi — Corpus: `campus_life`

---

# Unit 1

## What This Does

This project builds a retrieval-augmented generation (RAG) question-answering
system using the `campus_life` corpus. The corpus contains short documents about
housing, parking, advising, dining, courses, and other campus topics. When a
user asks a question, the system retrieves the most relevant document chunks
and uses Gemini to generate an answer with a source. It also uses a relevance
gate to reject questions that are unrelated to the corpus.

## Chunking Strategy

**Chunk size:** One complete document per chunk. In the final index, chunks
ranged from 178 to 549 characters, with an average of about 317 characters.

**Overlap:** 0 characters.

The `campus_life` documents are already short and usually focus on one specific
topic. I initially experimented with a 500-character chunk size and an
80-character overlap. After inspecting sample chunks, I found that most of the
documents were already short enough to stand alone and contained enough context
to answer a question.

Because splitting these documents further could remove useful context, I changed
`split_documents()` so that each document remains intact as one chunk. The final
index contained 88 chunks from 88 documents.

## Sample Chunks

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```text
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```text
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```text
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```text
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```
## Sample Answer

**Question:**

Is the housing lottery random?

**Answer:**

```text
The housing lottery is not entirely random in the way most people assume.
Rising sophomores receive a randomly drawn number, but juniors and seniors
are ordered first by accumulated credit hours, with random tie-breaks used
only for ties.

Source: admin_housing_lottery.txt
```

**My relevance cutoff:** 0.6

I tested five questions that the corpus should answer and five questions that
are clearly outside the corpus. Lower distance values indicate closer semantic
matches.

The highest best-distance among the in-corpus questions was 0.3586. The lowest
best-distance among the out-of-scope questions was 0.8246. This left a large
gap between the two groups, so I kept the relevance cutoff at 0.6. Questions
with a best distance below 0.6 are allowed through the gate, while questions
above the cutoff are refused.

| Question | In corpus? | Best distance |
|---|---|---:|
| When do housing lottery numbers come out? | Yes | 0.3453 |
| How are juniors and seniors ordered in the housing lottery? | Yes | 0.2250 |
| How long does it usually take west lot parking permits to sell out? | Yes | 0.2264 |
| How far in advance should students book an adviser before registration? | Yes | 0.3586 |
| How much does laundry cost to wash a load at Morrow House? | Yes | 0.2041 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

## How I Used AI

**1.** I asked ChatGPT for help when my Gemini request repeatedly returned an
`API_KEY_INVALID` error. ChatGPT suggested checking whether Python was actually
reading `GEMINI_API_KEY` from the `.env` file. I ran a check and discovered that
the value being loaded was only 13 characters long because I had multiple
`.env` files and was editing the wrong one. I corrected the `.env` file inside
the project, verified that the full key loaded correctly, and reran the
application successfully.

**2.** I asked ChatGPT to help me think through the chunking strategy after I
printed and inspected five chunks. I first tried changing the configuration to
500-character chunks with an 80-character overlap. After reviewing the corpus,
I saw that the documents were already short and mostly self-contained. I
therefore changed the implementation so that `split_documents()` keeps each
document intact as one chunk, rather than splitting short documents
unnecessarily.

---

# Unit 2

## Run Log — Before

Baseline evidence: `results/run_2026-09-23_1937_before.md`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---:|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are understandable on their own | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected fact | 4/5 | 5/5 | 5/5 | 5/5 | MET |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 questions retrieved an answer-bearing document, exceeding the 4/5 target. |
| 2 | Every answer names a source | MET | All generated answers named at least one source document. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all 5 of 5 out-of-scope questions, exceeding the 4/5 target. |
| 4 | Sampled chunks are understandable on their own | MET | All 5 sampled chunks were complete enough to understand independently. |
| 5 | Answers contain the expected fact | MET | All 5 questions passed in all 3 runs. |

## Diagnoses

None of the five acceptance criteria were missed.

Because all five criteria were MET, I looked for a target that was too loose. Criterion 1 only required the answer-bearing chunk to appear somewhere in the retrieved results.

A tighter target would be:

> For at least 4 of 5 test questions, the top-ranked retrieved chunk contains the answer.

The baseline system met this tighter target for only 2 of 5 questions.

**Pipeline stage:** Retrieval

**Mechanism:** Semantic retrieval usually found the correct document, but similar campus documents sometimes ranked above the exact document containing the requested fact.

## The Improvement

**What I changed:**

I changed `store.py::search` from semantic-only retrieval to hybrid retrieval using:

1. Semantic vector ranking
2. BM25 keyword ranking
3. Reciprocal Rank Fusion to combine both rankings

**Why I picked it:**

The baseline system usually retrieved the correct document, but it was not always ranked first. I wanted to test whether adding keyword matching would improve ranking for exact terms such as parking lots, adviser registration, and Morrow House.

### Run Log — After

After evidence: `results/run_2026-09-23_2052_after.md`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---:|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are understandable on their own | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected fact | 4/5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

The hybrid retrieval change did not improve the tighter top-ranked retrieval target.

Before: correct answer-bearing document ranked first for 2/5 questions.

After: correct answer-bearing document ranked first for 2/5 questions.

All five original acceptance criteria still passed, and the relevance gate continued to refuse 5/5 out-of-scope questions.

### Real Output

Produced by `run_eval.py::main` using retrieval from `store.py::search`.

```text
When do housing lottery numbers come out?
run 1: pass
run 2: pass
run 3: pass

How are juniors and seniors ordered in the housing lottery?
run 1: pass
run 2: pass
run 3: pass

How long does it usually take west lot parking permits to sell out?
run 1: pass
run 2: pass
run 3: pass

How far in advance should students book an adviser before registration?
run 1: pass
run 2: pass
run 3: pass

How much does laundry cost to wash a load at Morrow House?
run 1: pass
run 2: pass
run 3: pass

gate refused 5 of 5

```

## Stretch Improvement — Declared Before Build

For my second measured improvement, I will test weighted Reciprocal Rank Fusion
instead of giving semantic retrieval and BM25 equal influence.

My hypothesis is that giving BM25 slightly more weight may improve the tighter
top-1 retrieval target because several questions contain exact entity terms such
as building names, parking lots, and administrative topics.

### Run Log — Weighted RRF

Evidence: `results/run_2026-10-04_2120_weighted_rrf.md`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---:|---:|---:|---:|---|
| 1. Retrieved chunks contain the answer | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are understandable on their own | 4/5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected fact | 4/5 | 5/5 | 5/5 | 5/5 | MET |

### Did the Second Improvement Help?

Yes.

I changed the hybrid Reciprocal Rank Fusion scoring so that the BM25 keyword
component receives 1.5 times the weight of the semantic component.

The original semantic + BM25 RRF system achieved the tighter top-1
answer-bearing retrieval target for only 2 of 5 questions.

After weighting BM25 more heavily, the top-ranked chunk contained the expected
answer for all 5 of 5 questions.

**Before:** 2/5 top-1 answer-bearing retrieval  
**After weighted RRF:** 5/5 top-1 answer-bearing retrieval

The original five acceptance criteria also remained MET, and the relevance gate
continued to refuse 5 of 5 out-of-scope questions.


## What's Still Broken

None of the original five acceptance criteria are currently broken.

The weighted RRF improvement also fixed the tighter retrieval-ranking weakness:

> For at least 4 of 5 test questions, the top-ranked retrieved chunk contains the answer.

The system now achieves 5/5 on this tighter target.

If I continued, I would test the weighted approach on a larger question set to
see whether the improvement generalizes beyond these five evaluation questions.

## What I'd Do Differently

If I started Unit 1 again, I would make Criterion 1 stricter from the beginning.

Instead of only checking whether the correct chunk appears somewhere in the
retrieved results, I would measure whether it ranks first.

I would also add top-1 retrieval accuracy directly to the evaluator so ranking
quality is measured automatically instead of being checked manually.

## How I Used AI — Unit 2

I used ChatGPT to help interpret the Unit 2 rubric, diagnose the
retrieval-ranking weakness, and implement the hybrid semantic + BM25 retrieval
experiment.

I verified the suggested changes myself by running the evaluations and comparing
the measured results. The first hybrid RRF experiment did not improve top-1
retrieval, so I reported that result. I then tested a second improvement by
giving BM25 1.5 times the weight of semantic retrieval. The measured top-1
answer-bearing retrieval improved from 2/5 to 5/5.