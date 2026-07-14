<!-- ============================================================
STATUS AND PROVENANCE (added on check-in, 2026-07-14)
============================================================ -->

> **Status: pre-Task 7 external review.**
> Conducted by an external model (ChatGPT) on the frozen factual render (`eval/artifacts/factual_claimslice_sample.md`), on the **original wording**, and **without grounding or the flag set** (grounding, leak, anaphora, subject_in_gold, chunk_span).
>
> - Its **provisional final-20 slate is input to the Task 7 sitting, not a default.** Final selection still happens at the sitting, from the grounded + flagged review files.
> - Its **recommended wordings are UNGOVERNED rewrites**: none has passed the flag re-runs required by the rewrite-governance rule (cc_07 item b). Two are **known-defective** - `fc-0011`'s rewrite leaks the answer (via "shorter solution"), and `fc-0040`'s rewrite strips the only anchor. **The original wordings remain authoritative.**
>
> **Consistency with our records:**
> - Its drop list independently agrees with the standing **`fc-0022` drop** and flags **`fc-0004`'s unnamed benchmark** - consistent with our records.
> - Its **`fc-0009` strong-keep is the conscious reversal already logged** (composition build log, 2026-07-14); the review's reasoning ("targets a specific methodological-evidence claim fully supported by the selected gold") is the reversal rationale of record.
>
> Verdict vocabulary used below: **strong keep / keep / borderline / drop** (plus alternates).

<!-- ============================================================ -->

# AnswerTrail Phase 4: Review of All Factual Candidates

**Review date:** 2026-07-14  
**Source reviewed:** `factual_claimslice_sample.md`  
**Scope:** 50 factual candidates from Task 4

## Review standard

Each candidate is judged against its **selected claim only**. I do not use neighboring claims to repair missing context or expand the intended answer.

The main tests are:

1. **Gold fit:** Does the selected claim answer every part of the question?
2. **Standalone anchoring:** Can a user or librarian identify the intended paper, system, experiment, or result from the question?
3. **User naturalness:** Could a normal watcher or practitioner plausibly ask it?
4. **Final-20 value:** Is it worth one of only 20 factual slots, considering topic diversity and answer richness?
5. **No repair by neighboring claims:** If the selected claim lacks the anchor or answer, the default is to drop rather than reconstruct the question.

This is a **pre-Task 7 review**. Grounding, `subject_in_gold`, anaphora, leakage, and chunk-span flags may still change the final selection.

## Overall assessment

The run is successful. It produced a comfortable surplus of strong candidates, so there is no need to rescue weak or underanchored questions. The main failure modes are:

- selected claims that describe an experiment but do not contain the requested finding;
- unnamed papers, benchmarks, or systems that make questions underdetermined;
- questions that ask “why” when the claim only reports “what”;
- meta or future-plan questions;
- overly narrow worked-example details;
- questions that reveal part of their own answer.

## Provisional final 20

This list intentionally uses **four candidates from each temporal stratum**. It is a starting point, not a substitute for the Task 7 review files.

- **fc-0001:** ReasonFlux institutions and release date
- **fc-0002:** Autonomy of Experts router alternative
- **fc-0005:** Anthropic think tool on tau-bench
- **fc-0007:** MinionS performance and cost
- **fc-0011:** o4-mini Pareto-optimality claim
- **fc-0012:** Abstention on missing-data questions
- **fc-0015:** Off-policy traces and entropy collapse
- **fc-0020:** Deep Retrieval publication-search recall
- **fc-0023:** GeARs triple-link step
- **fc-0026:** Deep-DxSearch versus DeepSeek R1
- **fc-0029:** Grok 4 elevator mistake
- **fc-0030:** Feedback quality in textual-gradient methods
- **fc-0031:** Rank-one ICL update
- **fc-0033:** Nemotron Elastic uniform budget sampling
- **fc-0038:** VLM4VA benchmark-to-robot correlation
- **fc-0040:** Knee MRI dataset size
- **fc-0041:** GPT-5.2 versus local 14B at five hops
- **fc-0043:** ALOE intrinsic reward
- **fc-0045:** Multi-agent consensus-time scaling
- **fc-0048:** Asymmetric prediction paradox accuracy

## Strong alternates

