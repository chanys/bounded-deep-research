# Factual gold - factual-gold-v1.0 (25 questions, 53 nuggets)

Frozen approved generation. Model claude-sonnet-5, extract prompt_sha `910a6696`, entailment-audit prompt_sha `ddfc49a9`.

This artifact is the frozen generation itself, not a regenerable output: LLM extraction is non-deterministic, so re-running the prompt would not reproduce it.

## Nugget-count distribution

- 1 nugget(s): 7 question(s)
- 2 nugget(s): 10 question(s)
- 3 nugget(s): 7 question(s)
- 5 nugget(s): 1 question(s)

## Applied freeze edits

- DROP fc-0036: 0 nuggets after subtraction (plan zero-nugget rule); question/claim overlap, 25th instance the skips pass missed; its 3 A2 runs go unused at scoring
- CUT fc-0009 nugget 1: entailed by another nugget (entailment audit true positive)

---

## fc-0001  (3 nuggets)

**question:** Which universities published ReasonFlux, and when did the paper come out?

**claim:** The creator states that Princeton University and Peking University already implemented this exact approach, publishing it on February 10th, 2025, calling it ReasonFlux.

**nuggets:**
1. ReasonFlux was published by Princeton University.
2. ReasonFlux was published by Peking University.
3. ReasonFlux was published on February 10th, 2025.

---

## fc-0002  (3 nuggets)

**question:** In the Autonomy of Experts (AoE) paper for mixture-of-experts models, what alternative do the authors propose to using a traditional router?

**claim:** The Autonomy of Experts paper proposes removing the router entirely, having experts pre-compute internal activation functions for the input and rank themselves based on activation norms.

**nuggets:**
1. The router is removed entirely.
2. Experts pre-compute internal activations for the input.
3. Experts rank themselves based on activation norms.

---

## fc-0004  (3 nuggets)

**question:** On a benchmark comparing Qwen 2.5 to Stanford's S1 model trained with Gemini 2.0-improved reasoning data, how did the scores break down between Qwen 2.5, S1 without its test-time compute algorithm, and S1 with the algorithm activated?

**claim:** On one benchmark, Qwen 2.5 scored about 26.7%, while S1 with Gemini 2.0-improved reasoning data (without the test-time algorithm) scored nearly 50%, and activating the test-time compute algorithm added another 6.7 percentage points.

**nuggets:**
1. Qwen 2.5 scored about 26.7% on the benchmark.
2. S1 without the test-time algorithm scored nearly 50% on the benchmark.
3. Activating the test-time compute algorithm added another 6.7 percentage points.

---

## fc-0005  (1 nuggets)

**question:** How much did the 'think' tool improve performance when Anthropic added it to Claude Sonnet 3.7 on tau-bench, given that the same idea reportedly failed to help a year earlier?

**claim:** The creator finds it fascinating that the same think-function idea that failed to help a year ago in tau-bench now produces more than a 50% performance increase when Anthropic added it to Sonnet 3.7.

**nuggets:**
1. The 'think' tool produced more than a 50% performance increase on tau-bench when added to Claude Sonnet 3.7.

---

## fc-0006  (1 nuggets)

**question:** According to a Stanford study on agent frameworks, how often does Microsoft's AutoGen rely on a generalist single LLM/VLM approach rather than invoking other tools?

**claim:** According to the Stanford study, AutoGen uses the generalist (single LLM/VLM) approach about 90% of the time, rarely leveraging other tools.

**nuggets:**
1. AutoGen uses the generalist (single LLM/VLM) approach about 90% of the time

---

## fc-0007  (2 nuggets)

**question:** What did Stanford's research on MinionS find regarding performance and cost when using an 8 billion parameter local LLM compared to relying solely on remote cloud LLMs?

**claim:** Stanford's research found that with an 8 billion parameter local LLM, MinionS can recover close to 98% of the performance of remote-only cloud LLMs at 18% of the cost of using the cloud model exclusively.

**nuggets:**
1. MinionS recovers close to 98% of the performance of remote-only cloud LLMs.
2. MinionS achieves this at 18% of the cost of using the cloud model exclusively.

---

## fc-0009  (2 nuggets)

**question:** What kind of evidence does the L1 paper present to support the claim that models use distinct reasoning strategies at different response lengths?

**claim:** The L1 paper's evidence for distinct reasoning strategies is based on a graph showing that the words 'therefore' and 'so' are used more frequently in shorter (e.g., 500 token) answers than in longer answers.

**nuggets:**
1. The graph shows the frequency of the words 'therefore' and 'so'.
2. These words are used more frequently in shorter answers (e.g., 500 tokens) than in longer answers.

---

## fc-0010  (2 nuggets)

