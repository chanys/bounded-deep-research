# Project B: Bounded-Corpus Deep Research Agent — Master Plan (v4.2)

**Working title (external):** *Bounded-Corpus Deep Research: A Study of Harness Engineering for Agentic Systems over Expert Video Corpora*
**Working title (internal):** TransGlobal + Discover AI deep research agent
**Status:** Ready to build
**Date:** April 20, 2026 (v4.2 — adds research recipe as versioned artifact, tool return granularity, judge fallback pattern, MCP exclusion, Gemini ASR probe)
**Owner:** YS

---

## 0. Framing

### Positioning claim

> "I design, study, and ship production-grade AI agent systems. I work at the Principal / Staff / Head-of-AI level, bringing scientific discipline to applied systems engineering. Here is a recent example."

### The two-phase structure

This plan is **optimized for time-to-first-interview, not time-to-perfect-portfolio.** Financial runway pressure means the 8-week milestone is "interview-ready," not "project-complete."

- **Weeks 1–8: Ship the interview-viable artifact.** Live AWS system, baseline + one ablation, MVP writeup, demo. Begin outreach Week 8.
- **Weeks 9–14 (parallel with interviewing):** Deepen the work — two more ablations, failure taxonomy, full arXiv-style report, workshop submission decision.

The Week-8 artifact is *sufficient for Principal/Staff interviews*. The Weeks-9–14 work is quality deepening, shaped by real interview feedback on what matters.

### The six artifacts by end of Week 8

| Artifact | Form | Role |
|---|---|---|
| Live production system | Public URL on AWS, allowlisted | "I shipped this" |
| Public GitHub repo | Code, gold sets, eval harness, pre-registered hypotheses | Reproducibility |
| MVP technical summary | 2500–3500 words, structured | Primary inspectable artifact |
| Architecture diagram | Polished, vector | Communication |
| Demo video | 2–3 min walkthrough | Async share |
| Baseline + one ablation results | Numbers, one chart | Evidence of rigor |

### What makes this Principal-level at Week 8 (not just Staff-level)

- **Pre-registered hypotheses** committed to Git before baseline runs
- **Domain-expert-labeled gold set** (TransGlobal, wife-labeled)
- **Judge-human agreement reported** alongside any LLM-judge scores
- **Cross-language cross-domain generalization probe** (Discover AI) — not "one channel done well"
- **Generic-first framing throughout** — bounded-corpus methodology, channels as applications
- **Subtractive choices named and defended** — "why not Temporal, why not self-hosted ASR, why not pgvector, why not MCP"

These signals are independent of ablation count. One ablation rigorously done with these qualities beats five ablations done casually.

---

## 0.5 Differentiation from Table-Stakes Deep Research Projects

"Deep research agent" is 2026's saturated portfolio category. Thousands of people have built one. **A generic "I built a deep research agent" framing loses automatically** — not because the work is bad, but because the category is crowded. Project B's differentiation does not come from the *system*; it comes from what's done *around* the system.

### What's actually differentiating (ranked)

| # | Differentiator | Strength | Why it's rare |
|---|---|---|---|
| 1 | **Scientific rigor applied to an applied system** — pre-registered hypotheses, domain-expert gold set, calibrated LLM judges with uncertainty bounds, grounded-theory failure taxonomy | Strong | Applied AI projects rarely run real evaluation; evaluation papers rarely ship production systems; the intersection is nearly empty |
| 2 | **Project A → Project B arc** — diagnosed existing agent failures, then designed a new agent with the same rigor | Strong | Most portfolio projects stand alone |
| 3 | **Generic-first framing** — a study with channels as applications, not a product | Moderate | Competes in the small "research contribution" category instead of the saturated "AI product" category |
| 4 | **Cross-language cross-domain generalization probe** | Moderate | Existing deep research benchmarks (DeepSearchQA, DRACO, ReportBench) are all English-web-scale; bounded-corpus cross-corpus transfer is absent |
| 5 | **Bounded-corpus as a distinct scientific setting** | Moderate | Named explicitly as a research framing, not just "RAG over YouTube" |
| 6 | Full AWS deployment with IaC | Weak-to-moderate | Credibility floor; doesn't differentiate on its own |
| 7 | Roll-your-own ReAct loop, not a framework | Weak | Talking point only unless backed by visible harness work |

### What is NOT differentiating (table stakes)

- Hybrid retrieval (BM25 + dense) — standard
- Frontier-model planner (Opus, GPT-5) — standard
- Citation support in answers — claimed by every deep research product
- Full-stack deployment — floor, not ceiling
- "RAG pipeline" — category-level move
- Running ablations — common; what's rare is pre-registered, statistically-treated ablations

**Do not overclaim these in the writeup.** Senior reviewers will notice and discount.

### The honest competitive landscape

- **Tier A** — Hobbyist tutorial-follow-along projects. Project B is clearly above.
- **Tier B** — Mid-senior engineers who ship RAG at work. Project B is competitive; wins on study dimension, may lose on production scale.
- **Tier C** — Senior applied AI scientists at frontier labs. Credential story (PhD + DARPA PI + two rigorous projects) gets you into the conversation; Project B shows you're current and hands-on. **This is the realistic target tier.**
- **Tier D** — Research scientists publishing agent work at NeurIPS/ICLR. Different path; not the target.

### The framing imperative

Two candidates could ship identical systems. The one framed as *"I built a deep research agent"* gets filed under "generic AI engineer." The one framed as *"I studied harness engineering for bounded-corpus deep research, with findings on cross-language and cross-domain transfer"* gets filed under "applied AI scientist."

**Same work, different category. The category determines the roles.**

Three writeup disciplines enforce this:

1. **Open the MVP summary with the research question, not the system.**
2. **Lead the README with the Project A → Project B arc, not the tech stack.**
3. **State every differentiator explicitly** — don't make reviewers connect dots. Plain sentences like: "Pre-registered hypotheses are uncommon in applied AI engineering writeups; they are included here to support SQ2 and SQ3."

---

## 0.6 Is This Truly Agentic? (And the FirstCall Lesson)

A central question for Principal-level positioning: **does Project B actually exhibit agency, or is it an LLM-decorated pipeline?** This matters because it was *exactly the diagnosis* that killed the FirstCall project ("conversational controller, not truly agentic"). If Project B earns the same diagnosis, it fails the positioning test.

### Definition used throughout the plan