- **fc-0006:** AutoGen reliance on a generalist model
- **fc-0009:** L1 evidence for different reasoning strategies
- **fc-0010:** REMA average improvement
- **fc-0016:** GPDiT attention mechanism
- **fc-0017:** Laser-fusion scientific automation system
- **fc-0019:** HRM deep supervision
- **fc-0021:** GPT-OSS-120B elevator result
- **fc-0024:** LSD-3D versus competing driving-scene methods
- **fc-0032:** Gemini 3 Deep Think ARC-AGI-2 score
- **fc-0037:** t-SNE and a supposed continuous manifold
- **fc-0047:** KARL cost versus benchmark performance
- **fc-0050:** Kimi K2.5 parallel multi-agent conditions

## Per-candidate review

### fc-0001: ReasonFlux institutions and release date

**Question:** Which universities published ReasonFlux, and when did the paper come out?

**Decision:** STRONG KEEP after a light rewrite

**Gold fit:** Complete. The selected claim contains both institutions and the date.

**Opinion:** Clear, accessible, and well anchored by the ReasonFlux name. The only issue is technical wording: universities were behind the work, but saying they “published” the paper may imply they were the formal publisher.

**Recommended wording:** Which institutions were behind the ReasonFlux paper, and when was it released?

**Provisional final-20 status:** Yes

### fc-0002: Autonomy of Experts router alternative

**Question:** In the Autonomy of Experts (AoE) paper for mixture-of-experts models, what alternative do the authors propose to using a traditional router?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The selected claim directly and completely answers the mechanism question.

**Opinion:** One of the cleanest candidates in the run. It names the paper, asks one focused technical question, and has a concise, substantive answer.

**Recommended wording:** In the Autonomy-of-Experts paper, what do the authors propose instead of a traditional mixture-of-experts router?

**Provisional final-20 status:** Yes

### fc-0003: Dialogue tuning across difficulty levels

**Question:** How does dialogue tuning affect reasoning performance across basic, advanced, and challenging difficulty levels compared to other forms of training data?

**Decision:** DROP

**Gold fit:** Technically complete, but shallow: it only says dialogue tuning improves performance at all three levels.

**Opinion:** The question is not sufficiently anchored. It names neither the paper, the medical domain, nor the benchmark. Adding those identifiers would require borrowing from neighboring claims, which is outside the selected-claim-only rule.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0004: Qwen 2.5 versus Stanford s1 scores

**Question:** On a benchmark comparing Qwen 2.5 to Stanford's S1 model trained with Gemini 2.0-improved reasoning data, how did the scores break down between Qwen 2.5, S1 without its test-time compute algorithm, and S1 with the algorithm activated?

**Decision:** BORDERLINE, probably do not select

**Gold fit:** Complete for the three reported numbers.

**Opinion:** The numerical comparison is meaningful, but the benchmark is unnamed. “On a benchmark” is not a real anchor, and there is no safe way to add the benchmark name from the selected claim alone. The question is also long and asks for three conditions at once.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No, unless Task 7 shows that the question remains uniquely retrievable and the benchmark ambiguity is harmless

### fc-0005: Anthropic think tool on tau-bench

**Question:** How much did the 'think' tool improve performance when Anthropic added it to Claude Sonnet 3.7 on tau-bench, given that the same idea reportedly failed to help a year earlier?

**Decision:** STRONG KEEP

**Gold fit:** Complete under the selected claim: more than a 50% improvement, contrasted with the earlier failed attempt.

**Opinion:** Memorable, natural, and useful. The original wording is better than a more technically elaborate rewrite. Do not import the nearby prompt-optimization qualification into the question because it is not part of the selected claim.

**Recommended wording:** How much did Anthropic’s “think” tool improve Claude Sonnet 3.7 on tau-bench, given that a similar idea had failed a year earlier?

**Provisional final-20 status:** Yes

### fc-0006: AutoGen reliance on a generalist model

**Question:** According to a Stanford study on agent frameworks, how often does Microsoft's AutoGen rely on a generalist single LLM/VLM approach rather than invoking other tools?

**Decision:** KEEP

**Gold fit:** Complete. The selected claim gives the approximately 90% rate and the interpretation that other tools are rarely used.

**Opinion:** A useful agent-framework finding. “A Stanford study” is somewhat broad, but AutoGen, the generalist LLM/VLM behavior, and the requested percentage make the question specific enough.

**Recommended wording:** According to the Stanford study, how often did AutoGen rely on a generalist LLM or VLM instead of using specialized tools?

**Provisional final-20 status:** Alternate

### fc-0007: MinionS performance and cost

