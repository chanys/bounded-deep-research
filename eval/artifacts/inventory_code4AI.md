# Corpus inventory: code4AI

git_sha `37d73b323433` (dirty=True) | taxonomy model `claude-sonnet-5`

## Population

- manifest total: 1338
- in inventory: 475
- with DB chunk counts: 475
- chapter coverage: 36 videos (>= 2 lines)

## Clusters

| cluster | label | videos | % | hours | chunks |
|---|---|---:|---:|---:|---:|
| c01 | Elevator/Logic Puzzle Model Benchmarks | 54 | 11% | 15.9 | 1935 |
| c19 | Multi-Agent System Architectures & Protocols | 28 | 6% | 13.5 | 1630 |
| c06 | Reinforcement Learning Algorithms for Reasoning (GRPO/DAPO/etc.) | 23 | 5% | 11.3 | 1364 |
| c07 | Test-Time Compute & Inference Scaling | 20 | 4% | 9.5 | 1144 |
| c24 | Knowledge Graphs & GraphRAG Systems | 20 | 4% | 10.6 | 1274 |
| c04 | AI Reasoning Failure & Limitation Studies | 18 | 4% | 8.3 | 1009 |
| c32 | World Models & Model-Based AI | 18 | 4% | 9.0 | 1083 |
| c09 | Reasoning Architecture Innovations (Topology, Hierarchy, Graphs) | 15 | 3% | 6.5 | 789 |
| c22 | Self-Evolving & Self-Improving Agents | 15 | 3% | 6.7 | 811 |
| c26 | Neuro-Symbolic AI Integration | 14 | 3% | 7.3 | 878 |
| c27 | AI for Scientific Discovery & Research Automation | 14 | 3% | 5.9 | 718 |
| c21 | Agent Skills, Harness & Memory Engineering | 13 | 3% | 7.0 | 849 |
| c02 | Frontier Model Release Testing | 12 | 3% | 4.4 | 534 |
| c18 | Transformer Architecture Alternatives | 12 | 3% | 6.7 | 813 |
| c30 | Vision-Language & Multimodal Reasoning | 12 | 3% | 5.9 | 715 |
| c03 | Open-Source & MoE Model Comparisons | 11 | 2% | 3.9 | 468 |
| c08 | Small Model Reasoning Distillation & Efficiency | 11 | 2% | 4.4 | 534 |
| c11 | Physics/Math-Inspired Theoretical Frameworks for AI | 11 | 2% | 5.2 | 631 |
| c23 | Agentic RAG & Search-Augmented Reasoning | 11 | 2% | 4.7 | 568 |
| c13 | In-Context Learning Mechanisms | 10 | 2% | 4.8 | 578 |
| c20 | Multi-Agent Failure Modes & Debate Risks | 9 | 2% | 3.6 | 436 |
| c25 | RAG Limitations & Knowledge Conflicts | 9 | 2% | 4.1 | 499 |
| c41 | AI Weekly News & Paper Roundups | 9 | 2% | 4.1 | 494 |
| c10 | Interpretability of Model Internals | 8 | 2% | 3.9 | 476 |
| c28 | Deep Research Tools Evaluation | 8 | 2% | 3.7 | 444 |
| c16 | Reward Modeling & RLHF | 7 | 1% | 2.9 | 356 |
| c29 | Medical & Clinical AI Applications | 7 | 1% | 2.4 | 288 |
| c31 | Vision-Language-Action & Robotics | 7 | 1% | 3.2 | 392 |
| c33 | AI Agent Benchmarking & Scaling Laws | 7 | 1% | 3.0 | 361 |
| c40 | AI Companion, Persona & Emotional Modeling | 7 | 1% | 3.5 | 427 |
| c05 | Chain-of-Thought Mechanics & Faithfulness | 6 | 1% | 2.9 | 354 |
| c14 | Fine-Tuning, PEFT & Continual Learning | 6 | 1% | 2.5 | 300 |
| c15 | Pre-training & Data Strategy | 6 | 1% | 3.1 | 380 |
| c17 | Model Quantization & Hardware Deployment | 5 | 1% | 1.5 | 183 |
| c34 | AI Safety, Deception & Alignment | 5 | 1% | 2.3 | 278 |
| c35 | Agent & LLM Security Threats | 5 | 1% | 1.9 | 229 |
| c36 | DSPy & Prompt/Context Optimization | 5 | 1% | 3.0 | 365 |
| c12 | Grokking & Training Dynamics | 4 | 1% | 1.5 | 182 |
| c37 | AI Coding Agents & Software Engineering | 4 | 1% | 1.2 | 148 |
| c39 | AI Business, Economics & Job Impact | 4 | 1% | 1.9 | 227 |
| c38 | Google/Anthropic Agent Frameworks (ADK, MCP tooling) | 3 | 1% | 1.6 | 192 |
| other | other | 2 | 0% | 0.5 | 65 |