**question:** On average across benchmark scenarios, how much did REMA's multi-agent meta-thinking training improve performance over the baseline approaches?

**claim:** Averaged across all benchmark scenarios, the baseline approaches scored around 50-51%, and after the full multi-agent meta-thinking REMA training and optimization process, performance improved to approximately 53%.

**nuggets:**
1. Baseline approaches scored around 50-51% on average across benchmark scenarios.
2. After full multi-agent meta-thinking REMA training, performance improved to approximately 53%.

---

## fc-0012  (5 nuggets)

**question:** On missing-data questions where the correct answer is to admit data isn't available, how do abstain rates compare between reasoning models like QwQ, Stanford S1, DeepSeek, and o3-mini versus non-reasoning models?

**claim:** For missing-data questions, the study found abstain rates (correctly stating data is missing) of 10% for QwQ, 16% for Stanford S1, 16% for DeepSeek, and 23% for o3-mini, compared to over 50% abstain rate for non-reasoning models.

**nuggets:**
1. QwQ has an abstain rate of 10%
2. Stanford S1 has an abstain rate of 16%
3. DeepSeek has an abstain rate of 16%
4. o3-mini has an abstain rate of 23%
5. Non-reasoning models have an abstain rate of over 50%

---

## fc-0013  (3 nuggets)

**question:** How does performance change as the supervised fine-tuning dataset size increases from 20,000 samples to 1 million samples?

**claim:** Scaling the supervised fine-tuning dataset size improves performance: with 20,000 data samples performance rises from about 16% to 50%, and with 1 million data samples it reaches about 70%.

**nuggets:**
1. With about 20,000 samples, performance is about 16%.
2. With about 20,000 samples, performance rises to about 50%.
3. With about 1 million samples, performance reaches about 70%.

---

## fc-0015  (3 nuggets)

**question:** What happens to entropy and reasoning quality when off-policy traces are naively combined with on-policy learning during training?

**claim:** Naively combining off-policy traces with on-policy learning causes an immediate entropy collapse to a single solution, leading to overly rapid convergence and the model latching onto superficial patterns rather than genuine reasoning.

**nuggets:**
1. Entropy collapses immediately to a single solution when off-policy traces are naively combined with on-policy learning.
2. This causes overly rapid convergence.
3. The model latches onto superficial patterns rather than genuine reasoning.

---

## fc-0017  (2 nuggets)

**question:** In the context of an AI system built for laser fusion experiments, what is it actually designed to do if its purpose goes beyond just writing code?

**claim:** The creator explains that the system is not about writing code but about automating the scientific method itself: experiment, discover, reason about results, form new hypotheses, formulate new experiments with new parameters, run a digital twin simulation, and if successful, run the real laser fusion experiment, then repeat the loop.

**nuggets:**
1. The system automates the scientific method itself, rather than just writing code.
2. It runs a digital-twin simulation and, only if that succeeds, runs the real laser-fusion experiment, then repeats the loop.

---

## fc-0020  (2 nuggets)

**question:** What recall rate did Deep Retrieval achieve on publication search compared to the state-of-the-art method?

**claim:** Deep Retrieval outperformed leading literature search methods, achieving 65% recall for publication search compared to a SOTA of 24% recall.

**nuggets:**
1. Deep Retrieval achieved 65% recall for publication search.
2. The state-of-the-art method achieved 24% recall for publication search.

---

## fc-0021  (1 nuggets)

**question:** How many button presses did GPT-OSS-120B use in its solution to the elevator causal reasoning test?

**claim:** GPT-OSS-120B produced a 15-press solution to the elevator causal reasoning test.

**nuggets:**
1. GPT-OSS-120B produced a solution with 15 button presses.

---

## fc-0026  (2 nuggets)

**question:** How does the 14B Deep-DxSearch model compare in performance to the much larger 671B DeepSeek R1 system on common versus rare disease diagnosis tasks?

**claim:** The 14B Deep-DxSearch model outperforms a 671B DeepSeek R1 system by nearly 20 percentage points on common disease diagnosis and nearly 30 percentage points on rare disease diagnosis.

**nuggets:**
1. Deep-DxSearch outperforms DeepSeek R1 by nearly 20 percentage points on common disease diagnosis.
2. Deep-DxSearch outperforms DeepSeek R1 by nearly 30 percentage points on rare disease diagnosis.

---

## fc-0031  (3 nuggets)

**question:** How does the rank of the weight update differ between standard fine-tuning and in-context learning (ICL), and why does this make ICL's update fast, temporary, and specific to the current token position?

**claim:** Standard fine-tuning updates the whole weight matrix (rank N), making it expensive and slow, whereas ICL uses only a rank-one update, making it fast, temporary, and hyper-specific to the current token position due to non-linearity.