**Question:** What did Stanford's research on MinionS find regarding performance and cost when using an 8 billion parameter local LLM compared to relying solely on remote cloud LLMs?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. Both the performance recovery and cost ratio are explicit.

**Opinion:** Highly practical and user-natural. It captures the main tradeoff of the research in one question and is one of the strongest headline findings in the set.

**Recommended wording:** With an 8B local LLM, what performance and cost did MinionS achieve compared with using a remote cloud LLM alone?

**Provisional final-20 status:** Yes

### fc-0008: Agentic reasoning on a PhD-level benchmark

**Question:** How did the 'agentic reasoning' approach compare to the other models or modes tested on a PhD-level benchmark?

**Decision:** DROP

**Gold fit:** Complete only at a very general level: the method performed best.

**Opinion:** Both the method label and benchmark are vague. The answer is also little more than “it was best.” The question sounds source-dependent rather than like a standalone user query.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0009: L1 evidence for different reasoning strategies

**Question:** What kind of evidence does the L1 paper present to support the claim that models use distinct reasoning strategies at different response lengths?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The selected claim identifies the exact evidence: frequency differences for “therefore” and “so.”

**Opinion:** Specific, surprising, and useful for evaluating the strength of a paper’s evidence. It encourages retrieval of a methodological detail rather than merely a headline score.

**Recommended wording:** What evidence does the L1 paper give that models use different reasoning strategies at different response lengths?

**Provisional final-20 status:** Yes

### fc-0010: REMA average improvement

**Question:** On average across benchmark scenarios, how much did REMA's multi-agent meta-thinking training improve performance over the baseline approaches?

**Decision:** KEEP

**Gold fit:** Complete. Baselines were about 50–51%, and REMA reached about 53%.

**Opinion:** A clean numerical question with a named method. It is useful, although less distinctive than several stronger candidates because the improvement is simply a small aggregate score change.

**Recommended wording:** Across the tested benchmarks, how much did REMA improve average performance over the baselines?

**Provisional final-20 status:** Alternate

### fc-0011: o4-mini Pareto-optimality claim

**Question:** In an elevator puzzle test, o4-mini claimed its 20-step solution was Pareto optimal with no strictly shorter sequence possible - was that claim actually correct, especially compared to Gemini 2.5 Pro's solution?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The selected claim directly establishes that the claim was false because Gemini found a 10-step solution.

**Opinion:** Very natural for a watcher of the channel and strong as a reliability question. It asks the system to check a model’s confident self-evaluation against contradictory evidence.

**Recommended wording:** In the elevator puzzle, was o4-mini correct to call its 20-step solution Pareto optimal, especially given Gemini 2.5 Pro’s shorter solution?

**Provisional final-20 status:** Yes

### fc-0012: Abstention on missing-data questions

**Question:** On missing-data questions where the correct answer is to admit data isn't available, how do abstain rates compare between reasoning models like QwQ, Stanford S1, DeepSeek, and o3-mini versus non-reasoning models?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. All model rates and the non-reasoning comparison are included.

**Opinion:** A strong reliability and evaluation question. It is clearly motivated, quantitatively rich, and directly useful for understanding a counterintuitive weakness of reasoning models.

**Recommended wording:** On questions with missing information, how did the abstention rates of QwQ, s1, DeepSeek, and o3-mini compare with non-reasoning models?

**Provisional final-20 status:** Yes

### fc-0013: SFT dataset scaling from 20,000 to 1 million samples

**Question:** How does performance change as the supervised fine-tuning dataset size increases from 20,000 samples to 1 million samples?

**Decision:** DROP

**Gold fit:** Complete for the scaling figures.

**Opinion:** The question lacks a paper, model, task, or benchmark anchor. Many studies could contain an SFT scaling experiment. There is no safe selected-claim-only rewrite that makes it uniquely identifiable.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0014: CPT alone versus CPT plus additional optimization

**Question:** How does continuous pre-training (CPT) alone compare to CPT combined with additional optimization methods in terms of cost, speed, and performance gain (e.g., moving accuracy from 80% to 86.7%)?

**Decision:** BORDERLINE

**Gold fit:** Complete. The claim covers cost, speed, the 80% to 86.7% gain, and the extra 0.1 point.

**Opinion:** The result is interesting, but the experiment and system are unnamed. The question is also overloaded with cost, speed, and two performance comparisons. It can work as a channel-specific detail query, but it is not among the best final-core questions.