## Cluster definitions

- **Elevator/Logic Puzzle Model Benchmarks** (`c01`): Videos testing individual or paired LLMs on the creator's signature causal-reasoning elevator puzzle and similar logic grid puzzles.
- **Frontier Model Release Testing** (`c02`): Hands-on first-look tests and live evaluations of newly released proprietary/open frontier LLMs beyond the standard puzzle format (broader reasoning, coding, cost).
- **Open-Source & MoE Model Comparisons** (`c03`): Benchmarking and architectural comparison of open-weight models, mixture-of-experts variants, and thinking/non-thinking mode toggles.
- **AI Reasoning Failure & Limitation Studies** (`c04`): Research-backed critiques exposing systematic failures, illusions, or collapse of LLM/LRM reasoning under complexity, novel tasks, or scaling.
- **Chain-of-Thought Mechanics & Faithfulness** (`c05`): Deep dives into how chain-of-thought reasoning works, its faithfulness, overthinking, monitoring, and manipulation.
- **Reinforcement Learning Algorithms for Reasoning (GRPO/DAPO/etc.)** (`c06`): Technical explanations of RL training methods (GRPO, DAPO, VAPO, PPO, DPO variants) used to improve LLM reasoning.
- **Test-Time Compute & Inference Scaling** (`c07`): Methods and papers focused on scaling reasoning quality via extra inference-time compute, search, or budget forcing rather than training.
- **Small Model Reasoning Distillation & Efficiency** (`c08`): Techniques for distilling reasoning ability from large teacher models into smaller/cheaper student models and efficiency tradeoffs.
- **Reasoning Architecture Innovations (Topology, Hierarchy, Graphs)** (`c09`): Novel structured reasoning frameworks beyond plain chain-of-thought: trees/graphs of thought, hierarchical reasoning models, sketch of thought.
- **Interpretability of Model Internals** (`c10`): Mechanistic interpretability probing hidden activations, neurons, hallucination circuits, and geometric structure of transformer internals.
- **Physics/Math-Inspired Theoretical Frameworks for AI** (`c11`): Applying physics, topology, category theory or statistical mechanics analogies to explain or design AI training/reasoning dynamics.
- **Grokking & Training Dynamics** (`c12`): Studies of grokking, softmax collapse, spectral bias, and generalization/memorization phase transitions during training.
- **In-Context Learning Mechanisms** (`c13`): Papers explaining how in-context learning works mathematically/geometrically and its relation to fine-tuning and world modeling.
- **Fine-Tuning, PEFT & Continual Learning** (`c14`): LoRA/QLoRA, PEFT methods, continual learning, catastrophic forgetting, and model merging techniques.
- **Pre-training & Data Strategy** (`c15`): Research on pre-training methodology, data quality/composition, curriculum, and scaling laws affecting downstream model capability.
- **Reward Modeling & RLHF** (`c16`): Design and critique of reward models, RLHF, preference optimization, and reward hacking phenomena.
- **Model Quantization & Hardware Deployment** (`c17`): Practical evaluation of quantization formats, local deployment tools, GPU hardware and inference cost/performance tradeoffs.
- **Transformer Architecture Alternatives** (`c18`): Proposals and critiques of new architectures beyond standard transformers (Titans, HRM, CTM, encoder-decoder revival, distributed graphs).
- **Multi-Agent System Architectures & Protocols** (`c19`): Design of multi-agent orchestration, communication protocols (MCP, A2A), topology, and agent frameworks.
- **Multi-Agent Failure Modes & Debate Risks** (`c20`): Studies showing multi-agent systems degrade, hallucinate collectively, or fail to communicate/coordinate effectively.
- **Agent Skills, Harness & Memory Engineering** (`c21`): Skill.md files, harness/scaffolding design, file-based memory, and context engineering for autonomous agents.
- **Self-Evolving & Self-Improving Agents** (`c22`): Agents that autonomously improve, rewrite, or evolve their own strategies, code, or reasoning without human retraining.
- **Agentic RAG & Search-Augmented Reasoning** (`c23`): Retrieval-augmented generation systems that incorporate agentic reasoning, RL, or tool-based search rather than static retrieval.
- **Knowledge Graphs & GraphRAG Systems** (`c24`): Integration of knowledge graphs with LLMs/RAG for retrieval, reasoning, and hallucination reduction.
- **RAG Limitations & Knowledge Conflicts** (`c25`): Analyses of when and why RAG fails: knowledge conflicts, hallucination, context ignoring, and security risks.
- **Neuro-Symbolic AI Integration** (`c26`): Combining symbolic solvers/logic (PDDL, Lean, Prolog) with neural LLMs for more reliable reasoning and planning.
- **AI for Scientific Discovery & Research Automation** (`c27`): Autonomous AI scientists, research agents, peer review, and automated hypothesis/experiment pipelines applied to real science.
- **Deep Research Tools Evaluation** (`c28`): Comparative testing and trustworthiness analysis of commercial/open deep-research AI agents (OpenAI, Google, Perplexity, etc.).
- **Medical & Clinical AI Applications** (`c29`): LLM applications, benchmarks, and safety issues in medical diagnosis, healthcare communication, and clinical decision-making.
- **Vision-Language & Multimodal Reasoning** (`c30`): Capabilities and limitations of vision-language models handling images, video, and multimodal reasoning tasks.
- **Vision-Language-Action & Robotics** (`c31`): Embodied AI, robotic manipulation, autonomous driving, and VLA models connecting perception to physical action.
- **World Models & Model-Based AI** (`c32`): Research on learned world models for planning, simulation, and physical/causal understanding distinct from pure LLM prediction.
- **AI Agent Benchmarking & Scaling Laws** (`c33`): Empirical studies quantifying agent performance, scaling laws, cost, and topology effects across benchmark suites.
- **AI Safety, Deception & Alignment** (`c34`): Research on honesty, deception, sycophancy, hidden goals, and alignment risks in LLM behavior.
- **Agent & LLM Security Threats** (`c35`): Prompt injection, jailbreaking, adversarial attacks, and security vulnerabilities in agentic and RAG systems.
- **DSPy & Prompt/Context Optimization** (`c36`): Frameworks and methods (DSPy, GEPA, TextGrad) for automatically optimizing prompts, context, and agent topologies.
- **AI Coding Agents & Software Engineering** (`c37`): Agentic coding tools, benchmarks, and frameworks focused on software engineering tasks and code generation.
- **Google/Anthropic Agent Frameworks (ADK, MCP tooling)** (`c38`): Tutorials and explainers on building agents with vendor SDKs (Google ADK, Hugging Face smolagents, Anthropic tooling).
- **AI Business, Economics & Job Impact** (`c39`): Discussion of AI's economic impact, market data, job displacement, freelance platforms, and enterprise adoption.
- **AI Companion, Persona & Emotional Modeling** (`c40`): Personalization, persona injection, emotion modeling, and digital twin/avatar design for human-AI interaction.
- **AI Weekly News & Paper Roundups** (`c41`): Multi-paper digest episodes summarizing several unrelated recent AI research papers or news items in one video.

