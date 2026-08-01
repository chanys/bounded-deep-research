# bounded-deep-research

AnswerTrail is a bounded-corpus deep-research agent: a roll-your-own ReAct loop (search, reason, answer) over a fixed library of one YouTube creator's transcripts, live at `answertrail.yeesengchan.com`.
The full methodology, with pseudocode and every prompt, lives in the sibling `../bounded-deep-research-notes` repo (`eval/gold_construction_reference.md`, `eval/experiments_reference.md`); see `CLAUDE.md` for architecture and conventions.

## Overview

_Coming: a fuller description of the system and its ReAct agent loop (search, reason, answer over dense pgvector retrieval)._

## Building the evaluation gold

AnswerTrail is evaluated on two kinds of question:
- Factual questions: each asking for one specific fact
- Longitudinal questions: each asking how the creator's view on a topic changed over time.

To score either kind we build evaluation data. Each evaluation example consists of a question paired with a set of nuggets. Nuggets are the atomic facts that a correct answer must state:
- A factual nugget is a single fact
- A longitudinal nugget is a stance plus a time window.

This section describes how we produce (factual/longitudinal) questions and their associated nuggets. Briefly: nuggets are extracted from claims, and claims are extracted from chunks (30-second transcript slices).

### Vocabulary

- **chunk** - a fixed 30-second transcript window; the atomic unit that is searched and cited. Its id is `video_id:start_second`.
- **claim** - one atomic, faithful assertion a video makes, extracted from the transcript and tied to the chunk(s) that state it. Its id is `video_id#cNNN`.
- **topic / entity tags** - short labels attached to each claim by the extractor (e.g. topic "elevator puzzle benchmark", entity "GPT-5.4").
- **nugget** - one atomic fact a correct answer must state; the unit recall is scored against. A factual nugget is a fact; a longitudinal nugget is a stance plus a time window.

### The corpus

The corpus is an AI/LLM YouTube channel's transcripts. We gathered 475 videos from the most recent 16 months (excluding SHORTS) and divided each video's transcript text into 30-second chunks, obtaining a total of 25,401 chunks. A typical video contains around 52 chunks.

### From chunks to claims (shared by both tiers)

To derive the nuggets, we first extracted *claims* from *chunks*. For each video, we do the following:

- Load the video's chunks in start-time order and render them as a numbered list, one line per chunk (`index: text`).
- Call Sonnet 5 (thinking off) with the claim-extraction system prompt, asking for a list of claims where each generated claim cites the chunk indices that state it.

A single call produces for each claim: (1) the claim text, (2) its supporting chunk indices, and (3) its topic and entity tags.

A human review of a first extraction pass over 3 sample videos caught over-extraction of claims (production narration, blow-by-blow demo transcripts), driving one prompt revision that took those 3 videos from 210 claims to 145 before the full pass over all videos.