**Recommended wording:** How did continuous pre-training alone compare with CPT plus additional optimization in cost, speed, and performance?

**Provisional final-20 status:** No, unless a broader training-method mix is needed

### fc-0015: Off-policy traces and entropy collapse

**Question:** What happens to entropy and reasoning quality when off-policy traces are naively combined with on-policy learning during training?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It gives both the entropy effect and the resulting degradation in reasoning.

**Opinion:** A strong conceptual training-dynamics question. The technical phenomenon is specific enough to stand alone even without a paper name, and the selected claim provides a meaningful causal answer.

**Recommended wording:** What happens to entropy and reasoning quality when off-policy traces are naively mixed with on-policy learning?

**Provisional final-20 status:** Yes

### fc-0016: GPDiT attention mechanism

**Question:** What kind of new attention mechanism does GPDiT introduce to reduce computational cost?

**Decision:** KEEP

**Gold fit:** Complete, but thin: the answer is simply a lightweight causal attention mechanism.

**Opinion:** Very clean and well anchored by GPDiT. Its weakness is low answer richness; the question may be too easy and almost definitional.

**Recommended wording:** What attention mechanism does GPDiT introduce to reduce computational cost?

**Provisional final-20 status:** Alternate

### fc-0017: Laser-fusion scientific automation system

**Question:** In the context of an AI system built for laser fusion experiments, what is it actually designed to do if its purpose goes beyond just writing code?

**Decision:** BORDERLINE

**Gold fit:** Excellent. The selected claim gives a rich description of the full scientific-method loop.

**Opinion:** The answer is substantive and interesting, but the system is unnamed. “An AI system built for laser fusion experiments” may still be enough for a watcher to recognize it, yet it is weaker than candidates with a stable paper or system name.

**Recommended wording:** What is the laser-fusion AI system designed to automate beyond simply writing code?

**Provisional final-20 status:** Alternate

### fc-0018: Asymmetric code-evaluation test

**Question:** In a code evaluation setup where the one correct ('ground truth') code snippet was stripped down to plain text while all the incorrect candidate snippets kept their original well-documented, nicely formatted code and explanations, what did this asymmetric test reveal?

**Decision:** DROP because the gold does not answer the question

**Gold fit:** Insufficient. The selected claim only describes the experimental setup; it does not state what the test revealed.

**Opinion:** This is the clearest gold-to-question failure in the set. A correct answer would have to borrow the finding from neighboring claims, while the judge is supposed to score against the selected claim.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0019: HRM deep supervision

**Question:** How does the Hierarchical Reasoning Model (HRM) use deep supervision, breaking training into segments with loss computed at multiple depths, to address long-horizon training instability?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The mechanism and its purpose are both explicit.

**Opinion:** Well anchored, technically substantive, and directly answerable. The current wording is slightly leading because it explains much of the mechanism before asking how it works, but it remains a strong candidate.

**Recommended wording:** How does HRM use deep supervision to reduce long-horizon training instability?

**Provisional final-20 status:** Yes

### fc-0020: Deep Retrieval publication-search recall

**Question:** What recall rate did Deep Retrieval achieve on publication search compared to the state-of-the-art method?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It supplies both Deep Retrieval’s 65% recall and the 24% state of the art.

**Opinion:** A concise and useful benchmark question with a named method and a clear comparison. It is suitable as a straightforward numerical item in the final mix.

**Recommended wording:** What publication-search recall did Deep Retrieval achieve, and how did it compare with the previous state of the art?

**Provisional final-20 status:** Yes

### fc-0021: GPT-OSS-120B elevator result

**Question:** How many button presses did GPT-OSS-120B use in its solution to the elevator causal reasoning test?

**Decision:** KEEP

**Gold fit:** Complete. The answer is 15 presses.

**Opinion:** Clean and natural for a channel watcher, but it is a narrow detail question. Since the corpus contains many elevator-test videos, the final factual set should avoid overrepresenting this family.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** Alternate

### fc-0022: Opus 4.1 versus Sonnet 4.5 cited scores

**Question:** What scores were reported for Opus 4.1 16k thinking versus Sonnet 4.5 on a benchmark comparison cited by the creator?

**Decision:** DROP

**Gold fit:** Contains the two numbers, but the benchmark is unnamed.

**Opinion:** This is already a standing human-drop. “Cited by the creator” is a meta-reference, the benchmark is unspecified, and the model/version wording carries high transcription risk.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0023: GeARs triple-link step

