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

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. Chunks contain enough standalone context | 4 of 5 |  |  |  |  |
| 5. Answers contain the expected fact | 4 of 5 |  |  |  |  |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer |  |  |
| 2 | Every answer names a source |  |  |
| 3 | Gate stops out-of-corpus questions |  |  |
| 4 | Chunks contain enough standalone context |  |  |
| 5 | Answers contain the expected fact |  |  |

## Diagnoses

To be completed in Unit 2 after running the before evaluation and comparing the
results against the five acceptance criteria.

## The Improvement

**What I changed:**

To be completed in Unit 2 after diagnosing any criteria that were missed.

**Why I picked it:**

To be completed after identifying which pipeline stage caused the problem.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. Chunks contain enough standalone context | 4 of 5 |  |  |  |  |
| 5. Answers contain the expected fact | 4 of 5 |  |  |  |  |

**Did it help?**

To be completed in Unit 2 after running the after evaluation.

## What's Still Broken

To be completed in Unit 2 after comparing the before and after results.

## What I'd Do Differently

To be completed in Unit 2 after completing the evaluation and improvement cycle.

The final system uses document-level chunks and a 0.6 relevance cutoff selected from retrieval-distance testing.