A snippet of the claim-extraction prompt ([`CLAIM_SYSTEM` in `eval/extract_claims.py`](https://github.com/chanys/bounded-deep-research/blob/main/eval/extract_claims.py#L61)):

```
Extract EVERY concrete claim, finding, number, result, comparison, or stated opinion...
For each claim, list in evidence_indices the indices of the chunk(s) that support it.
Never cite a chunk that does not state the claim.
```

A real extracted claim, showing the tags produced in the same call:

```
{ "claim_id": "-HjPWrKavyA#c016",
  "text":     "Claude 4.5 scored 77% on general finance in this study.",
  "chunk_ids":["-HjPWrKavyA:00390", "-HjPWrKavyA:00420"],
  "topics":   ["FIRE benchmark", "model comparison"],
  "entities": ["Claude 4.5"],
  "confidence":"high" }
```

The corpus yields 26,240 claims with a median of 54 per video.

### Factual gold: 25 questions, 53 nuggets

The factual tier asks for a single specific fact, so its gold is a small set of atomic facts (nuggets) per question, produced in four steps.

1. **Sample over time, not topic.** Order the 475 videos by date, divide them into 5 equal-count bins of about 95 videos each, and take a seeded draw of 10 videos from each, so the 50 source videos span the whole 16-month range rather than clustering on prolific months.

2. **Select and compose (two calls per video).** We aim to derive one factual question from each of the 50 videos. First, a cheap thinking-off Sonnet 5 call picks the video's 2 most question-worthy high-confidence claims, and the script keeps one as primary and one as fallback ([`SELECT_SYSTEM`](https://github.com/chanys/bounded-deep-research/blob/bfc57c2/eval/compose_factual_claims.py#L45)):

   ```
   Return the ids of the 2 claims a practitioner who never saw the video would most
   plausibly ask a substantive question about... Do not select claims with unresolved
   references ("the paper", "the study") that only sibling claims resolve.
   ```

   An adaptive-thinking call then writes one natural question from the primary claim ([`COMPOSE_SYSTEM`](https://github.com/chanys/bounded-deep-research/blob/bfc57c2/eval/compose_factual_claims.py#L48)):

   ```
   Anchor it: include at least one identifying specific from the claim (a named system,
   org, paper, benchmark, technique, or figure)... Never include the part of the claim
   the question ASKS FOR (the finding, verdict, reason, or outcome).
   ```

   The output is 50 question candidates, one per sampled video, each paired with its source claim.

3. **Human adjudication.** Not every one of the 50 composed factual questions is usable, so a human vets each one. After reviewing the questions, each with its associated claim and chunk(s), we kept 26 out of the 50 questions. The most common reasons for omitting questions include: the question already contained its answer, and unnatural questions no real user would type (e.g., *"In a paper's worked example on agent matchmaking with a pool of 100 agents, cosine similarity is used to match agent self-descriptions to subtasks - which agent was identified as the best fit for subtask one, and what was its similarity score?"*).

4. **Nugget extraction.** For each of the 26 factual questions, a Sonnet 5 call (adaptive) decomposes its claim into the atomic facts an answer must state, while omitting facts already stated in the question.

   A snippet of the [nugget-extraction prompt](https://github.com/chanys/bounded-deep-research/blob/main/eval/extract_factual_nuggets.py#L55) (`SYSTEM`):

   ```
   Decompose the claim into "nuggets": the atomic, independently-checkable facts that a
   correct answer must state...
   Subtract the question - entities AND predicates. A fact already given in the question
   earns nothing.
   ```

   An example of a question, with its associated claim and nuggets:

   ```
   question : Which universities published ReasonFlux, and when did the paper come out?
   claim    : The creator states that Princeton University and Peking University already
              implemented this exact approach, publishing it on February 10th, 2025,
              calling it ReasonFlux.
   nuggets  : fc-0001_n1  "ReasonFlux was published by Princeton University."
              fc-0001_n2  "ReasonFlux was published by Peking University."
              fc-0001_n3  "ReasonFlux was published on February 10th, 2025."
   ```

   The first automated run produced 69 nuggets across the 26 questions. Manual adjudication removed nuggets describing properties (e.g. "fast", "temporary") already stated in the question. In the end, we obtained 25 questions with 53 associated nuggets.

### Longitudinal gold: 35 questions

The longitudinal tier draws on the same claims but asks a harder question: not what one claim says, but how a view changed over time. That kind of change never shows up in a single claim, so the longitudinal gold is built from a topic's claims tracked over time. We produce it in four steps.

1. **Build threads.** A thread is formed by grouping high-confidence claims that share a normalized topic tag, keeping only groups spanning at least 3 videos and at least 90 days, ordered by date. Normalizing a tag is purely lexical: lowercase it, drop parenthetical asides, turn hyphens into spaces, and strip a trailing role word. For instance, "In-Context Learning" and "in context learning" both become `in context learning`, and "multi-agent systems" becomes `multi agent`. The intuition: three videos means the topic is not a one-off, ninety days means enough time to actually change. Claims from generic non-trajectory topics are dropped first by a stop-list:

   ```
   STOPPED:  "creator opinion", "creator assessment", "benchmarks", "benchmark results",
             "results", "model comparison", "model architecture", "reasoning",
             "training data", "methodology", "limitations", "publication date"
   ```

   A real thread (abbreviated) is shown below: the `reinforcement learning` thread, a family of 134 videos and 301 dated claims spanning 461 days:

   ```
   ### topic:reinforcement learning  [videos=134, span=461d, claims=301]  2025-01-10 -> 2026-04-16
     2025-01-10 [FR8oE8chp7c#c019] new data or RL approaches do not override the root-cause reasoning engine's outdated knowledge
     2025-01-29 [2ENvGkkK36E#c002] DeepSeek's R1 paper explains GRPO (Group Relative Policy Optimization) in detail
     2025-02-02 [bjktcqGxxac#c039] RL-tuned models like o1 and R1 are optimized for final-answer correctness, not reasoning
     2025-02-07 [tLnZBUuxNAI#c010] OpenAI's Deep Research uses end-to-end RL over web browsing and reasoning
     ... (+293 more claims)
   ```

2. **Compose a question from each thread.** Each thread then goes to one adaptive-thinking Sonnet 5 call. Its input is the thread of dated claims; its output is three things at once: a question, a `trajectory_must_say` of 2 to 4 arc statements describing how the view changed, and 3 to 6 of the thread's claims chosen as the dated evidence. The claims are not generated here: they are the thread's existing claims that the call selects as evidence; only the question and the trajectory are newly written. Before it composes any of that, the same call applies a development test: it must first decide whether the thread shows genuine development (a stance changing, results evolving, a position reversing) and reject threads that merely restate the same point.

   A snippet of the [composition prompt](https://github.com/chanys/bounded-deep-research/blob/main/eval/compose_longitudinal_claims.py#L63) (`SYSTEM`):

   ```
   First decide: does this thread show genuine DEVELOPMENT... REJECT threads that only
   show the same point restated over time.
   question: ONE natural question about the development... do NOT name the specific
   dimension or direction of the change.
   ```

   Of about 1,105 threads left after the stop-list, 505 pass this development test.

3. **Triage arcs versus collections.** Passing the development test is necessary but not sufficient: the 505 surviving threads are still not precise enough, because Sonnet 5 cannot reliably tell two things apart:
   - An **arc** is a genuine trajectory: the creator's own position, or his own test's results, moving directionally on one object over time.
   - A **collection** is separate points that merely share a topic word but do not move directionally, e.g. several facts about "RAG" across the year, with no single evolving position. It looks longitudinal but is really a list.

   A human reads all 505 (longitudinal question + trajectory/arc statements). After filtering for questions associated with genuine trajectory arcs, we are left with 35 questions.

4. **Extract nuggets from arcs.** We deliberately do not turn every fact in a thread into a nugget. Because the corpus is large, there are many plausible routes from a starting stance to an ending stance, so two correct answers can tell the same story through different intermediate points. A nugget should therefore capture only the route-independent parts of the arc: the starting stance, each genuine turning point, the ending stance, and the change itself. The test for each candidate nugget, answerable yes or no: could a correct answer, taking a different route through the corpus, omit this and still tell the same story? If yes, it is not a nugget and stays as supporting evidence; if no, it is a nugget.

   For example, the composer drafts this question and its `trajectory_must_say` (the "must-say" arcs) for one thread:

   ```
   question: How did the creator's assessment of agentic AI's real-world capability and
             impact evolve from early 2025 through early 2026?
   arcs    : - In February 2025 the creator was optimistic, arguing agentic AI systems
               could already perform all the desired science and research tasks
             - By mid-2025 he tempered this optimism, arguing it was unrealistic to expect
               agentic systems alone to resolve LLM incoherence
             - By early 2026 he concluded the anticipated 2025 agentic AI revolution had
               stalled and the autonomous-AI-software-engineer narrative had not materialized
             - He also identified persistent reliability bottlenecks in agentic/RAG systems
   ```

   Every longitudinal question also carries one shift nugget, whose job is to check whether the answer connects the endpoints of the arc rather than stating them as disconnected snapshots.
   The stance nuggets alone cannot catch this, because each can be satisfied by describing its own period in isolation:

   - The stance nuggets (n1, n2, n3) can each be hit by describing that period on its own: "in early 2025 he was optimistic," "in mid-2025 he tempered," "in early 2026 he concluded it had stalled."
   - An answer can hit all three and still never say that the optimism became the tempering became the conclusion - three correct but disconnected snapshots.
   - The shift nugget is what fails that answer: it is graded as a connection, asking whether the answer asserts the trajectory itself, not just enumerates its points.

   The final nuggets, after editing those arcs (the RAG-bottleneck line dropped as route-omittable):

   ```
   n1 (stance) He was optimistic about agentic AI's real-world capability and near-term
               impact [early 2025]
   n2 (stance) He tempered that view: on realistic evaluation, agentic performance was
               weak [mid 2025]
   n3 (stance) He concluded the anticipated agentic-AI revolution had stalled [early 2026]
   n4 (shift)  He moved from early-2025 optimism, through a mid-2025 tempering, to an
               early-2026 conclusion that the promised agentic revolution had stalled
               [Feb 2025 - Jan 2026]
   ```


## Evaluation: scoring and results

We score the frozen agent with a single LLM judge that runs on a different model family (Claude Sonnet 5) from the OpenAI gpt-5.4 agent it grades, so the system never grades its own output.
That judge always does the same thing: given a claim and a piece of text, it decides HIT or MISS on whether the text supports the claim. We use it for three different checks by changing what the claim and the text are:

- **Recall**: does the agent's answer contain each gold nugget it should? (a gold nugget checked against the agent's answer)
- **Groundedness**: is each claim the agent made actually backed by the chunks it retrieved? (an answer claim checked against the retrieved chunks)
- **Retrieval**: was each gold nugget's evidence even retrieved? (a gold nugget checked against the retrieved chunks) The share of nuggets where it was is the *retrieval ceiling*, the highest recall the agent could reach given what retrieval surfaced.

### Results

With the scorer defined, the main study is simple to state: run the frozen agent over every gold question and score each answer.
The agent (gpt-5.4, reasoning effort low, dense pgvector retrieval, top-k 10 per search, up to 15 steps) answered each of the 25 factual and 35 longitudinal questions three times.
A factual run took about 5 reasoning loops and about 4 searches in all (some loops issue no query, such as the final answer turn); a longitudinal run worked harder, about 7 loops and about 9 searches, often firing several searches in a single loop, and surfaced about 40 chunks for synthesis versus about 19 for factual.

| Metric | Factual | Longitudinal |
|--------|---------|--------------|
| Recall | 86.9% | 32.2% |
| Groundedness | 96.0% | 97.9% |
| Retrieval ceiling | 86.8% | 43.5% |

Longitudinal questions are inherently harder than factual ones: a factual answer needs a single fact from usually one place, whereas a longitudinal answer must gather and connect evidence scattered across many videos and many months.
That difficulty shows in the scores: the agent answers single-fact questions well (87%) but change-over-time questions poorly (32%).
The gap is dominantly retrieval, not reasoning: the retrieval ceiling, the fraction of gold nuggets whose evidence was retrieved at all, is only 43.5% for longitudinal against 86.8% for factual.
On the other side, groundedness is high on both tiers (96 to 98%): almost everything the agent asserts is backed by the chunks it actually retrieved, so it rarely states a claim its own evidence does not support.

### How the scoring works

Those numbers come from applying that one judge to every run.
Each run is scored by running the judge in the three directions above, over the run's answer and its retrieved chunks.
A snippet of the judge prompt ([`SYSTEM` in `eval/judge.py`](https://github.com/chanys/bounded-deep-research/blob/main/eval/judge.py#L51)):

```
You decide whether a single CLAIM is supported by a given TEXT. Output a binary
verdict - HIT or MISS - and a one-sentence reason. There is no middle category...
Be strict about substance and lenient about wording. Do not reward a text that is
merely on the same topic; require that it actually supports the specific claim.
```

Recall and retrieval hand the judge its two texts directly, but groundedness needs one extra step first.
To score it, we first extract the claims (the atomic facts) that the agent's answer makes, using an LLM call.
A snippet of that extractor prompt ([`SYSTEM` in `eval/extract_answer_claims.py`](https://github.com/chanys/bounded-deep-research/blob/main/eval/extract_answer_claims.py#L47)):

```
Extract the assertions the answer makes about what the creator said, holds, or claimed...
CRUCIAL - do not extract a cross-video SHIFT or TRAJECTORY statement... Instead extract
the individual period stances it is built from.
```

### Calibration

Every number above rests on trusting the judge's verdicts, and an LLM judge is itself a fallible model, so before relying on them we calibrate it: we measure how often its HIT/MISS verdicts agree with a human's on a sample of blind-labeled pairs.
Without this, the scores above could reflect the judge's quirks rather than the agent's behavior.

To calibrate, we draw 66 pairs to hand to both the judge and a human.
Each pair is just a claim and a piece of text, and the task is to say HIT or MISS: does this claim appear in, or get supported by, this text?

- **The pairs cover the three checks above**: recall (a gold nugget against the agent's answer), groundedness (an agent claim against the retrieved chunks), and retrieval (a gold nugget against the retrieved chunks).
- **Each check needs both clear hits and clear misses.** Most misses arise naturally, but groundedness is almost always a hit, so we add a few constructed misses: one of the agent's own claims paired with the chunks retrieved for a different, unrelated question, which cannot support it.
- **The human labels all 66 blind**, seeing only each claim and its text exactly as the judge did, with the judge's verdict and reasoning hidden.
- **The counts:** across the 66 pairs the judge determined 36 to be hits and 30 misses, while the human labeled 32 hits and 34 misses.
- **The calibration score** is how often the human and the judge agree, corrected for chance.

That chance-corrected measure is Cohen's kappa, where $p_o$ is the observed agreement and $p_e$ the agreement expected if each labeled at its own hit/miss rate:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

The observed agreement is $p_o = 62/66 = 0.9394$, and the chance agreement from the two distributions above is $p_e = \frac{36}{66}\cdot\frac{32}{66} + \frac{30}{66}\cdot\frac{34}{66} = 0.4986$, giving:

$$\kappa = \frac{0.9394 - 0.4986}{1 - 0.4986} = 0.879$$

### Ablations

With a judge we can trust, we can ask what would actually move the results.
Two ablations probe the two obvious levers: a better retriever, and no agent loop at all.

**Hybrid retrieval.**
We ran a pre-registered ablation on the longitudinal questions that swaps dense retrieval for hybrid (dense plus BM25, fused by reciprocal rank fusion), to test whether a better ranker raises the retrieval ceiling.
This was a single run, and its scores came out essentially identical to the three-run dense baseline (ceiling 40.2% against 43.5%, recall 31.1% against 32.2%): hybrid is no better than dense-only.

If a better ranker does not help, the other lever is the agent loop itself.

**Plain single-shot RAG.**
This ablation removes the ReAct loop entirely, one dense retrieval on the raw question then one synthesis call with no exploration, to price what the loop buys:

- Factual: plain RAG recall 82.0% against agent recall 86.9% (the loop adds +4.9 points).
- Longitudinal: plain RAG recall 22.6% against agent recall 32.2% (the loop adds +9.6 points).

The loop's gain is coverage, not reasoning: it lifts the retrieval ceiling, most on longitudinal, but longitudinal still caps around 44%.

### In short

Putting the main study and both ablations together: the factual-versus-longitudinal gap (87% against 32%) is dominantly a retrieval problem, since evidence for barely 44% of what a trajectory answer must say is ever retrieved.
The ReAct loop and repeated querying lift that ceiling from about 28% to about 44%, but neither a better ranker (hybrid) nor a wider context window gets past it.
The indicated fix is query decomposition by time period, not a better ranker.

## Deployment

_Coming: the AWS infrastructure and a note on CI/CD._