**Question:** In the GeARs architecture, what happens during the 'triple link' step where each proximal triple is used as a search query against a large external knowledge graph like Wikidata?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It fully describes the search and canonical-triple linking process.

**Opinion:** A strong architecture-process question. It names the system and operation and asks for one concrete step that has a substantive answer.

**Recommended wording:** In GeARs, what happens during the “triple link” step against an external knowledge graph such as Wikidata?

**Provisional final-20 status:** Yes

### fc-0024: LSD-3D versus competing driving-scene methods

**Question:** How does LSD-3D compare to methods like Gaussian splatting scenes (3C) and MagicDrive 3D when generating novel driving trajectories?

**Decision:** KEEP

**Gold fit:** Complete. It states LSD-3D outperformed the named methods and explains their consistency and plausibility problem.

**Opinion:** Well anchored and substantive, though somewhat specialized. It is a valid candidate if the final set should include a vision or world-model result.

**Recommended wording:** How did LSD-3D compare with 3C and MagicDrive3D when generating novel driving trajectories?

**Provisional final-20 status:** Alternate

### fc-0025: Qwen3 non-thinking puzzle result and future plan

**Question:** Was Qwen3 235B, running at maximum non-thinking effort, able to reliably solve the causal reasoning puzzle, and is a comparison planned once the thinking variant of the new Qwen3 is available?

**Decision:** DROP

**Gold fit:** Complete for both parts.

**Opinion:** The question combines a model result with the creator’s future testing plan. The second half is meta and time-sensitive, making the item less useful as durable core gold.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0026: Deep-DxSearch versus DeepSeek R1

**Question:** How does the 14B Deep-DxSearch model compare in performance to the much larger 671B DeepSeek R1 system on common versus rare disease diagnosis tasks?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It gives separate margins for common and rare diseases.

**Opinion:** One of the best comparative facts in the factual tier. It is surprising, practical, well anchored, and has a compact but information-rich answer.

**Recommended wording:** How did the 14B Deep-DxSearch model compare with the 671B DeepSeek R1 system on common and rare disease diagnosis?

**Provisional final-20 status:** Yes

### fc-0027: Duncan experiment thought experiment

**Question:** What is the 'Duncan experiment' thought experiment about testing whether an LLM's world model can predict the deflection angle of water hitting a newly invented object with novel angles it has never seen described in pretraining data?

**Decision:** DROP

**Gold fit:** Complete, but the question nearly restates the entire claim.

**Opinion:** The wording is long, the term may be creator-specific, and there is little left for the answer beyond repeating the premise. It is more suitable for discussion than factual retrieval.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0028: Agent-matchmaking worked-example detail

**Question:** In a paper's worked example on agent matchmaking with a pool of 100 agents, cosine similarity is used to match agent self-descriptions to subtasks - which agent was identified as the best fit for subtask one, and what was its similarity score?

**Decision:** DROP

**Gold fit:** Complete. Agent D scored 0.73.

**Opinion:** Answerable but arbitrary. It tests retrieval of a very narrow worked-example detail without teaching much about the method. With only 20 slots, stronger questions should take priority.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0029: Grok 4 elevator mistake

**Question:** What mistake did Grok 4 make in an elevator puzzle involving a 50-floor building, where it moved the elevator to floor 52 and then capped it at floor 50?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The precise invalid assumption is stated.

**Opinion:** Natural, concrete, and memorable. It tests retrieval of a model failure rather than merely a score. Keep only one or two elevator questions overall to preserve topic diversity.

**Recommended wording:** What mistake did Grok 4 make in the 50-floor elevator puzzle when it moved the elevator to floor 52?

**Provisional final-20 status:** Yes

### fc-0030: Feedback quality in textual-gradient methods

**Question:** Why does feedback quality matter so much in textual gradient methods, and why would using a small LLM such as a 1.5 billion parameter model likely cause unstable updates?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It explains both dependence on LLM diagnostics and the instability risk from a small model.

**Opinion:** A useful conceptual-method question with a clear causal answer. It is understandable without requiring the paper name.

**Recommended wording:** Why is feedback quality critical in textual-gradient methods, and why can a small 1.5B model make the updates unstable?

**Provisional final-20 status:** Yes

### fc-0031: Rank-one ICL update

**Question:** How does the rank of the weight update differ between standard fine-tuning and in-context learning (ICL), and why does this make ICL's update fast, temporary, and specific to the current token position?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It fully contrasts full-matrix fine-tuning with rank-one ICL and states the consequences.