## Time axis (videos per cluster per month)

| cluster | 2025-01 | 2025-02 | 2025-03 | 2025-04 | 2025-05 | 2025-06 | 2025-07 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 | 2026-01 | 2026-02 | 2026-03 | 2026-04 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c01 | 2 | 1 | 5 | 2 | 5 | 5 | 4 | 5 | 2 |  | 3 | 4 | 1 | 5 | 4 | 6 |
| c02 |  | 1 |  | 2 |  | 1 |  | 2 |  | 1 | 2 | 2 |  |  |  | 1 |
| c03 | 2 |  |  | 2 | 2 |  |  |  | 1 |  | 1 |  |  | 3 |  |  |
| c04 |  | 1 | 1 | 2 |  | 3 | 4 | 1 | 1 | 3 |  |  | 1 |  | 1 |  |
| c05 |  |  | 3 | 1 |  |  |  |  |  | 2 |  |  |  |  |  |  |
| c06 | 1 |  | 6 | 4 |  | 2 | 1 |  | 1 |  | 2 | 1 | 2 | 1 | 2 |  |
| c07 | 3 | 5 | 1 | 2 | 1 | 1 | 1 |  |  | 1 | 1 | 2 | 1 |  | 1 |  |
| c08 | 3 |  | 2 | 1 | 1 |  | 2 |  |  |  |  |  | 1 | 1 |  |  |
| c09 |  |  | 4 |  | 1 |  | 1 | 1 |  | 3 | 1 |  | 2 | 1 | 1 |  |
| c10 |  |  |  |  |  |  | 1 |  |  | 1 | 1 | 3 | 1 | 1 |  |  |
| c11 |  |  |  | 1 | 1 |  |  | 2 |  | 2 | 2 | 1 |  | 1 | 1 |  |
| c12 | 2 |  |  |  |  |  |  |  |  |  | 1 | 1 |  |  |  |  |
| c13 | 2 |  |  |  | 2 |  |  |  |  | 1 | 1 | 1 |  | 2 |  | 1 |
| c14 | 1 |  |  |  | 1 | 1 |  |  |  |  |  |  | 1 | 1 | 1 |  |
| c15 | 1 |  |  |  | 2 | 1 | 2 |  |  |  |  |  |  |  |  |  |
| c16 |  | 1 |  | 1 | 1 |  | 1 | 2 |  |  |  |  | 1 |  |  |  |
| c17 | 1 | 1 |  |  |  |  |  | 2 |  |  |  |  |  | 1 |  |  |
| c18 | 1 |  |  | 1 | 1 |  | 1 | 1 |  |  | 2 | 2 | 3 |  |  |  |
| c19 | 1 | 4 |  | 2 | 1 | 3 | 1 | 1 | 4 | 3 |  | 2 |  | 3 | 3 |  |
| c20 | 1 |  | 1 |  |  |  |  |  | 2 |  | 1 |  | 1 | 2 |  | 1 |
| c21 |  |  |  |  |  |  |  |  |  | 1 |  |  |  |  | 6 | 6 |
| c22 | 2 | 1 |  |  | 1 |  | 1 | 1 |  |  | 1 |  |  | 3 | 4 | 1 |
| c23 |  | 1 |  | 1 | 1 | 1 |  | 5 |  | 1 |  |  |  |  |  | 1 |
| c24 | 3 | 4 |  |  |  | 1 | 5 | 2 |  |  | 2 |  | 1 |  | 1 | 1 |
| c25 |  |  |  | 1 |  | 2 |  |  | 2 |  | 1 |  | 2 |  |  | 1 |
| c26 |  |  |  |  | 2 |  | 2 | 1 | 1 | 3 | 1 |  | 2 | 1 | 1 |  |
| c27 | 1 | 1 |  | 2 |  | 1 | 1 | 1 | 4 |  |  | 3 |  |  |  |  |
| c28 |  | 3 | 1 |  |  | 1 |  | 2 |  | 1 |  |  |  |  |  |  |
| c29 | 1 | 1 |  | 2 | 1 |  |  |  | 1 |  |  |  | 1 |  |  |  |
| c30 |  |  | 1 |  |  | 2 |  | 1 | 2 | 1 | 3 | 1 |  |  |  | 1 |
| c31 |  |  | 4 |  |  |  |  |  | 1 |  |  |  | 1 |  | 1 |  |
| c32 |  |  | 1 |  |  | 2 | 1 | 3 | 4 |  | 1 | 3 | 1 | 1 | 1 |  |
| c33 |  |  |  |  |  | 1 |  | 2 | 1 | 1 |  | 1 | 1 |  |  |  |
| c34 |  |  |  |  | 1 |  |  |  |  | 1 | 1 |  | 1 |  | 1 |  |
| c35 |  |  |  |  | 4 |  |  |  | 1 |  |  |  |  |  |  |  |
| c36 |  | 1 |  |  | 1 |  | 2 |  |  |  |  |  |  |  | 1 |  |
| c37 |  |  |  | 1 | 1 | 1 |  |  | 1 |  |  |  |  |  |  |  |
| c38 | 2 |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  |
| c39 |  |  |  | 1 |  |  | 1 |  |  |  |  |  | 1 | 1 |  |  |
| c40 |  |  |  | 1 |  |  | 1 |  | 1 |  | 2 | 2 |  |  |  |  |
| c41 |  | 1 |  |  | 2 | 1 |  |  | 2 | 1 |  |  | 2 |  |  |  |
| other |  |  | 1 |  |  |  |  |  |  |  |  |  |  |  |  | 1 |