**nuggets:**
1. Standard fine-tuning updates the whole weight matrix (rank N).
2. ICL uses only a rank-one update.
3. The position-specificity comes from non-linearity.

---

## fc-0032  (1 nuggets)

**question:** What score did Gemini 3 Deep Think achieve on the ARC-AGI-2 benchmark?

**claim:** Gemini 3 Deep Think scores 45% on the ARC-AGI-2 benchmark.

**nuggets:**
1. Gemini 3 Deep Think scored 45% on the ARC-AGI-2 benchmark.

---

## fc-0033  (2 nuggets)

**question:** In Nemotron Elastic's multi-size training setup with 6B, 9B, and 12B models, what went wrong when the training budget was sampled uniformly across the three sizes?

**claim:** Researchers found that if the training budget across the 6B, 9B, and 12B models was sampled uniformly, gradient updates from struggling smaller models overwhelmed the fine-tuning of the larger models, causing the 12B model to become less capable ('more stupid').

**nuggets:**
1. Gradient updates from the smaller (struggling) models overwhelmed the fine-tuning of the larger models.
2. This caused the 12B model to become less capable ('more stupid').

---

## fc-0038  (1 nuggets)

**question:** What did the VLM4VA paper's ablation study find about the correlation between a vision-language model's performance on standard visual question-answering benchmarks and its success rate in robotic manipulation tasks?

**claim:** The VLM4VA paper's core innovation is a systematic ablation demonstrating the visual-semantic gap in real AI systems, finding zero correlation between a vision-language model's performance on standard vision question-answering benchmarks and its success rate in robotic manipulation.

**nuggets:**
1. The study found zero correlation between the vision-language model's visual-question-answering benchmark performance and its robotic-manipulation success rate.

---

## fc-0040  (2 nuggets)

**question:** Approximately how many high-quality quintuples and how many 3D knee MRI volumes make up the dataset built by researchers affiliated with Harvard Medical School?

**claim:** The dataset comprises close to 500,000 high quality quintuples derived from about 8,000 three-dimensional knee MRI volumes.

**nuggets:**
1. The dataset comprises close to 500,000 high-quality quintuples.
2. The dataset is derived from about 8,000 three-dimensional knee MRI volumes.

---

## fc-0042  (2 nuggets)

**question:** How many button presses did Qwen 3.5 397B-A17B end up using to solve the elevator puzzle, and was that considered a good result?

**claim:** The final result for Qwen 3.5 397B-A17B was a 19-press solution, and the creator states this is not a good result.

**nuggets:**
1. Qwen 3.5 397B-A17B used 19 button presses to solve the elevator puzzle.
2. The creator states this is not a good result.

---

## fc-0043  (2 nuggets)

**question:** How does ALOE's intrinsic reward function work, and why does it rely on eigenvectors of a state graph rather than a simple error signal?

**claim:** ALOE measures geometric diffusion on a topological space rather than a simple error, calculating eigenvectors of the state graph to reward the agent for reaching states that are mathematically furthest apart.

**nuggets:**
1. ALOE measures geometric diffusion on a topological space.
2. The agent is rewarded for reaching states that are mathematically furthest apart.

---

## fc-0044  (1 nuggets)

**question:** In few-shot Q&A examples like 'France->Paris' and 'Japan->Tokyo', why does the geometric transition from country to capital appear as a discontinuity rather than a straight line?

**claim:** In a few-shot Q&A example (e.g., 'France->Paris', 'Japan->Tokyo'), the transition from country to capital is not a straight line but a discontinuity, indicating the model uses a different, nonlinear geometric mechanism to jump from country to capital.

**nuggets:**
1. The model uses a different, nonlinear geometric mechanism to jump from country to capital.

---

## fc-0045  (3 nuggets)

**question:** In a multi-agent system, how does the time required to reach consensus scale with population size, message bandwidth M, and the adaptation rate alpha?

**claim:** The paper's author derives that the time to reach consensus in a multi-agent system grows quadratically with population size, grows linearly with message bandwidth (M), and shrinks quadratically with the adaptation rate alpha.

**nuggets:**
1. Consensus time grows quadratically with population size.
2. Consensus time grows linearly with message bandwidth M.
3. Consensus time shrinks quadratically with adaptation rate alpha.

---

## fc-0048  (1 nuggets)

**question:** In the 'asymmetric prediction paradox' finding, what accuracy did an auto-rater achieve when predicting honest ('label A') outcomes from the reasoning traces of a Gemma 27B model?

**claim:** In the 'asymmetric prediction paradox' finding, an auto-rater reading the reasoning traces of a Gemma 27B model predicted honest ('label A') outcomes with 97% accuracy.

**nuggets:**
1. The auto-rater achieved 97% accuracy predicting honest ('label A') outcomes.

---