**Opinion:** One of the strongest technical questions in the run. It is specific, conceptually important, and answerable from a single dense claim.

**Recommended wording:** How does the update rank differ between standard fine-tuning and in-context learning, and why does that make ICL fast and temporary?

**Provisional final-20 status:** Yes

### fc-0032: Gemini 3 Deep Think ARC-AGI-2 score

**Question:** What score did Gemini 3 Deep Think achieve on the ARC-AGI-2 benchmark?

**Decision:** KEEP

**Gold fit:** Complete. The answer is 45%.

**Opinion:** Very clean but extremely simple. It is useful as an easy factual item if the exact model name survives grounding, but it is not as informative as the stronger conceptual and failure-analysis questions.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** Alternate

### fc-0033: Nemotron Elastic uniform budget sampling

**Question:** In Nemotron Elastic's multi-size training setup with 6B, 9B, and 12B models, what went wrong when the training budget was sampled uniformly across the three sizes?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It names the gradient-interference failure and its effect on the 12B model.

**Opinion:** A strong method-detail question with a surprising and specific answer. It is well anchored and useful for understanding multi-size training.

**Recommended wording:** In Nemotron Elastic’s 6B, 9B, and 12B setup, what went wrong when the training budget was sampled uniformly across model sizes?

**Provisional final-20 status:** Yes

### fc-0034: Opposing concepts across a hyperplane

**Question:** Why do trained models place opposing concepts, like multiplication and addition, on opposite sides of a hyperplane in high-dimensional space?

**Decision:** BORDERLINE

**Gold fit:** Adequate. It says the arrangement is an efficient way to organize information.

**Opinion:** The question is understandable, but it is underanchored and its “why” answer is fairly generic. It risks sounding like an unsupported universal claim rather than a finding from a particular analysis.

**Recommended wording:** Why does the creator say a trained model may place opposing concepts on opposite sides of a high-dimensional hyperplane?

**Provisional final-20 status:** No

### fc-0035: SRL average improvement

**Question:** On average across the benchmarks tested, how much did SRL improve performance compared to classical reinforcement learning?

**Decision:** DROP

**Gold fit:** Complete for the numbers.

**Opinion:** SRL is not expanded or otherwise identified in the selected claim. The question is therefore not standalone, and there is no safe way to repair it without neighboring information.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0036: Equilibrium Matching

**Question:** What is 'equilibrium matching,' the technique developed by researchers from MIT, Oxford, and Harvard, and how does it bridge two different model architecture paradigms?

**Decision:** DROP because the gold is insufficient

**Gold fit:** Insufficient. The claim calls it a bridge between two architecture “kingdoms” but does not identify those paradigms or explain the bridge.

**Opinion:** The question asks both what the technique is and how it connects two paradigms. The selected claim cannot support a substantive answer to either part.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0037: t-SNE and a supposed continuous manifold

**Question:** Why might a t-SNE plot showing a supposed continuous manifold be misleading when the original data lives in roughly 896-dimensional space?

**Decision:** KEEP

**Gold fit:** Complete as a creator assessment. It gives the dimensionality-compression concern and the visually mixed result.

**Opinion:** A useful visualization-skepticism question. It is explicitly the creator’s judgment rather than an objective benchmark finding, so it should be used sparingly among more empirical items.

**Recommended wording:** Why did the creator question whether the t-SNE plot really demonstrated a continuous manifold from roughly 896-dimensional data?

**Provisional final-20 status:** Alternate

### fc-0038: VLM4VA benchmark-to-robot correlation

**Question:** What did the VLM4VA paper's ablation study find about the correlation between a vision-language model's performance on standard visual question-answering benchmarks and its success rate in robotic manipulation tasks?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. The selected claim states zero correlation and identifies both evaluation domains.

**Opinion:** A highly valuable evaluation-validity question. It captures a clear, consequential finding that a practitioner could plausibly want to retrieve.

**Recommended wording:** What did VLM4VA find about whether standard VQA benchmark performance predicts robotic-manipulation success?

**Provisional final-20 status:** Yes

### fc-0039: Reasoning data during pre-training

**Question:** According to Nvidia's research on injecting reasoning data during pre-training, why can't supervised fine-tuning combined with reinforcement learning fully recover the performance gains achieved by that approach?

**Decision:** DROP because the question asks for an unsupported explanation