**A system is agentic to the degree that the LLM makes open-ended decisions about what actions to take next, based on previous observations, in pursuit of a goal.** (Anthropic's framing; Shreya Shankar's and Hamel Husain's align.)

The test: **at each step, does the LLM choose what to do next, or does the code?**

- If the code has a fixed sequence (search → summarize → synthesize → output), it's a **workflow** with LLM calls inside. Not agentic.
- If the LLM chooses its next action based on observations (*"I should search again with different terms," "I've seen enough; stop and synthesize"*), it's **agentic**.

### Where Project B sits

**Agentic (the LLM drives):**
- *Query formulation* — the agent decides what to search for, and how to refine searches based on partial results
- *Depth selection* — the agent decides which videos/segments warrant full read vs. snippet
- *Stopping* — the agent decides when evidence is sufficient to synthesize (with a controller-enforced fallback gate at step budget)
- *Answer structure* — the agent structures the response based on what it found, not a template

**Non-agentic (code drives, correctly):**
- Ingestion pipeline (scripted, deterministic)
- Evaluation framework (deterministic measurement)
- Retrieval execution once the agent has formulated the query
- Summarization sub-agent (a tool the agent *calls*, follows fixed prompt)

### The honest characterization

> Project B's agent is a **bounded agentic system with a controller-enforced stopping gate.** The LLM has genuine open-ended authority over query formulation, reading depth, and stopping — the three decisions that matter most for deep research. It does not have authority over tool installation, prompt modification, or sub-agent spawning.

This is the same class of agency as OpenAI's deep research, Perplexity's, and Anthropic's — bounded agentic systems with controller gates, not fully-autonomous unbounded agents. The claim is accurate and does not overstate.

### The interview-ready answer

When asked *"is this really agentic?"*:

> "Yes. The agent makes three classes of open-ended decisions that define whether a system is agentic for deep research: query formulation, depth of reading, and when to stop. These are the same decisions the DeepSearchQA benchmark found even the best systems fail at 34% of the time — which is exactly why I'm studying them. I enforce a stopping gate at the controller level, which I'd characterize as bounded agency rather than full agency. Project A taught me that unconstrained agency produces the premature-stop failure mode, so bounded agency is the deliberate design choice for reliability."

### The FirstCall contrast (when asked)

When asked *"how does this differ from your FirstCall work?"*:

> "FirstCall was a state machine with LLM-generated text at each state. The control flow was deterministic; the LLM only produced natural language. Project B's agent chooses actions based on observations at each step — query formulation, reading depth, stopping. The LLM drives control flow, not just text generation. That's the categorical difference between a conversational controller and an agentic system."

---

## 0.7 Harness Engineering Dimensions (Honest Audit)

The positioning claim includes "harness engineering" — which has a specific meaning in the current literature: **the code and design choices surrounding the LLM that shape how it operates as an agent.** Project B must demonstrate real exposure to multiple harness dimensions, not just surface-level agent construction.

### The seven harness dimensions

Honest grades for what Project B exercises:

| # | Dimension | Exposure | Studied as ablation? |
|---|---|---|---|
| 1 | **Scaffolding code** (ReAct loop, step function, error handling) | Strong | No (craft) |
| 2 | **Tool interface design** (schemas, failure modes, output formats) | Moderate | No (craft) |
| 3 | **Context management** (raw vs. summarized; window budget) | Strong | **Yes (A2, Week 9)** |
| 4 | **Stopping policy** (step budget, controller-enforced submit) | Strong | **Yes (A3, Week 10)** |
| 5 | **Verification layer** (checks on LLM output before acceptance) | Conditional | Added if Week 7 baseline shows citation hallucination is dominant |
| 6 | **Prompt architecture** (system prompt, reasoning scaffolds) | Moderate | Optional (A4, Week 11 if time) |
| 7 | **Retrieval interface** (what the agent sees from search) | Strong | **Yes (A1, Week 7)** |

### The verification-layer decision (important, honest)

An earlier draft of this plan proposed a runtime citation-verification gate as a harness intervention analogous to Project A's `VerifyingAgent`. On examination, the proposal was **conflating two different things**:

- **Provenance verification** — "does this citation point at something real?" — **free**, because the agent copies `video_id`, timestamps, and text directly from retrieval results. No gate can add value here.
- **Semantic support verification** — "does the chunk actually support the claim?" — **not free**, requires judgment (another LLM call). The real failure mode a gate could catch.

A runtime semantic verification gate has real costs (latency, extra LLM calls, self-judgment weakness) and is only worth adding *if* the Week 7 baseline shows citation hallucination (not coverage gaps, not synthesis incoherence) is the dominant failure mode.

**Decision rule:** Build the baseline first, see what fails, intervene on what fails. This is what Project A did with mini-swe-agent. Premature verification is over-engineering.

### The aggregate claim

Project B exercises **5 of 7 harness dimensions at moderate-to-strong depth, with 3 of those studied as ablation variables with pre-registered hypotheses and statistical treatment.** The remaining 2 (verification, prompt architecture) are conditional on baseline findings.

This is legitimate harness engineering exposure. The writeup does not need to claim coverage of all 7 to be defensible; naming the 3 studied ablations and the judgment behind the conditional 2 *is* the Principal-level move.

---

## 0.8 Evaluation Methodology (The Hamel/Shreya Spine)

The evaluation framework is Project B's primary differentiator (§0.5). It follows the practitioner methodology developed by Hamel Husain and Shreya Shankar in their applied LLM evaluation course — methodology that has become the de facto standard in 2025–2026. Using its vocabulary and protocols is not copying; it is **speaking the shared language of the field**, which senior reviewers (who have often read or taken the course) will recognize immediately.

### The Analyse → Measure → Improve loop (the methodological spine)

The full project organizes around three phases, applied iteratively:

1. **Analyse** — read traces, discover failure modes (qualitative, grounded-theory style)
2. **Measure** — translate failure modes into automated evaluators (quantitative, binary-testable)
3. **Improve** — change prompts / harness / retrieval based on what measurement reveals

Each ablation is one pass through this loop on a specific harness dimension.

### Grounded-theory failure taxonomy (Week 7)

Failure analysis follows the explicit qualitative research protocol:

1. **Open coding** — read each failed trace end-to-end, write short free-form notes about what went wrong. No predefined categories.
2. **Axial coding** — cluster open codes into a taxonomy of named failure modes.
3. **Saturation check** — continue reading traces until 5 consecutive traces produce no new categories (theoretical saturation reached).
4. **Relabeling** — revisit early traces with the mature taxonomy.

### Binary, testable failure modes

Every failure mode in the taxonomy is phrased as a **yes/no question tied to a single observable.** Vague categories become operational:

| ❌ Vague | ✅ Binary & testable |
|---|---|
| "Premature stop" | "Agent submitted answer before issuing ≥2 distinct search queries" |
| "Citation hallucination" | "Cited chunk's text does not contain the specific claim made in the answer" |
| "Incomplete coverage" | "Gold set contains ≥1 relevant video not retrieved in any search query during the run" |
| "Synthesis incoherence" | "Answer contains contradictory claims within the same paragraph" |
| "Terminology confusion" | "Agent conflated two distinct named entities (e.g., two AI models, two indicators)" |

Binary phrasing makes each failure mode either code-checkable or LLM-judge-checkable with unambiguous input/output.

### Code-first evaluators, LLM judges as fallback

Following Hamel/Shreya's strong preference: reach for code-based checks first. LLM judges only when the check is inherently semantic.

| Check | Evaluator type |
|---|---|
| Citation format validity (schema, field presence) | Code |
| Citation pointer existence (video_id / timestamp in index) | Code |
| Citation content match (chunk hash matches retrieval) | Code |
| Premature-stop detection (step count, tool sequence) | Code |
| Retrieval P/R/F1 against gold set | Code |
| **Citation grounding** (does chunk *support* the claim) | **LLM judge** (semantic) |
| **Synthesis rubric** (completeness, coherence) | **LLM judge** (semantic) |

Code checks are cheap, trustworthy, and don't require evaluating an evaluator. LLM judges are reserved for genuinely semantic questions where no code can substitute.

### LLM judge calibration (TPR/TNR + bootstrap)

When an LLM judge is used, it is calibrated against human labels, and its raw output is bias-corrected.

**Vocabulary in plain language:**

- **TPR (True Positive Rate):** Of the cases humans labeled PASS, what fraction does the judge also label PASS? *Answers: "does my judge correctly recognize good outputs?"*
- **TNR (True Negative Rate):** Of the cases humans labeled FAIL, what fraction does the judge also label FAIL? *Answers: "does my judge correctly catch bad outputs?"*

A judge with 90% TPR and 70% TNR is optimistic — it over-reports PASS. Raw "82% passing" from such a judge is not the true passing rate; it's a biased measurement.

**Bias correction:** a formula combining raw pass rate with TPR and TNR to recover the unbiased estimate. (Standard formula; derivable from the confusion matrix.)

**Bootstrap confidence intervals (plain language):** Repeatedly resample the human-labeled calibration set *with replacement* (say, 1000 times). Re-estimate the corrected pass rate on each resample. Report the 2.5th and 97.5th percentiles as the 95% confidence interval. This says: *"given the size of my calibration set, the true pass rate is likely between X% and Y%."*

**Why this matters:** without bootstrap CIs, reporting "83% passing" sounds precise. With bootstrap, you report "83% [76%, 88%] with n=50 calibration samples" — which is both more honest and, counterintuitively, **more credible** to senior reviewers, because it shows statistical maturity.

### Session-level before turn-level

For multi-step agent runs, session-level success is primary: *"did the agent produce a correct answer for this gold query?"* Turn-level evaluation (was this specific tool call appropriate?) is a debugging tool, not a primary metric. A run can have an awkward intermediate step and still succeed; a run can have perfect-looking steps and still fail.

### Distribution-shift and data-leakage discipline

- **Distribution shift:** gold set queries are drawn from realistic query types (by pre-registered protocol, §6), not from whatever is easy to label. Threat to validity documented in writeup.
- **Data leakage:** gold set queries are not used in few-shot examples, system prompts, or judge calibration prompts. Enforced by separate file paths and a CI check.

---

## 1. Research Question

### Central question

**How do harness-engineering decisions affect reliability in deep research agents operating over bounded, domain-specific video corpora?**

### Sub-questions

**SQ1** — *Failure taxonomy.* What are the dominant failure modes of a deep research agent over bounded video corpora, and how do they compare to failure modes documented in DeepSearchQA, DRACO, and ReportBench?

**SQ2** — *The bounded-corpus redundancy effect.* Web-scale deep research benefits from source redundancy; bounded corpora do not. **Hypothesis:** precision-oriented harness configurations transfer from web-scale; recall-oriented configurations require changes, because every retrieval miss is unrecoverable.

**SQ3** — *Cross-domain generalization.* Do harness decisions that optimize reliability on a Chinese financial advisory corpus transfer to an English AI research commentary corpus — i.e., are harness decisions primarily driven by corpus *structure* (bounded, single-creator, multi-hour aggregate) rather than *domain* or *language*?

### Scope by Week 8

- SQ1: preliminary failure taxonomy from Week 7 baseline (3–5 categories named, with examples)
- SQ2: one ablation (retrieval mode) addresses this directly
- SQ3: winning retrieval config tested on Discover AI (generalization probe)

### Scope by Week 14 (post-interview-start)

- SQ1: full taxonomy with prevalence data
- SQ2: three ablations covering retrieval, context, stopping
- SQ3: full generalization analysis

---

## 2. Scope (v4.2, hard)

### In scope for Week 8

- Two channels: **TransGlobal** (Chinese, financial services, primary study) + **Discover AI / code4AI** (English, AI research, generalization probe)
- Corpus windows: TransGlobal 12 months; Discover AI last 6 months (~200 videos)
- Production AWS deployment: public URL, custom domain, HTTPS, email-allowlist auth
- Next.js frontend with SSE streaming, citation cards, timestamp deep-links
- Hybrid retrieval on OpenSearch Service (BM25 + dense + RRF)
- Scripted ingestion (no Temporal, no proxy pool, no self-hosted ASR)
- Terraform IaC, GitHub Actions + OIDC CI/CD
- Langfuse + CloudWatch observability
- Gold sets: 25 TransGlobal queries (wife-labeled), 12–15 Discover AI queries (self-labeled with pre-registered protocol)
- One ablation (retrieval mode: BM25 / dense / hybrid) × 3 seeds on TransGlobal; winner re-run on Discover AI with 1 seed
- MVP writeup (2500–3500 words), architecture diagram, demo video

### Deferred to Weeks 9–14 (parallel with interviewing)

- Second ablation: context mode (full / summarized)
- Third ablation: stopping policy (budget-only / controller-enforced)
- Full failure taxonomy with prevalence data
- Full arXiv-style report (6000–10,000 words)
- Workshop submission decision

### Explicitly out of scope entirely (deferred indefinitely)

- Temporal (not warranted — scripted pipeline suffices for one-time bounded ingestion)
- Self-hosted ASR (not warranted — English auto-captions for Discover AI, Chinese auto-captions for TransGlobal are sufficient; Whisper API as per-video fallback)
- Self-hosted embeddings (not warranted — OpenAI `text-embedding-3-large` handles Chinese + English, one-time ingestion cost ~$15)
- Custom cost dashboard (folded into `/system` page with Langfuse + Cost Explorer numbers)
- Proxy pool (not warranted — polite-paced ingestion from home IP avoids blocks)
- Sentry (optional; free tier is fine if wired in an hour, otherwise skip)
- **MCP for tool registration** (not warranted — single-caller architecture; portability across MCP clients is not a requirement; see §10)
- Multi-region / HA, SSO/RBAC, real-time SLA, mobile UI, fine-tuning, load testing

Each "not warranted" is a sentence in the writeup explaining the judgment.

---

## 3. Target Architecture

```
          ┌──────────────────────────────────────────────────────────┐
          │          User (allowlisted email via Cognito)            │
          └─────────────────┬────────────────────────────────────────┘
                            │ HTTPS, custom domain
                            ▼
          ┌──────────────────────────────────────────────────────────┐
          │  CloudFront + S3 (Next.js 15 static export)              │
          └──────────────────┬───────────────────────────────────────┘
                             │ /api/*
                             ▼
          ┌──────────────────────────────────────────────────────────┐
          │  ALB → ECS Fargate (FastAPI, single service)             │
          │  - /query (SSE streaming)                                │
          │  - /runs (eval history, read-only)                       │
          │  - /system (architecture, live dashboards link-outs)     │
          └───┬──────────────┬────────────────┬─────────────────────┘
              │              │                │
              ▼              ▼                ▼
     ┌──────────────┐ ┌──────────────┐  ┌──────────────────┐
     │ Agent Loop   │ │ OpenSearch   │  │ RDS Postgres     │
     │ (ReAct) on   │ │ Service      │  │ (gold set, runs, │
     │ ECS Fargate  │◀┤ (BM25 +      │  │  video state)    │
     │              │ │  dense + RRF)│  └──────────────────┘
     └──────┬───────┘ └──────────────┘
            │ LLM calls
            ▼
     ┌──────────────────────┐
     │ Anthropic API        │
     │  Opus 4.7 planner    │
     │  Haiku 4.5 summarize │
     └──────────────────────┘

   Ingestion (scripted Python, one-time per channel):
   ┌───────────────────────────────────────────────────────────────┐
   │ ingest.py                                                     │
   │   1. Fetch video list (YouTube Data API + manifest.json)      │
   │   2. Fetch transcripts (youtube-transcript-api, 30–90s delay) │
   │   3. Cleanup pass (Haiku: terminology, punctuation)           │
   │   4. Chunk (timestamp-aligned 30s windows, 10s overlap)       │
   │   5. Embed (OpenAI text-embedding-3-large)                    │
   │   6. Index (OpenSearch + Postgres state)                      │
   │                                                               │
   │ Idempotent: re-run skips completed videos via Postgres check  │
   │ Resumable: Ctrl-C safe, crash safe                            │
   └───────────────────────────────────────────────────────────────┘

   Observability:
     Langfuse SaaS  — LLM traces, per-step costs
     CloudWatch     — infra metrics, logs, dashboards, alarms
     /system page   — surfaces key numbers for demos
```

---

## 4. Tech Stack (Final)

### Application

| Layer | Choice | Rationale |
|---|---|---|
| Ingestion | **Scripted Python, Postgres idempotency** | Bounded one-time ingest doesn't warrant Temporal |
| Transcripts primary | **`youtube-transcript-api`** with 30–90s delays | Polite pacing avoids IP block |
| Transcripts fallback | **Whisper API** (per-video, as needed) | Rare (<5% expected for English; maybe 5–15% for Chinese) |
| Transcript cleanup | **Claude Haiku 4.5 pass** | Fixes ticker symbols, model names, adds punctuation |
| Metadata DB | **RDS Postgres 16** (smallest tier) | State + gold set + run history |
| Transcript storage | **S3** (JSONL per video, SHA-256 checksums) | Corpus reproducibility |
| Search index | **OpenSearch Service** (smallest tier, single node) | Hybrid retrieval ablation load-bearing for study |
| Embeddings | **OpenAI `text-embedding-3-large`** via API | Multilingual, one-time cost ~$15 |
| Agent framework | **Roll-own ReAct loop** (mini-swe-agent style) | Keeps harness decisions explicit, Project A style carries forward |
| Planner LLM | **Claude Opus 4.7** | Synthesis quality |
| Summarization sub-agent | **Claude Haiku 4.5** | Cost-sensitive |
| LLM judge | **Claude Opus 4.7** with 20% human spot-check | Judge-human agreement reported |
| Observability (LLM) | **Langfuse SaaS** | Framework-agnostic, open-source |

### Infrastructure

| Layer | Choice | Rationale |
|---|---|---|
| IaC | **Terraform** (state in S3 + DynamoDB lock) | Industry-standard, portable |
| API compute | **ECS Fargate** single service | Right-sized; Lambda timeout unsuitable for agent runs |
| Frontend framework | **Next.js 15 App Router + Tailwind + shadcn/ui** | Polished UI without deep frontend investment |
| Frontend hosting | **CloudFront + S3** static export | All-AWS |
| DNS / TLS | **Route 53 + ACM** | Standard |
| Auth | **Cognito email allowlist** | Prevents crawlers; minimal config |
| Secrets | **AWS Secrets Manager** | KMS-backed |
| CI/CD | **GitHub Actions + OIDC to AWS** | No long-lived keys |
| Container registry | **ECR** | Standard |
| Infra observability | **CloudWatch** dashboards + alarms | Free, integrated |
| Testing | **pytest** + 1 Playwright E2E | Right-sized for 8-week scope |

### What's intentionally NOT in the stack

- ❌ Temporal (scripted pipeline suffices)
- ❌ Self-hosted ASR (API fallback handles rare case)
- ❌ Self-hosted embeddings (API is cheaper + simpler)
- ❌ pgvector (OpenSearch enables cleaner retrieval ablation)
- ❌ Proxy pool (polite-paced ingestion avoids blocks)
- ❌ Sentry (optional, skip if time-pressured in Week 6)
- ❌ Custom cost dashboard (folded into /system page)
- ❌ **MCP for tool registration** (v4.2 — single-caller architecture; tool portability across clients isn't a requirement)

Each exclusion is a one-sentence judgment-signal in the writeup.

---

## 5. Phase Plan (8 weeks)

### Phase 0 — Walking Skeleton (Week 1, Apr 20–26)

End-to-end local system on 10 videos (5 TransGlobal, 5 Discover AI) by end of week.

**Deliverables:**
- Repo scaffold (`bounded-deep-research`), uv env, docker-compose (Postgres, OpenSearch, Langfuse)
- 10 hardcoded video IDs ingested to local OpenSearch
- FastAPI + minimal ReAct loop (2 tools: search, submit; 10-step budget)
- Next.js 15 dev UI with SSE streaming, basic citation cards
- Langfuse traces visible
- YouTube deep-link citation format working

**Exit criteria:** `docker-compose up && pnpm dev` → query → streaming answer with 3 clickable citations. **End of Friday Apr 24.** If not met: no Phase 1 until met.

**Pre-work this weekend (Apr 19–20):**
- [ ] Domain name purchased
- [ ] AWS account verified, billing alerts set
- [ ] Anthropic + OpenAI API keys
- [ ] GitHub repo created, initial README committed
- [ ] `bounded-deep-research` repo name confirmed (or alternative)

### Phase 1 — Ingestion + Retrieval (Week 2, Apr 27 – May 3)

Both channels ingested locally with hybrid retrieval working.

**Deliverables:**
- Ingestion pipeline: fetch → cleanup pass → chunk → embed → index
- Idempotency via Postgres state table (video_id + content hash)
- Polite-paced fetching with tenacity retries + tqdm progress
- TransGlobal 12-month snapshot ingested (~150–300 videos estimated)
- Discover AI 6-month snapshot ingested (~200 videos, excluding members-only)
- OpenSearch hybrid retrieval: BM25 + dense via OpenAI `text-embedding-3-large`. Hybrid via RRF
- Title/description boost as configurable field weight
- `search_transcripts(query, k, mode)` tool accepts `mode` ∈ {bm25, dense, hybrid}

**Exit criteria:**
- 95%+ videos usable for both channels (transcript availability)
- Re-running ingest is a no-op
- 5 manual queries return top-10 in each retrieval mode; you can argue about the differences
- Corpus manifest auto-generated (video IDs, checksums, transcript source, duration, language)

**Risk note:** TransGlobal video count is unknown. If >400 videos, consider 9-month snapshot instead of 12.

### Phase 2 — Agent Loop + Context Engineering (Week 3, May 4–10)

Baseline agent answers multi-aspect queries with citations on both corpora.

**Deliverables:**
- ReAct loop: tools `search_transcripts`, `read_video_segment`, `submit_answer`
- **Research recipe as versioned system prompt (new in v4.2):** `prompts/research_recipe.md` in the repo — a numbered procedural prompt describing when to search, when to escalate from snippet to full read, when to stop, and what to do when a tool returns zero useful results. Includes an explicit **Critical Failure Policy** rule: if any tool returns zero useful results on a query, the agent halts and reports ("0 results found for X; unable to answer without additional evidence") rather than fabricating a synthesis. Treated as code — committed before baseline, stable within an ablation cell, swapped only at ablation-level boundaries (A4 if run). This artifact is what the §0.6 agentic characterization is built on: the LLM follows the recipe but chooses which step applies when.
- **Tool return granularity (new in v4.2):** `search_transcripts` returns title + timestamp + 80–120-token snippet per hit (top-10); `read_video_segment` returns the full 30-second chunk, raw or summarized per config. Search stays context-cheap; escalation to full read is the agent's explicit decision, which (a) keeps working context small during the search phase, (b) gives the A2 (context mode) ablation a clean boundary at the read layer rather than muddying search, and (c) produces three naturally-distinct failure modes to study: *missed in search*, *saw-snippet-didn't-escalate*, *read-but-misattributed*.
- Citation format: `{video_id, start_ts, end_ts, supporting_text_hash}` — hash enables programmatic verification later
- Summarization sub-agent (Haiku 4.5): `read_video_segment` returns raw or summarized (config flag, A2 ablation variable)
- Stopping policy: step budget (15 max) + forced `submit_answer` (controller-enforced, Project A lesson carried forward)
- Bilingual content handling (EN technical terms in zh content, full EN for Discover AI) — folded into the research recipe prompt above
- Langfuse instrumentation on every tool call
- SSE streaming to Next.js frontend: retrieval steps, tool calls, tokens in-flight, final answer

**Exit criteria:** Runs 5 trial queries per channel end-to-end, ≥3 citations each, streams cleanly to frontend, no crashes. Research recipe prompt and tool granularity locked; subsequent phases don't revisit these interfaces.

### Phase 3 — Frontend Polish (Week 4, May 11–17)

The production demo UI.

**Deliverables:**
- Query input with 3 example prompts per channel
- Streaming trace panel: retrieval queries, tool calls, token-in-flight indicator, elapsed time
- Answer panel: rendered markdown
- Citation cards: video thumbnail + title + timestamp range → click opens YouTube at timestamp
- `/system` page: architecture diagram, cost numbers (Langfuse + Cost Explorer link-outs), eval results placeholder
- Dark mode, responsive, loading/error states
- Channel selector (TransGlobal / Discover AI)

**Exit criteria:** Would demo to a CTO without apologizing.
**Cap:** 7 days. shadcn/ui defaults only. No custom components. If a feature takes > half a day, cut it.

### Phase 4 — Gold Set + Eval Harness (Week 5, May 18–24)

The evaluation framework — the portfolio differentiator. Upgraded in v4.1 with Hamel/Shreya protocols (§0.8); judge implementation pattern added in v4.2.

**Pre-registration before queries are written:** commit to Git:
- Query-generation protocol for each channel (2 paragraphs each)
- Hypotheses H1–H2 (see §6) with timestamps
- Judge prompt (initial draft; may be revised once before calibration)

**Deliverables:**

**(a) TransGlobal gold set (25 queries, wife-labeled):**
- Tier 1 (single-indicator/topic factual): 15 queries
- Tier 2 (multi-topic comparative): 7 queries
- Tier 3 (longitudinal/contradiction): 3 queries
- 2 half-day sessions with wife for labeling
- JSON artifact versioned in repo

**(b) Discover AI gold set (12–15 queries, self-labeled with pre-registered protocol):**
- Tier 1: 8 queries
- Tier 2: 4 queries
- Tier 3: 2–3 queries (leveraging creator's opinion evolution, e.g., chain-of-thought views)
- Self-labeling honesty: 3-query sample cross-labeled for agreement check; asymmetric-rigor caveat in writeup

**(c) Adversarial retrieval probe (5–8 queries, new in v4.1):**
- Each query constructed to distinguish semantic from keyword matching (see §6)
- Used as a qualitative diagnostic, reported separately from the main gold set

**(d) Metrics suite (upgraded in v4.1):**

| Metric | Measures | Evaluator | Reference |
|---|---|---|---|
| Retrieval Precision@10 | Fraction retrieved that are relevant | Code | DeepSearchQA |
| Retrieval Recall | Fraction of gold retrieved | Code | DeepSearchQA |
| Retrieval F1 | Harmonic mean | Code | DeepSearchQA |
| **Retrieval MRR** (v4.1) | Rank of first relevant chunk | Code | IR literature |
| Citation format validity | Schema, field presence | Code | — |
| Citation pointer existence | video_id, timestamp in index | Code | — |
| **Citation grounding** | Does cited chunk support the claim? | **LLM judge (calibrated)** | ReportBench, DRACO |
| Citation coverage | Every claim has citation | Code | DRACO |
| **Synthesis rubric** | 1–5 on completeness/coherence/accuracy | **LLM judge (calibrated)** | ResearchRubrics |
| Premature stop | <2 distinct searches before submit | Code | Project A failure taxonomy |

**(e) Judge calibration protocol (new in v4.1, §6, §0.8):**
- Build 30–40 (trace, verdict) calibration set hand-labeled by YS + wife
- Measure TPR (judge PASS when human PASS) and TNR (judge FAIL when human FAIL)
- Apply bias correction to production pass rates
- Report bootstrap 95% CIs (1000 resamples) for all judge-derived metrics
- Re-calibrate if judge prompt changes

**(f) Judge implementation pattern (new in v4.2, §0.8):**
- Judge returns a Pydantic model with `Literal["pass", "fail"]` verdict, `Literal["high", "medium", "low"]` confidence, and reasoning text — the `Literal` types constrain the LLM output into the valid set via structured output / function calling
- On parse error, schema mismatch, or LLM exception: default to `fail` verdict, not to silently dropping the sample — preserves both the denominator and a conservative headline
- Parse error rate and exception rate logged per run and reported alongside TPR/TNR in the Week 8 writeup
- Rationale: silent drops shrink the denominator and hide reliability problems; silent promotions to PASS inflate the metric; explicit fail-default preserves both the count and the pessimism. This matters specifically because the Week 8 headline is a bias-corrected pass rate — a 2% silent failure rate defaulting to PASS inflates the headline by 2% in ways the bias correction does not catch.
- Pattern applies equally to any structured LLM call inside the agent itself (e.g., if query rewriting is ever implemented as a structured LLM call); not just the judge.

**(g) Runner:** `uv run eval --suite gold --channel transglobal --config configs/baseline.yaml` → JSON + Markdown report with point estimates and 95% CIs.

**Exit criteria:** Gold sets locked + committed. Adversarial probe committed. Judge calibration set built; TPR/TNR measured; judge implementation pattern in place with parse-error rate logging. Eval runner end-to-end working with bias-corrected numbers and CIs. Sample baseline on 5 queries produces calibrated numbers.

### Phase 5 — AWS Deployment (Week 6, Jun 1–7)

Public URL works, reproducible from scratch.

**Deliverables:**
- Terraform stack: VPC, ECS cluster, ALB, RDS, OpenSearch Service, S3, CloudFront, Route 53, ACM, Cognito, Secrets Manager, ECR, CloudWatch dashboards, budget alarms
- GitHub Actions: OIDC → AWS, push-to-main deploys
- Both corpora reindexed into production OpenSearch
- Custom domain live with HTTPS
- Email allowlist seeded (you, wife, 2–3 trusted reviewers)

**Exit criteria:**
- Send a link → allowlisted user queries the system → streaming answer returned
- `terraform destroy && terraform apply` reproduces a working system
**Cap:** Half-day per AWS sub-problem. Exceeded → simplify the layer. Terraform AWS modules, not hand-rolled IAM.

### Phase 6 — Baseline + Retrieval Ablation + Failure Synthesis (Week 7, Jun 8–14)

First real production numbers.

**Deliverables:**
- Full baseline run on both gold sets in production with bias-corrected metrics + bootstrap CIs
- Retrieval ablation (A1): BM25 / dense / hybrid × 3 seeds on TransGlobal
- Winner config re-run on Discover AI (generalization probe, 1 seed)
- Adversarial probe run on winner config — qualitative diagnostic of semantic vs. keyword matching
- **Grounded-theory failure analysis (upgraded in v4.1, §0.8):**
  - Open coding on every failed trace (free-form notes, no preset categories)
  - Axial coding to cluster open codes into named failure modes
  - Saturation check — continue until 5 consecutive traces produce no new categories
  - Each failure mode phrased as a **binary testable question** (not a vague label)
  - Relabel early traces with the mature taxonomy
- **Conditional verification decision (new in v4.1, §0.7):**
  - If citation hallucination is the dominant failure mode → runtime semantic verification gate goes into Weeks 9–10 ablation backlog
  - If a different failure dominates → intervention targets that failure instead
  - Decision logged explicitly in synthesis document
- Synthesis document `project-b-baseline-findings.md` — mirrors `terminal-bench-failure-synthesis-comprehensive.md` structure, with Three-Gulfs framing (§0.8) applied to each dominant failure
- Results chart for A1

**Exit criteria:**
- Dominant failure mode named in one binary, testable sentence, with evidence
- A1 results table with mean ± std + 95% CI across seeds
- Generalization probe result: "hybrid wins on TransGlobal; it also wins / does not win / partially wins on Discover AI" — stated with confidence intervals
- Weeks 9–10 intervention backlog written, ranked by expected impact on dominant failure

### Phase 7 — MVP Writeup + Launch (Week 8, Jun 15–21)

Convert work into interview-ready artifacts. **The framing disciplines in §0.5 are enforced here** — generic writeups are table stakes; study-framed writeups are the differentiator.

**Deliverables:**

**(a) MVP technical summary** (2500–3500 words), structured to front-load what's differentiating:

1. **Abstract (150 words)** — opens with research question, not system description
2. **Introduction** — motivates bounded-corpus deep research as a distinct setting (§0.5); references Project A explicitly; states pre-registered hypotheses (§6)
3. **Related work** — DeepSearchQA, DeepResearchEval, ResearchRubrics, DeepResearch Bench, ReportBench, DRACO — and how this study's framework extends, modifies, or simplifies each
4. **System** — architecture, harness design, agentic framing (§0.6), roll-your-own-loop rationale, research recipe prompt as versioned artifact
5. **Method** — corpus construction, gold-set protocol, **calibrated LLM judges with TPR/TNR + bootstrap CIs** (§0.8), grounded-theory failure analysis
6. **Results** — baseline + A1 with bias-corrected numbers and CIs, adversarial probe, generalization probe
7. **Failure taxonomy (preliminary)** — binary testable categories, Three-Gulfs framing (§0.8)
8. **Discussion** — what transfers across language/domain, what doesn't, the harness-dimension audit (§0.7), what's in Weeks 9–14
9. **Limitations & threats to validity** — single ablation, self-labeled probe for Discover AI, judge-model bias, gold set size, judge parse-error rate
10. **Reproducibility** — repo, calibration set, pre-registration commits, research recipe prompt

**Writeup framing discipline (§0.5):**
- Opens with research question, **not** system description
- Every differentiator stated plainly (pre-registration, judge calibration, cross-corpus probe — each gets a sentence explaining *why it's uncommon*)
- Subtractive choices defended explicitly (why not Temporal, why not self-hosted ASR, why not runtime verification-pre-baseline, why not MCP — §0.5, §0.7, §10)
- Project A → Project B arc established in Introduction, closed in Discussion
- Generic-first throughout — "bounded-corpus deep research," channels as applications

**(b) README** — 3-minute skim that lands the identity claim. Opens with the two-project arc, not the tech stack (§0.5).

**(c) Architecture diagram** — polished vector, same topology as §3 ASCII version.

**(d) Demo video** — 2–3 min walkthrough of live system + key results. Narration matches writeup framing (study, not product).

**(e) LinkedIn long-form summary** — generic-first, study-framed, 600–900 words.

**(f) Project A writeup** — reviewed and published if not already. Linked from Project B README as the *diagnose* half of the arc.

**(g) Outreach launch:**
- 20 named targets identified (companies + specific people)
- First message drafted, customized per target; references both projects and the arc
- Application tracker set up
- First batch sent Week 9

**Exit criteria:** Portfolio artifacts published. A hiring manager reading only the README and Abstract understands (1) what was built, (2) what was found, (3) why either is uncommon — in 3 minutes.

### Phases 8–14 (Weeks 9–14, parallel with interviewing)

- **Week 9:** Second ablation (A2: context mode — full / summarized). Start interview outreach. *If Week 7 named citation hallucination dominant, A2 swaps to runtime verification gate instead of context mode.*
- **Week 10:** Third ablation (A3: stopping policy — budget / controller-enforced). Interviews in progress.
- **Week 11:** Full failure taxonomy with prevalence data across three ablations; Three-Gulfs categorization per failure mode.
- **Week 12:** Full arXiv-style report drafting (sections 1–6 — system, method, results, discussion).
- **Week 13:** Report finalization. Workshop submission decision (venues: NeurIPS Agents, ICLR LLM Agents, COLM workshops).
- **Week 14:** Outreach expansion. Report published.

These phases are **shaped by interview feedback.** If hiring managers consistently ask about X, prioritize X. If nobody asks about the workshop paper, skip it.

---

## 6. Experimental Design (Pre-registered)

### Hypotheses (committed to Git before Week 7 baseline run)

- **H1:** Hybrid retrieval > BM25 > dense on Retrieval F1 *and* MRR for TransGlobal Tier 2 queries, with gap larger than for Tier 1.
- **H2:** The winning retrieval configuration on TransGlobal is also the winning configuration on Discover AI (transfer hypothesis supporting SQ3).

### Deferred hypotheses (committed before Week 9 ablations)

- **H3:** Summarized context mode loses more on citation groundedness than synthesis rubric score — compression damages verifiability faster than perceived quality.
- **H4:** Controller-enforced stopping reduces premature-stop failures more than step-budget-only stopping.

Pre-registration procedure: hypotheses written to `hypotheses.md` in the repo, Git-committed with the timestamp visible in the commit history, before the corresponding baseline or ablation run begins. This is a **cheap and high-signal move** (§0.5, §0.8).

### Retrieval metrics (enhanced from v4)

| Metric | What it answers | When it matters most |
|---|---|---|
| Precision@10 | Fraction of retrieved that are relevant | Precision-sensitive queries |
| Recall | Fraction of gold-relevant retrieved across full run | **Bounded corpora: critical** — miss is unrecoverable |
| F1 | Balance | Default headline |
| **MRR** (Mean Reciprocal Rank) | How early the first relevant chunk appears in top-10 | Agents read top chunks first; early placement matters |

MRR is added in v4.1 because agents under time/context pressure may only read the first 2–3 results thoroughly — where the first relevant chunk ranks is a better proxy for *agent-visible* retrieval quality than F1 alone.

### Adversarial retrieval probe (added in v4.1)

A small set (5–8 queries) designed to distinguish keyword-matching from semantic-matching. Construction:

- Select a gold chunk A containing the answer-relevant fact
- Identify similar chunks B, C in the corpus that share surface terms with A but do not contain the fact
- Write a query using B/C's language that can only be correctly answered from A

If retrieval returns B/C rather than A, the system is doing dumb term matching. This probe directly exposes whether hybrid retrieval's advantage over BM25 is real semantic grounding or just tokenization artifacts. Results reported as separate section in Week 8 writeup.

### Judge calibration protocol (new in v4.1, replaces single κ report)

Follows Hamel/Shreya methodology (§0.8):

1. Build a **calibration set** of 30–40 (trace, verdict) pairs hand-labeled by YS + wife (for TransGlobal judge) or YS alone (for Discover AI judge, acknowledged asymmetry).
2. Run the LLM judge on the calibration set; compute TPR and TNR.
3. Apply bias-correction formula to production pass rates.
4. Report bootstrap 95% CIs (1000 resamples) alongside point estimates.
5. Re-calibrate after any judge prompt change.

Reported in the Week 8 writeup as: *"Judge calibrated on n=35 samples; TPR = 0.89, TNR = 0.76; bias-corrected production pass rate = X% [95% CI: Y%, Z%]; judge parse-error rate = P%."*

This is the single strongest rigor-signal upgrade in v4.1. Takes ~2 days in Week 5; pays off in every number reported afterward.

### Controls

- Fixed corpus snapshots (SHA-256 checksummed manifests)
- Fixed gold sets (versioned in repo, no leakage to prompts)
- **Research recipe prompt versioned as `prompts/research_recipe.md` (v4.2);** identical across seeds and retrieval modes within A1; swapped only at ablation-level boundaries (A4 if run). Any change during an ablation invalidates that ablation.
- Fixed judge model (Claude Opus 4.7) with fixed judge prompt (calibrated separately)
- Fixed judge output schema (Pydantic `Literal` types, fail-biased fallback, v4.2)
- Temperature = 0 for planner
- **3 seeds minimum per ablation cell on TransGlobal; 1 seed on Discover AI probe**

### Statistical treatment

- Mean ± std across seeds
- Bootstrap 95% CIs for pass rates and calibrated metrics
- All seed runs reported (no cherry-picking)
- Honest null-result reporting: if a hypothesis is rejected, rejection is reported as-is
- Judge parse-error rate reported as a separate line item (v4.2)

### Reproducibility

- Gold sets in repo (committed before baseline runs)
- Eval configs in repo
- Corpus manifest (video IDs + content hashes) in repo
- Judge calibration set in repo
- Research recipe prompt in repo (v4.2)
- Pre-registration timestamps visible in Git history
- Transcripts on S3 (requestable; Discover AI members-only excluded and noted)
- One-command reproduction: `uv run eval --suite gold --channel transglobal --config configs/A1-hybrid.yaml`

---

## 7. Timeline (Calendar)

Starting **Monday, April 20, 2026**.

| Week | Dates | Phase | Primary milestone |
|---|---|---|---|
| 1 | Apr 20–26 | 0: Walking skeleton | Local end-to-end on 10 videos |
| 2 | Apr 27 – May 3 | 1: Ingestion + retrieval | Both corpora ingested; hybrid retrieval working |
| 3 | May 4–10 | 2: Agent + context eng | Baseline agent runs queries locally on both channels; research recipe + tool granularity locked |
| 4 | May 11–17 | 3: Frontend polish | Production-grade demo UI |
| 5 | May 18–24 | 4: Gold set + eval harness | Both gold sets locked; eval runner working; judge calibrated |
| 6 | Jun 1–7 | 5: AWS deployment | Live public URL |
| 7 | Jun 8–14 | 6: Baseline + A1 + synthesis | First production numbers; preliminary failure taxonomy |
| 8 | Jun 15–21 | 7: MVP writeup + launch | Portfolio artifacts published; outreach begins Week 9 |

**Interview readiness: end of June 21, 2026.** Week 22 post-layoff.

Week 9 onward: interview outreach in progress, Phases 8–14 deepen the work in parallel.

---

## 8. Open Decisions (Week 1 blockers)

| # | Decision | Needed by | Recommendation |
|---|---|---|---|
| D1 | Domain name | Apr 19 (before Phase 0) | Pick + buy this weekend |
| D2 | Total project budget cap (LLM + AWS + APIs) | Now | **$600** (reduced from v3's $1200 due to scope cuts). Track weekly. |
| D3 | TransGlobal snapshot window | Apr 27 (Phase 1 start) | **12 months.** Revisit if video count >400. |
| D4 | Discover AI members-only handling | Apr 27 | **Exclude, note in manifest.** Reproducibility > completeness. |
| D5 | Repo name | Apr 19 | **`bounded-deep-research`** (generic-first) |
| D6 | Transcript cleanup pass scope | Apr 27 | **Include for TransGlobal** (ticker/indicator cleanup). Optional for Discover AI (model name disambiguation). Re-decide after Day-2 Gemini ASR probe (v4.2). |
| D7 | Cognito allowlist: who else gets access? | Jun 1 (Phase 5) | You, wife, 2–3 named reviewers (Jerry Shen, Alexey Grigorev if he's willing, one former colleague). |
| D8 (v4.2) | Transcript pipeline: `youtube-transcript-api` + cleanup + Whisper fallback, or Gemini multimodal ASR? | Apr 22 (after Day-2 probe) | Default keeps v4.1 pipeline. If Day-2 Gemini probe shows notably better Chinese quality, swap for TransGlobal (Discover AI stays on auto-captions regardless). |

---

## 9. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Week 1 slip** | High | Phase 0 is the forcing function. If not met Friday Apr 24, stop and pair with Claude Code over weekend. No Phase 1 until skeleton runs. |
| **AWS rabbit hole Week 6** | High | Half-day cap per sub-problem. Terraform AWS modules, not hand-rolled. Simplify if stuck. |
| **Frontend rabbit hole Week 4** | Medium-High | 7-day cap. shadcn/ui defaults only. No custom design. |
| **Gold set slip Week 5** | Medium | Cap at 2 half-days for TransGlobal (with wife), 1 day for Discover AI. Ship with smaller set if needed. |
| **TransGlobal corpus size surprises** | Medium | Check Week 2 Day 1. If >400 videos, narrow to 9 months. |
| **Week 8 writeup eats more than 7 days** | Medium | Draft outline end of Week 7. Write sections 2–3 (system + method) before baseline results land. |
| **Chinese ASR quality worse than expected** | Low-Medium | YouTube auto-caps + cleanup pass. If persistent problem, Whisper API for specific problem videos (~$20 budget). Day-2 Gemini probe (v4.2) provides an early alternative data point. |
| **Judge-human κ low** | Medium | Report transparently as threat to validity. Increases scientific maturity signal. |
| **Cost overrun** | Medium | $600 cap with weekly tracking. Primary risk: LLM calls during eval runs. Mitigation: smaller gold sets first, scale only when baseline stable. |
| **Judge parse-error rate high (v4.2)** | Low | Fail-biased fallback keeps headline conservative; log rate; if >5%, re-examine judge prompt structure or switch to tool-calling mode instead of structured output. |
| **Research recipe prompt regression (v4.2)** | Low | Prompt is versioned; changes require explicit commit with justification; A1 cells run against a frozen prompt version. |
| **Interview starts before Week 8** | Low (you said project-first) | If a role appears, don't refuse — Week 5+ artifacts already defensible. |

---

## 10. Portfolio Narrative (Target, End of Week 8)

### Top-line (live demo + summary)

> **Live demo:** `[custom-domain]` — a bounded-corpus deep research agent operating across two structurally distinct video corpora: a Chinese financial advisory channel (TransGlobal, domain-expert evaluated) and an English AI research commentary channel (Discover AI, generalization probe).
>
> **System:** Full AWS deployment (Terraform), Next.js frontend on CloudFront+S3, FastAPI on ECS Fargate, scripted idempotent ingestion, hybrid retrieval (BM25 + dense + RRF) on OpenSearch Service, roll-own ReAct loop with controller-enforced stopping and a versioned research recipe prompt, Langfuse + CloudWatch observability, Cognito allowlist auth, GitHub Actions + OIDC CI/CD.
>
> **Evaluation:** Multi-layer framework grounded in six recent deep research benchmarks — retrieval P/R/F1/MRR, programmatic citation verification, rubric-based synthesis scoring with judge-human agreement reported. Pre-registered hypotheses. One ablation (retrieval mode) × 3 seeds on TransGlobal, with generalization probe on Discover AI. Preliminary failure taxonomy.
>
> **What transfers across corpora:** [finding from Week 7 generalization probe].

### Combined with Project A (the arc)

> "Project A diagnosed failure modes in an existing agent (mini-swe-agent on Terminal-Bench 2.0), identified wrong-layer verification as the dominant failure, and shipped a controller-level intervention (`VerifyingAgent`) with measured task flips. Project B designed, built, deployed, and studied a production deep research agent from scratch, applying the same rigor to its own harness decisions and extending to cross-language cross-domain generalization."

### Pitch variants by role target

| Target | Emphasis |
|---|---|
| Staff AI Scientist / Principal IC | The study, pre-registered hypotheses, judge-human agreement, failure taxonomy, connection to benchmark literature |
| Head of AI / Director | The full stack judgment, the arc from problem-definition → production, team-shaped execution done solo |
| Applied AI role (agent-focused) | The agent harness work, reliability engineering, cross-domain transferability |

### The subtractive-principle talking points

Reviewers will notice what's *not* in the stack. Each has a ready answer:

- **"Why not Temporal?"** → "Bounded one-time ingestion doesn't warrant durable workflow orchestration. Scripted pipeline with idempotency is sufficient. Temporal would be the right call at multi-channel continuously-ingesting tier."
- **"Why not self-hosted ASR?"** → "YouTube auto-captions are sufficient for both target corpora. Whisper API provides per-video fallback. Self-hosting would be infrastructure theater."
- **"Why not Sentry/custom cost dashboard?"** → "Langfuse + CloudWatch cover LLM + infra observability. Adding more SaaS was surface area without signal."
- **"Why not MCP?"** (v4.2) → "The agent's tools are called by a single client — my own FastAPI service. MCP buys portability across clients (IDEs, other agent frameworks, external programmatic callers), which isn't a requirement here. Adding MCP would be surface area without signal, and the equivalent design effort went into the versioned research recipe prompt and the gold set instead. If this were a multi-client tool library, MCP would be the right call."
- **"Why one ablation for Week 8?"** → "Financial runway prioritizes interview-readiness. Two more ablations ship in weeks 9–10, parallel with interviewing. This is the scope decision the constraints require."

**That last bullet is the key Principal-level talking point.** A candidate who names their scope-management reasoning explicitly is stronger than one who doesn't.

---

## 11. First-Week Checklist (Concrete, Non-Negotiable)

**Pre-work (this weekend, Apr 19–20):**
- [ ] Domain name purchased
- [ ] AWS account + billing alarm ($50/week threshold)
- [ ] Anthropic + OpenAI API keys stored in password manager
- [ ] GitHub repo created, initial commit
- [ ] Hypotheses H1 + H2 drafted (not final — committed to Git at end of Phase 4)

**Day 1 (Mon Apr 20):** Repo scaffold, uv env, Next.js 15 scaffold, docker-compose with Postgres + local OpenSearch + Langfuse. Smoke-test each.

**Day 2 (Tue Apr 21):** Hardcode 10 video IDs (5 TransGlobal, 5 Discover AI). `youtube-transcript-api` fetches → JSONL. Load to local OpenSearch with fixed-30s chunking. BM25 query works from Python REPL.

> **Also (v4.2): 2-hour Gemini 2.5 Flash multimodal ASR probe.** On 3 TransGlobal videos, pass the YouTube URL directly to Gemini with a transcription prompt and compare output to `youtube-transcript-api` auto-captions. If Gemini output is notably cleaner for Chinese financial content — fewer ticker-symbol errors, better punctuation, less cleanup-pass dependence — evaluate swapping the pipeline (see D8). Worst case: one option cheaply eliminated, which is still a win for the writeup ("we evaluated X and it didn't pan out" is a credible signal). Do NOT allow this probe to eat more than half a day; cap hard.

**Day 3 (Wed Apr 22):** FastAPI endpoint + minimal ReAct loop (2 tools: search, submit; 15-step budget). Answers one hardcoded query end-to-end. Langfuse traces visible. D8 decision made and logged.

**Day 4 (Thu Apr 23):** Next.js page wiring to FastAPI via SSE. Query input + streaming trace + citation cards. Click citation → opens YouTube at timestamp.

**Day 5 (Fri Apr 24):** Polish, screen-record for your own reference. Write Phase-0 retro. Commit to main.

**Phase 0 gate (Fri Apr 24 EOD):** `docker-compose up && pnpm dev` → type a query → see streaming answer with 3 clickable citations on both channels. Pass → Phase 1 unlocks Monday. Fail → weekend is for cutting scope until Phase 0 passes before Phase 1 starts.

---

## 12. What's NOT in the Plan (Intentional)

- Detailed prompts (write in-phase, version them — research recipe prompt is the one exception, committed Week 3)
- Exact OpenSearch mappings (Phase 1)
- Retry/backoff constants (Phase 1)
- Rubric wording (Phase 4 with wife)
- Judge prompt wording (Phase 4, versioned once)
- Terraform module layout (Phase 5)
- UI component design (Phase 3 — shadcn defaults)
- Chart styling (Phase 7)

These are in-phase decisions. Pre-deciding them is how plans become excuses.

---

## 13. Parallel-with-Interviewing Principles (Weeks 9–14)

When interviews start Week 9, some discipline needs to hold:

1. **Interview prep > project deepening** when they conflict. One great interview beats a better writeup.
2. **Record interview questions** about Project B. If three different hiring managers ask "how did you handle X?" — that's signal to add it to the writeup.
3. **Don't rewrite v8 architecture based on one interviewer's opinion.** Change requires pattern, not outlier.
4. **Workshop submission is optional.** If findings are interesting and a venue fits the timeline, submit. Otherwise skip.
5. **Protect ~15 focused hours/week for project** even during interview weeks. Morning or evening blocks.
6. **Full arXiv-style report is the goal, but MVP writeup is sufficient for most interviews.** Don't delay outreach waiting for the full report.