**Gold fit:** Partial. It establishes that SFT plus RL does not fully recover the gain, but it does not explain why.

**Opinion:** The current “why can’t” wording requires a causal explanation absent from the selected claim. A descriptive question could be supported, but changing it would materially alter the candidate.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0040: Knee MRI dataset size

**Question:** Approximately how many high-quality quintuples and how many 3D knee MRI volumes make up the dataset built by researchers affiliated with Harvard Medical School?

**Decision:** KEEP

**Gold fit:** Excellent. Both quantities are explicit.

**Opinion:** A precise, well-formed detail-retrieval question. It is narrow, but that can be useful for balancing a set otherwise dominated by headline findings and conceptual questions.

**Recommended wording:** Approximately how many high-quality quintuples and 3D knee MRI volumes were in the dataset?

**Provisional final-20 status:** Yes in the provisional balanced set

### fc-0041: GPT-5.2 versus local 14B at five hops

**Question:** At five reasoning hops, how do GPT-5.2's accuracy and a locally trained 14B-parameter model's accuracy compare?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. Both accuracies and the 20-point difference are explicit.

**Opinion:** Clear, surprising, and naturally phrased. It is a strong benchmark-comparison item as long as the local model is uniquely identifiable from the source context during grounding.

**Recommended wording:** At five reasoning hops, how did GPT-5.2’s accuracy compare with the locally trained 14B model?

**Provisional final-20 status:** Yes

### fc-0042: Qwen 3.5 elevator result

**Question:** How many button presses did Qwen 3.5 397B-A17B end up using to solve the elevator puzzle, and was that considered a good result?

**Decision:** BORDERLINE pending Task 7

**Gold fit:** Complete at the claim level: 19 presses and judged not good.

**Opinion:** The question is natural for a watcher, but this is the known subject-in-gold risk: the grounded chunks may contain the result without naming Qwen. The exact model name is also complex. Retain as a possible loop-bridging probe, not a clean-core first choice.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No for the clean provisional 20; possible deliberate probe

### fc-0043: ALOE intrinsic reward

**Question:** How does ALOE's intrinsic reward function work, and why does it rely on eigenvectors of a state graph rather than a simple error signal?

**Decision:** STRONG KEEP, subject to entity verification in grounding

**Gold fit:** Excellent. It explains the topological diffusion framing, eigenvectors, and the reward objective.

**Opinion:** A technically rich mechanism question whose selected claim fully answers both parts. The acronym is potentially ambiguous in the wider literature, but within the corpus the claim itself is coherent.

**Recommended wording:** How does ALOE define its intrinsic reward using eigenvectors of the state graph, and how does that differ from a simple error signal?

**Provisional final-20 status:** Yes

### fc-0044: Country-to-capital geometric discontinuity

**Question:** In few-shot Q&A examples like 'France->Paris' and 'Japan->Tokyo', why does the geometric transition from country to capital appear as a discontinuity rather than a straight line?

**Decision:** BORDERLINE

**Gold fit:** Adequate. It attributes the discontinuity to a different nonlinear geometric mechanism.

**Opinion:** The example makes the question self-contained, but the answer is somewhat circular: it is discontinuous because the model uses a nonlinear jump. The claim does not explain that mechanism further.

**Recommended wording:** Why does the country-to-capital transition in examples such as France → Paris appear as a discontinuity rather than a straight path?

**Provisional final-20 status:** No

### fc-0045: Multi-agent consensus-time scaling

**Question:** In a multi-agent system, how does the time required to reach consensus scale with population size, message bandwidth M, and the adaptation rate alpha?

**Decision:** STRONG KEEP

**Gold fit:** Excellent. It supplies all three scaling relationships.

**Opinion:** A precise technical question with a compact, multi-part answer. It is demanding without being underdetermined and adds mathematical diversity to the set.

**Recommended wording:** How does consensus time scale with population size, message bandwidth M, and adaptation rate alpha in the paper’s multi-agent model?

**Provisional final-20 status:** Yes

### fc-0046: Similarity-based thinking versus explicit logic

**Question:** Why does converting human similarity-based thinking (dot products of dense vectors) into explicit logical structures like DAGs and trees, with defined state transitions and causality, lose some of the complexity and beauty of human language?

**Decision:** DROP

**Gold fit:** Complete as a creator viewpoint.

**Opinion:** The question is long, closely mirrors the claim, and asks for a philosophical interpretation rather than a clearly evaluable research finding. It is lower value than the other candidates.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0047: KARL cost versus benchmark performance

**Question:** On a cost-per-query versus benchmark-score chart, how does KARL's pricing compare to models like GPT 5.2, Opus 4.5, and Opus 4.6, given that it reportedly matches Opus 4.6's performance?

**Decision:** KEEP after rewriting

**Gold fit:** Excellent. It contains both the cost comparison and performance parity with Opus 4.6.

**Opinion:** The practical cost/performance axis is strong. The current question gives away part of the answer and assumes the user already knows KARL. A simpler comparison question is more natural, although KARL remains a specialist entity.

**Recommended wording:** How did KARL compare with GPT-5.2, Opus 4.5, and Opus 4.6 on the cost-per-query versus benchmark-score chart?

**Provisional final-20 status:** Alternate

### fc-0048: Asymmetric prediction paradox accuracy

**Question:** In the 'asymmetric prediction paradox' finding, what accuracy did an auto-rater achieve when predicting honest ('label A') outcomes from the reasoning traces of a Gemma 27B model?

**Decision:** KEEP

**Gold fit:** Excellent. The answer is 97%.

**Opinion:** A precise and fully anchored corpus-specific detail. It is narrower and less user-natural than the headline findings, but it provides useful difficulty and detail diversity.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** Yes in the provisional balanced set

### fc-0049: Seed workflow results

**Question:** When the seed workflow was tested on a set of 100 problems, what results came back in terms of accuracy, token cost, and time taken, and where did it struggle?

**Decision:** DROP

**Gold fit:** Excellent for all requested metrics and the failure mode.

**Opinion:** The problem is not answerability but anchoring. “The seed workflow” does not identify the framework or paper, and the question asks for four separate details. Adding a real identifier would require a neighboring claim.

**Recommended wording:** No safe or worthwhile rewrite under the selected-claim-only rule.

**Provisional final-20 status:** No

### fc-0050: Kimi K2.5 parallel multi-agent conditions

**Question:** In a parallel multi-agent setup, what two conditions determine whether the approach fails versus whether success then hinges on Kimi K2.5's ability to summarize sub-results into a coherent final answer?

**Decision:** KEEP after simplifying

**Gold fit:** Excellent. Both the failure and success conditions are explicit.

**Opinion:** The underlying distinction is useful, but the current sentence is difficult to parse and is a creator assessment rather than an experimental finding. It is a solid alternate rather than an automatic final selection.

**Recommended wording:** When would Kimi K2.5’s parallel multi-agent approach fail, and when would the result depend on its ability to synthesize the sub-results?

**Provisional final-20 status:** Alternate

## Decision summary

- **Strong keep:** 20
- **Keep:** 11
- **Borderline:** 6
- **Drop:** 13

## Candidates I would drop before final selection

- **fc-0003:** Dialogue tuning across difficulty levels
- **fc-0008:** Agentic reasoning on a PhD-level benchmark
- **fc-0013:** SFT dataset scaling from 20,000 to 1 million samples
- **fc-0018:** Asymmetric code-evaluation test
- **fc-0022:** Opus 4.1 versus Sonnet 4.5 cited scores
- **fc-0025:** Qwen3 non-thinking puzzle result and future plan
- **fc-0027:** Duncan experiment thought experiment
- **fc-0028:** Agent-matchmaking worked-example detail
- **fc-0035:** SRL average improvement
- **fc-0036:** Equilibrium Matching
- **fc-0039:** Reasoning data during pre-training
- **fc-0046:** Similarity-based thinking versus explicit logic
- **fc-0049:** Seed workflow results

## Final selection guidance after Task 7

When the grounded review file is available:

1. Remove any candidate whose gold chunks do not independently support the selected claim.
2. Prefer `subject_in_gold=full`, while deliberately retaining only a small number of partial/none cases as loop-bridging probes.
3. Recheck `fc-0042` specifically for the known Qwen-subject omission.
4. Preserve a mix of headline findings, mechanisms, failures, and narrow details.
5. Avoid selecting more than one or two elevator-puzzle questions.
6. Replace any provisional selection that develops a grounding or entity problem with the strongest alternate from the same temporal stratum.

## Bottom line

Task 4 generated a credible factual candidate pool. The strongest questions are already sufficient for a balanced final 20. The most important human-selection rule is not merely “can nearby transcript chunks answer this?” It is: **does the selected claim itself completely support the exact question, and is the question identifiable and natural without hidden source context?**
