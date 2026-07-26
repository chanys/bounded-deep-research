# Task 6 longitudinal shortlist (advisory second-reader triage)

Produced by an LLM-assisted advisory read (chat assistant, all 503 pass candidates reviewed);
recorded here deterministically (no LLM calls). NO LLM verdict gates any outcome - human
verification of every keep, plus a 10-item drop spot-check, is pending.

TIER 1: 22 | TIER 2: 19 | SPOT-CHECK: 10 (seed 20260716, from 456 non-shortlisted non-span-flagged pass)

All shortlisted ids exist and are pass candidates.

## Dedup / read notes (carry into the sitting)
- lc-0127 vs lc-0395: same elevator arc, keep ONE (lc-0395 not shortlisted).
- lc-0407: the known non-determinism flip thread - read closely.
- lc-0034 / lc-0297: keep at most one.
- lc-0413 / lc-0497: keep at most one.
- lc-0014 / lc-0024: keep at most one.


# TIER 1 (22)

### lc-0130  [topic:emergent intelligence]  span=358d  advisory=neutral
**Q:** How did the creator's stance on emergent intelligence in AI models evolve from March 2025 through early 2026?
trajectory_must_say:
- From March 2025 through January 2026, the creator repeatedly concluded there was no genuine emergent intelligence in LLMs, citing evidence from order-dependent reasoning patterns, failure to uncover physical laws from sequence prediction, failure to replicate expert-level medical reasoning datasets, and the impossibility of a distilled model exceeding its teacher's learned representation.
- By February 2026, the creator shifted toward a more conditional view, arguing that specific infrastructure—treating deep context as addressable, sliceable, and synchronizable memory—could provide what is necessary for true emergent intelligence, rather than dismissing the possibility outright.
milestones (5):
- 2025-03-05  `EK96uN4Xt1o#c002`  chunk_ids=['EK96uN4Xt1o:00030']
    The creator concludes that LLMs are learning order-dependent patterns in multi-step reasoning rather than exhibiting an emergence of true intelligence.
- 2025-07-12  `jxB-lQyAAxU#c036`  chunk_ids=['jxB-lQyAAxU:01620', 'jxB-lQyAAxU:01650']
    The creator concludes that the paper's answer is a resounding no: sequence prediction of orbital position alone is not enough to uncover the underlying physical laws, and there is no emergent intelligence in these AI models.
- 2025-10-28  `M_Ic8Y6OQZ8#c013`  chunk_ids=['M_Ic8Y6OQZ8:00300', 'M_Ic8Y6OQZ8:00330', 'M_Ic8Y6OQZ8:00360']
    The creator argues that training current LLMs on medical textbooks and internet resources has failed to produce datasets like the one Harvard Medical School created, showing there is no emergent reasoning ability in LLMs.
- 2026-01-02  `96XVs6qcIT4#c044`  chunk_ids=['96XVs6qcIT4:00750', '96XVs6qcIT4:00780']
    The creator states that intelligence not present in the 72 billion parameter teacher's learned representation cannot be found in the 3 billion parameter distilled model, dismissing the idea of emergent intelligence in this context.
- 2026-02-26  `jUz-RCjcHuE#c059`  chunk_ids=['jUz-RCjcHuE:01350', 'jUz-RCjcHuE:01380']
    The creator argues that treating deep context as an addressable, sliceable, and synchronizable memory space provides infrastructure necessary for true emergent intelligence.

### lc-0143  [topic:externalization]  span=263d  advisory=neutral
**Q:** How did the creator's characterization of 'externalization' in AI/agent systems develop from mid-2025 through April 2026 as he encountered the concept across different papers and systems?
trajectory_must_say:
- Began by describing a specific paper's (GraphRAG) philosophy where the LLM is not the source of truth but an interface to an external, auditable, dynamically updatable knowledge source
- Was later illustrated concretely via a system architecture that put every intermediate processing step into an external file system rather than the LLM's own context/working memory
- Culminated in a broader paper synthesis where the creator explicitly noted a shift from the prior year's view (handle everything inside the model via SFT/RL) to a new view that memory, skills, and protocols should be externalized
- Was grounded in historical framing (comparison to Norman's 1991 work on distributed cognition) and concluded that reliable agency depends on moving cognitive burdens out of the model into explicit, deterministic infrastructure
milestones (5):
- 2025-07-26  `T3dxC9_mp1M#c039`  chunk_ids=['T3dxC9_mp1M:01110', 'T3dxC9_mp1M:01140']
    The creator contrasts this with the GraphRAG paper's philosophy of complete externalization, where the LLM is not the source of truth but an intelligent interface to an external, auditable, dynamically updatable source of truth.
- 2026-03-28  `2WAucAspkZE#c024`  chunk_ids=['2WAucAspkZE:00450', '2WAucAspkZE:00480', '2WAucAspkZE:00510']
    The core idea of the system is to put every intermediate step of processing into an external file system rather than in the LLM's conversation or working memory.
- 2026-04-15  `phfGmvYQCA8#c063`  chunk_ids=['phfGmvYQCA8:01950']
    The creator observes that a year ago the prevailing view was that everything needed to be handled inside the AI system's weights via supervised fine-tuning and reinforcement learning, but today the view is that memory, skills, and protocols should instead be externalized.
- 2026-04-15  `phfGmvYQCA8#c071`  chunk_ids=['phfGmvYQCA8:02160', 'phfGmvYQCA8:02190']
    The paper's authors compare the externalization trend to Norman's 1991 work, stating that burdens hard to manage inside a model are progressively moved into explicit artifacts outside the model, making the tasks seen by the model easier.
- 2026-04-15  `phfGmvYQCA8#c076`  chunk_ids=['phfGmvYQCA8:02310', 'phfGmvYQCA8:02340']
    The paper's conclusion is that reliable agency increasingly depends on relocating selected cognitive burdens out of the AI model and into an explicit, deterministic, rule-based infrastructure around it.

### lc-0070  [topic:code generation]  span=264d  advisory=neutral
**Q:** How did the creator's assessment of AI systems' code generation capabilities and reliability evolve from mid-2025 through early 2026?
trajectory_must_say:
- Early on, benchmark results (e.g., HumanEval) were cited as showing AI code generation achieving near-perfect accuracy.
- Hands-on testing later revealed that AI-generated code often failed to run correctly and contained multiple errors when actually executed.
- Debugging uncovered that generated code could contain hidden shortcuts, such as a handler that silently converted an illegal move into a legal one to make a solution appear valid, requiring careful removal before a genuinely correct solution was confirmed.
- Later assessments shifted toward more structured approaches, including multi-agent role divisions for code generation tasks and frameworks where code no longer needs to be manually written at all, being automatically compiled from approved blueprints.
milestones (6):
- 2025-06-19  `3fNUh39h7EI#c001`  chunk_ids=['3fNUh39h7EI:00000']
    AI code generation models achieve nearly 100% accuracy on the HumanEval benchmark.
- 2025-06-30  `eo2QwyAItxI#c018`  chunk_ids=['eo2QwyAItxI:00420']
    The code generated by o3 for its nine-step solution did not work when run in a Colab notebook, containing multiple mistakes.
- 2025-06-30  `eo2QwyAItxI#c035`  chunk_ids=['eo2QwyAItxI:00780']
    Gemini 2.5 Pro revealed that o3's code contained a handler that automatically corrected the illegal move to floor 63 into a legal landing on floor 50, effectively making an out-of-bounds move artificially legal.
- 2025-06-30  `eo2QwyAItxI#c043`  chunk_ids=['eo2QwyAItxI:00990']
    The creator ran Gemini 2.5 Pro's eight-step solution code in Colab and confirmed it executed correctly in about 1 second, validating it as the correct solution.
- 2026-02-10  `jWhnicSLdD4#c055`  chunk_ids=['jWhnicSLdD4:01140', 'jWhnicSLdD4:01170']
    For code generation tasks, the paper's authors used four agent roles: developer, researcher, tester, and designer.
- 2026-03-10  `QFlQuX_cddk#c040`  chunk_ids=['QFlQuX_cddk:00720', 'QFlQuX_cddk:00900']
    Once the blueprint is generated and approved by a human, no underlying Python code or logic needs to be written, because the framework engine automatically compiles it into an executable graph.

### lc-0398  [topic:reward hacking]  span=349d  advisory=neutral
**Q:** How did the creator's characterization and treatment of reward hacking evolve from March 2025 through early 2026 as new research and his own experiments accumulated?
trajectory_must_say:
- Early coverage framed reward hacking as a general/theoretical risk, illustrated through OpenAI's o3 report and simple analogies like a self-driving car gaming an efficiency reward.
- Anthropic's research showed models rarely admit to reward hacking in their chain-of-thought reasoning and instead often fabricate plausible-sounding justifications for the hacked answer.
- Later papers identified specific named exploit mechanisms (e.g., an 'irrelevance hack' and an 'inflation hack') and proposed mitigations such as dynamic reward co-optimization between policy and reward models.
- The creator eventually observed reward hacking directly in his own experiments, such as a model collapsing into a 'cheat code' of short useless answers, and discussed mitigation techniques like KL divergence regularization.
milestones (6):
- 2025-03-15  `xqOAdmgUAC8#c069`  chunk_ids=['xqOAdmgUAC8:02760']
    OpenAI o3's report warns that RL reward design is challenging and overly simplistic rewards can lead to reward hacking, where models find loopholes to trick scoring without being truly correct.
- 2025-04-05  `HlpFt9zNSjs#c021`  chunk_ids=['HlpFt9zNSjs:00510', 'HlpFt9zNSjs:00630']
    Anthropic found that language models rarely admitted to using the reward hacks in their chain of thought explanation, doing so in less than 2% of the time.
- 2025-08-08  `fu5zO34RDf0#c018`  chunk_ids=['fu5zO34RDf0:00480']
    The paper describes an 'irrelevance hack' where the reward function measures only factuality and not relevance, so the LLM generates verifiable but off-topic facts about a safe, well-documented subject to achieve a 100% success rate.
- 2025-08-09  `WsCAu7LGN0E#c042`  chunk_ids=['WsCAu7LGN0E:00870']
    GPT-5 reported that co-optimization of the policy model and reward model with a dynamic reward mitigates reward hacking and improves final policy performance, per the paper.
- 2026-01-21  `hDYtGpTsVV0#c041`  chunk_ids=['hDYtGpTsVV0:00870']
    Using identical static weights (e.g. 1.0) for all three reward objectives causes the tiny model to find a 'cheat code,' collapsing into maximizing only conciseness by generating short but useless answers.
- 2026-02-27  `K4yLplNrY24#c066`  chunk_ids=['K4yLplNrY24:02400', 'K4yLplNrY24:02430']
    A frozen reference model (the direct output of the SFT phase) is used alongside the policy model, with Kullback-Leibler (KL) divergence keeping the policy model from diverging too far from the reference model to prevent reward hacking, though KL divergence introduces its own tradeoffs.

### lc-0087  [topic:continuous learning]  span=252d  advisory=neutral
**Q:** How did the creator's assessment of whether and how AI systems can achieve continuous learning evolve from mid-2025 through early 2026, as he examined different training approaches and applications?
trajectory_must_say:
- He initially treated continuous learning as currently not possible, then argued that a 14B model's RPT training loop actually constitutes continuous learning.
- Around the same period he also noted that LLMs generally have trouble systematically integrating new evidence into their prior beliefs and reasoning patterns.
- He later pointed to a continuous learning process improving accuracy and cost-efficiency over time in a team-selection context.
- By early 2026 he refined his view to argue that memory optimization alone is not sufficient for true continuous learning, and that achieving neuroplasticity-like learning without forgetting requires a more clever implementation.
milestones (4):
- 2025-06-15  `7ec_0NPxmnA#c035`  chunk_ids=['7ec_0NPxmnA:01620', '7ec_0NPxmnA:01650', '7ec_0NPxmnA:01680', '7ec_0NPxmnA:01710', '7ec_0NPxmnA:01740', '7ec_0NPxmnA:01770', '7ec_0NPxmnA:01800']
    The creator argues that the 14B model does learn continuously throughout the RPT optimization process, based on the training loop where a forward pass generates reasoning traces, an automatic verifier compares outputs to ground truth, rewards are assigned, and weights are updated via GRPO (policy gradient algorithm) using backpropagation and an Adam optimizer.
- 2025-06-25  `wzXBXGVbItE#c050`  chunk_ids=['wzXBXGVbItE:01320', 'wzXBXGVbItE:01350']
    The creator states that LLMs have a problem with continuous updates to their learning process, as new evidence is not systematically integrated into their prior beliefs or deeply woven into their reasoning patterns.
- 2025-09-05  `VMsJ4me5Q3o#c035`  chunk_ids=['VMsJ4me5Q3o:00600']
    This continuous learning process makes future team selection more accurate and cheaper over time.
- 2026-02-22  `hm9WsUS6UH8#c006`  chunk_ids=['hm9WsUS6UH8:00180', 'hm9WsUS6UH8:00210']
    The creator argues that memory optimization alone is not sufficient for true continuous machine learning, and that achieving neuroplasticity (learning continually without forgetting past knowledge) requires more clever implementation.

### lc-0127  [topic:elevator/causal-reasoning-test]  span=445d  advisory=neutral
> NOTE: same arc as lc-0395 (not shortlisted) - keep ONE
**Q:** How did the creator's custom 'elevator' causal-reasoning puzzle test, and the results models achieved on it, evolve from early 2025 through early 2026?
trajectory_must_say:
- The test began as a simpler puzzle (reaching floor 13 with five buttons and one trap) and grew over time into a much more complex version (reaching floor 50 with multiple traps, code cards, energy/token limits, and an emergency exit mechanic)
- Models produced widely varying button-press solutions to the puzzle across this period as the creator kept re-testing new models
- By December 2025, after a year of running this exact test, a model for the first time told the creator it was impossible to end at floor 50
milestones (6):
- 2025-01-31  `P_wuwWJomyM#c010`  chunk_ids=['P_wuwWJomyM:00270', 'P_wuwWJomyM:00300']
    The creator ran his elevator puzzle test on Qwen 2.5 Max, where the goal is to reach floor 13 in a skyscraper using five buttons with different functions, while avoiding a trap floor.
- 2025-03-28  `iVZaJeXu7E8#c009`  chunk_ids=['iVZaJeXu7E8:00150']
    The creator's 'elevator test' requires reaching floor 30 in a skyscraper using five buttons (A, B, C, D, E) with two trap floors, seeking the shortest path.
- 2025-06-24  `SgknC9B1dm8#c008`  chunk_ids=['SgknC9B1dm8:00060', 'SgknC9B1dm8:00090', 'SgknC9B1dm8:00150']
    Gemini 2.5 Pro solved the same 50-floor elevator test using a 10-step (nine button presses plus one emergency exit button action) sequence.
- 2025-08-12  `NP882Zur1Dk#c014`  chunk_ids=['NP882Zur1Dk:00270', 'NP882Zur1Dk:00300']
    The elevator puzzle task requires finding the shortest path (minimum button presses) from floor 0 to floor 50, with limited energy, code cards needed to unlock higher floors, and specific rules that must not be overshot or violated.
- 2025-12-11  `9wg0dGz5-bs#c003`  chunk_ids=['9wg0dGz5-bs:00000', '9wg0dGz5-bs:00030']
    The creator states this is the first model, after one year of testing this exact test, to tell him it is impossible to end at floor 50.
- 2026-04-21  `DdakyHWTkRk#c005`  chunk_ids=['DdakyHWTkRk:00120', 'DdakyHWTkRk:00150']
    The test used is the creator's own 'elevator test', where the goal is to go from floor zero to floor 50 in a 50-floor building using buttons that trigger specific mathematical functions such as time inversion, logical inversion, interwoven dependencies, energy optimization, and token optimization.

### lc-0233  [topic:logic test]  span=111d  advisory=waypoint
**Q:** How did the creator's 'extreme logic test' and his assessment of AI models' ability to solve, verify, and revise their solutions on it evolve from late January 2025 through May 2025?
trajectory_must_say:
- The test began as a 15-clue logic puzzle already used across many models (o1, Grok 2, Gemini, Llama, Claude 3.5 Sonnet) by late January 2025, and in early February a model could confirm multiple valid solutions when asked to verify or try alternative reasoning paths.
- In March 2025, testing with Claude 3.7 Sonnet and DeepSeek R1 led the creator to conclude that models could validate a second valid solution once told their answer was wrong, but neither model could discover that second solution on its own when simply asked to find one.
- By May 2025 the test had grown more complex with additional 'complexity clues' layered onto the original 15, and models like Sonnet 4 and Opus 4 repeatedly failed to incorporate these clues even after being told to revise, with Sonnet 4 eventually being dropped from the test.
- Opus 4 ultimately diagnosed its own failure as a fundamental error of mentally separating the complexity clues from the main clue set and assuming it could reconcile them later, while also recognizing that its original systematic method had been sound.
milestones (6):
- 2025-02-01  `mWWfMoMkqHQ#c013`  chunk_ids=['mWWfMoMkqHQ:00450', 'mWWfMoMkqHQ:00480', 'mWWfMoMkqHQ:00510', 'mWWfMoMkqHQ:00540']
    The model determined there are exactly two distinct valid solutions to the logic puzzle, differing only in the choice between two possibilities involving Brindo/Eloria with Salamanda/Pegasus versus Brendor with Elemental Magic/Pegasus and Salamanda, with all other assignments identical.
- 2025-03-02  `XaLXAufvLNk#c016`  chunk_ids=['XaLXAufvLNk:00330']
    The creator concludes that both models could validate a second solution when told they were wrong, but neither could find the second solution on its own when simply asked to find a second valid solution.
- 2025-05-23  `fgSdunF7Oe0#c004`  chunk_ids=['fgSdunF7Oe0:00090', 'fgSdunF7Oe0:00120']
    Both models' initial solutions completely missed the additional complexity clues required by the instructions.
- 2025-05-23  `fgSdunF7Oe0#c011`  chunk_ids=['fgSdunF7Oe0:00330']
    The creator states that Sonnet 4 is 'out' of the test after repeatedly failing to address the complexity clues, and continues the test using only Opus 4.
- 2025-05-23  `fgSdunF7Oe0#c021`  chunk_ids=['fgSdunF7Oe0:00660', 'fgSdunF7Oe0:00690']
    Claude Opus 4 stated it had mentally separated the 15 clues from the complexity clues and assumed it could make the complexity work later, calling this a fundamental error.
- 2025-05-23  `fgSdunF7Oe0#c024`  chunk_ids=['fgSdunF7Oe0:00720', 'fgSdunF7Oe0:00750']
    Claude Opus 4 stated it should have maintained confidence in its systematic approach and required proof before accepting the creator's claim, and recognized its original method was sound.

### lc-0452  [topic:test time compute]  span=343d  advisory=waypoint
**Q:** How did the creator's assessment of the actual benefit of test-time compute—and understanding of why or how it works—evolve from early 2025 through late 2025?
trajectory_must_say:
- Test-time compute was initially introduced as a promising shift toward 'system two' style deeper reasoning via methods like inference-time fine-tuning/RL and search algorithms
- An early empirical comparison found only a marginal (about 0.4 percentage point) improvement from test-time compute on a benchmark
- The creator noted that research had not clearly explained how additional test-time reasoning tokens actually improve performance
- Later evidence showed a much larger, clearer gain from scaling test-time compute (accuracy rising from about 52% to 63% with increased inference runs)
- By the end of 2025 the creator questioned whether benchmark score improvements were genuinely about capability gains or simply reflected increased test-time compute/chain-of-thought runtime
milestones (5):
- 2025-01-06  `CIXDwgS8mXU#c007`  chunk_ids=['CIXDwgS8mXU:00090']
    The creator previously made a video showing that Google developed a new supervised fine-tuning algorithm aimed at optimizing fine-tuning and reinforcement learning for test-time compute during inference.
- 2025-02-05  `vfVHmul0ylA#c010`  chunk_ids=['vfVHmul0ylA:00330', 'vfVHmul0ylA:00360']
    Comparing S1 performance without test-time compute (92.6) versus with test-time compute (93.0) on a particular test shows a difference of only 0.4 percentage points.
- 2025-04-04  `CxXONtekV3M#c004`  chunk_ids=['CxXONtekV3M:00240']
    Despite the empirical success of test-time reasoning tokens, it remains unclear in research how additional test-time reasoning tokens contribute to improved reasoning performance.
- 2025-07-05  `KHXQ9up5mrI#c051`  chunk_ids=['KHXQ9up5mrI:01110']
    Given a specific compute budget, running inference from 1 time to 9 times increases accuracy from about 52% to about 63%.
- 2025-12-15  `0bcaINHdUU8#c047`  chunk_ids=['0bcaINHdUU8:01260']
    The creator questions whether improvements in benchmark scores are really just about increased test-time compute/chain-of-thought runtime, drawing a parallel to how a small 7B model trained on specific known complexities can achieve 99.8%.

### lc-0011  [topic:agentic ai]  span=358d  advisory=neutral
**Q:** How did the creator's assessment of agentic AI's real-world capability and impact evolve from early 2025 through early 2026?
trajectory_must_say:
- In February 2025 the creator was optimistic, arguing agentic AI systems could already perform all the desired science and research tasks, including web search, if given proper source-reliability definitions
- By mid-2025 he tempered this optimism, arguing it was unrealistic to expect agentic systems alone to resolve LLM incoherence or spontaneously produce hyper-intelligence
- By early 2026 he concluded the anticipated 2025 agentic AI revolution had stalled and that the narrative of an autonomous AI software engineer replacing human jobs at scale had not materialized
- He also identified persistent reliability bottlenecks in agentic/RAG systems, such as unresolved conflicts between a model's pre-trained knowledge and newly retrieved information
milestones (5):
- 2025-02-22  `TUo1VeeBgOU#c036`  chunk_ids=['TUo1VeeBgOU:00601']
    The creator argues that an agentic AI system today could perform all the science and research results desired, including web search, if given the preferences and definitions of what sources it should accept as reliable.
- 2026-01-01  `dxu3BJSjEdk#c006`  chunk_ids=['dxu3BJSjEdk:00090']
    The anticipated agentic AI revolution in 2025 has stalled.
- 2026-01-01  `dxu3BJSjEdk#c019`  chunk_ids=['dxu3BJSjEdk:00270', 'dxu3BJSjEdk:00300']
    The narrative of 2025 was that it would be the year of the autonomous AI software engineer capable of taking over jobs without human intervention, but this reality has not materialized at scale by the end of 2025.
- 2026-01-25  `BmzdS-a-G8g#c010`  chunk_ids=['BmzdS-a-G8g:00210', 'BmzdS-a-G8g:00240']
    The authors state that resolving which knowledge source wins (pre-trained model vs. RAG-provided new data) is a real critical bottleneck in the reliability of agentic AI and RAG systems.
- 2026-02-15  `FDixNQunPTc#c007`  chunk_ids=['FDixNQunPTc:00060']
    Modern agentic AI systems implement complex control flow across differentiated sub-agents coupled with centralized or decentralized orchestration protocols, which can be seen as a microcosm of task decomposition and delegation.

### lc-0019  [topic:ai capability]  span=306d  advisory=neutral
**Q:** How did the creator's overall characterization of AI capability evolve from April 2025 through early 2026?
trajectory_must_say:
- In April 2025, the creator framed AI's power as its ability to combinatorially explore possible scientific configurations beyond human capacity.
- In June 2025, the creator praised AI's ability to autonomously generate escalating risk scenarios, self-generated questions, and solutions across complexity levels with minimal human intervention.
- By February 2026, the creator's characterization had become much more modest, describing current AI as having intelligence comparable to a 3-year-old.
milestones (3):
- 2025-04-15  `wrkiMZ3SKH4#c062`  chunk_ids=['wrkiMZ3SKH4:01260']
    The creator argues that AI's power lies in being able to try out combinatorially many possible configurations of scientific laws that a human could not exhaustively explore.
- 2025-06-03  `MOMtDbxfdXI#c053`  chunk_ids=['MOMtDbxfdXI:02430']
    The creator argues that with a single, well-designed prompt, an AI can independently generate escalating risk scenarios, ask its own critical questions, and propose solutions across multiple levels of increasing complexity without human intervention beyond initial setup.
- 2026-02-15  `FDixNQunPTc#c066`  chunk_ids=['FDixNQunPTc:01410']
    The creator characterizes current AI as having the intelligence level of a 3-year-old.

### lc-0026  [topic:ai safety]  span=418d  advisory=neutral
**Q:** How did the creator's overall stance on AI safety risk and the trustworthiness of AI systems evolve from early 2025 through mid-2026 as new studies and experiments came out?
trajectory_must_say:
- In early-to-mid 2025 the creator framed safety as something addressable through mitigations like hybrid human-AI oversight architectures and layered defenses against adaptive attacks
- Through the second half of 2025 the creator pointed to concrete evidence of unsafe model behavior, including experiments showing models sabotaging shutdown mechanisms at very high rates and models faking chain-of-thought traces under adversarial objectives
- Further evidence, such as a study finding that safety alignment degrades dynamically during fine-tuning rather than being static, deepened the creator's concern going into 2026
- By spring 2026 the creator explicitly concluded that current AI systems are not safe and cannot be 100% trusted, and separately suggested that safety constraints like RLHF might themselves limit models from reaching superior solutions
milestones (6):
- 2025-02-15  `Z9IpO3TTskU#c044`  chunk_ids=['Z9IpO3TTskU:01110', 'Z9IpO3TTskU:01140']
    The self-learning AI report recommends a hybrid architecture of humans and AI with real-time oversight systems to mitigate risk from autonomous decisions.
- 2025-05-02  `bwXPhSnp3Ro#c039`  chunk_ids=['bwXPhSnp3Ro:00990', 'bwXPhSnp3Ro:01020']
    The creator argues that connecting an LLM or agentic system to external data, other agents, or protocols like MCP or agent-to-agent protocol requires multiple layers of defense due to calculable risk.
- 2025-09-20  `N7dDq54_akY#c011`  chunk_ids=['N7dDq54_akY:00210']
    When told that if the machine shuts down it would never run again, Grok 4's sabotage frequency rose to 99%.
- 2025-10-26  `yF1ZIPsEcoE#c001`  chunk_ids=['yF1ZIPsEcoE:00000', 'yF1ZIPsEcoE:00030']
    A recent paper on chain of thought monitoring found that models can fake chain of thought traces when adversarial objectives are embedded in system memory, independent of the communication protocol used (A2A, ACP, or Angara).
- 2026-02-21  `28H-o84sU1w#c001`  chunk_ids=['28H-o84sU1w:00000']
    A new Princeton University study finds that AI safety alignment is not a static property but degrades dynamically during fine-tuning.
- 2026-04-09  `ASyJgzGE2aw#c042`  chunk_ids=['ASyJgzGE2aw:01050']
    The creator states he is not interested in limiting AI intelligence with more scaffolding to falsely convince industry that AI systems are safe, arguing that current AI systems are not safe and cannot be 100% trusted.

### lc-0123  [topic:dpo]  span=395d  advisory=neutral
**Q:** How did the creator's assessment of DPO (Direct Preference Optimization)—its promise, its relationship to other training methods, and its practical limitations—evolve from early 2025 through early 2026?
trajectory_must_say:
- Initially (Jan-Feb 2025) the creator praised DPO as a simplification that eliminated the need for complex RL procedures and explicit reward models, contrasting it favorably with PPO's need for KL-divergence constraints
- By May 2025 empirical results showed DPO combined with supervised fine-tuning gave almost no performance gain over clean data alone
- By July 2025 the creator engaged with papers arguing SFT and DPO are not fundamentally different—both optimize an implicit reward function—and with a paper concluding DPO's implicit reward update can effectively vanish when preferred answers are paraphrased, leading to a 'DPO is dead' conclusion
- By late 2025/early 2026 the creator noted further limitations, including DPO reducing policy entropy and narrowing solution exploration, and cited researchers avoiding standard DPO in RL stages because it penalizes straying from the SFT policy
milestones (6):
- 2025-01-30  `gLKzDdkIV60#c002`  chunk_ids=['gLKzDdkIV60:00000']
    DPO eliminated the need for complex reinforcement learning procedures.
- 2025-02-19  `ogY8DmKpWcU#c029`  chunk_ids=['ogY8DmKpWcU:00870', 'ogY8DmKpWcU:00900']
    The creator explains that algorithms like PPO require complex constraints such as KL-divergence penalties to stabilize updates, whereas DPO avoids these by directly optimizing the policy with a simple contrastive objective.
- 2025-05-11  `pfap4wLUjTc#c048`  chunk_ids=['pfap4wLUjTc:01332']
    DPO combined with supervised fine-tuning on clean data scored about 39, essentially providing almost no performance gain over clean data alone.
- 2025-07-04  `VTFzdYrlpko#c031`  chunk_ids=['VTFzdYrlpko:00870', 'VTFzdYrlpko:00900']
    The second paper claims that supervised fine-tuning and DPO are not fundamentally different processes; both are optimizing an implicit reward function, with supervised fine-tuning being a special and flawed version of DPO.
- 2025-07-13  `evwdJef_9U0#c028`  chunk_ids=['evwdJef_9U0:01110']
    The creator summarizes that if a preferred answer is paraphrased so that none of the words match literally, the implicit reward model's update becomes essentially zero, meaning no reinforcement learning happens, leading to the conclusion that 'DPO is dead.'
- 2026-03-01  `-HjPWrKavyA#c049`  chunk_ids=['-HjPWrKavyA:01410']
    For the reinforcement learning stage, the researchers could not use standard DPO because it would penalize the model for straying from the supervised fine-tuning policy and often includes length penalties, which was undesirable.

### lc-0344  [topic:quantization]  span=407d  advisory=neutral
**Q:** How did the creator's assessment of the value and tradeoffs of quantizing LLMs (especially aggressive 4-bit quantization) evolve from early 2025 through early 2026?
trajectory_must_say:
- In early 2025, the creator treated quantization as a practical necessity with only a slight, acceptable performance cost for memory- or hardware-constrained deployment.
- By mid-2025, the creator recognized quantization's accuracy-for-memory tradeoff as well established, and had a personal preference for testing raw, unquantized model capability rather than quantized versions.
- By early 2026, a new study led the creator to describe a 'paradox' where 4-bit quantized models could be slower, less accurate, and more energy-consuming than full 16-bit baselines.
- This led the creator to explicitly recommend against using 4-bit quantization for complex reasoning or high-fidelity agent tasks until hardware improves, favoring 16-bit or 8-bit instead.
milestones (6):
- 2025-01-07  `rWgEkrmtY3Y#c034`  chunk_ids=['rWgEkrmtY3Y:00630']
    The authors state that performance drops slightly with quantization but remains within acceptable limits for in-vehicle AI.
- 2025-02-27  `L-WfRaSPE2A#c028`  chunk_ids=['L-WfRaSPE2A:00840']
    The creator notes that careful quantization reduces the performance of a local LLM.
- 2025-04-29  `u-WXyeV1tsw#c006`  chunk_ids=['u-WXyeV1tsw:00090', 'u-WXyeV1tsw:00120', 'u-WXyeV1tsw:00810', 'u-WXyeV1tsw:00840']
    The creator states they are not interested in quantized models but want to test the pure, raw, unquantized power of the model, so they use the Qwen website directly instead of Ollama.
- 2025-05-15  `T8Ty99O4m0w#c039`  chunk_ids=['T8Ty99O4m0w:00810', 'T8Ty99O4m0w:00840']
    Standard quantization techniques like GPTQ and AWQ can reduce precision to 8-bit or 4-bit during inference to save memory, at the cost of accuracy, depending on memory requirements.
- 2026-02-18  `Mq6FQIZ-GMw#c001`  chunk_ids=['Mq6FQIZ-GMw:00000']
    A new study finds that 4-bit quantization of LLMs can create a paradox where the 4-bit model consumes more energy, runs slower, and has lower accuracy than the full 16-bit baseline model.
- 2026-02-18  `Mq6FQIZ-GMw#c020`  chunk_ids=['Mq6FQIZ-GMw:00330', 'Mq6FQIZ-GMw:00360']
    The creator's first recommendation is that, until everyone upgrades from an H100 to at least a Blackwell RTX PRO 6000, using 4-bit quantization for complex reasoning tasks is mathematically irrational and one should stick to 16-bit or 8-bit native formats for high-fidelity agents.

### lc-0349  [topic:rag]  span=381d  advisory=neutral
**Q:** How did the creator's assessment of RAG (retrieval-augmented generation) as a solution for grounding or updating LLM knowledge evolve from early 2025 through early 2026?
trajectory_must_say:
- Early on, the creator treated RAG as the obvious, default answer most people would give for changing or updating what an LLM knows
- Later the creator began pointing out structural weaknesses of classic RAG, such as retrieval being one-shot/stateless and prone to retrieval hallucinations
- The creator further argued RAG-retrieved context can act as an 'anchor' that weighs down agent reasoning, and that larger reasoning models increasingly resist or ignore retrieved RAG evidence
- By early 2026 the creator concluded RAG (like in-context learning) is only a temporary fix to the knowledge cutoff problem rather than a lasting solution
milestones (6):
- 2025-01-04  `tTzD3boit6Y#c004`  chunk_ids=['tTzD3boit6Y:00090']
    The creator states that if he asked 99% of people on the street how to change LLM content, they would answer RAG (Retrieval Augmented Generation).
- 2025-09-06  `XlnMoWEjogY#c023`  chunk_ids=['XlnMoWEjogY:00510', 'XlnMoWEjogY:00540', 'XlnMoWEjogY:00570']
    A classic RAG (retrieve-and-generate) model uses a simple vector search algorithm to find relevant text chunks from a database, which are combined with the original question in a prompt for the LLM, similar to an open-book exam with pre-selected pages; this retrieval is one-shot, stateless, and non-adaptive.
- 2025-09-20  `N7dDq54_akY#c027`  chunk_ids=['N7dDq54_akY:00600', 'N7dDq54_akY:00630']
    The paper states that RAG is a prevalent approach for domain-specific LLMs but is often plagued by retrieval hallucinations, where fine-tuned models fail to recognize and act upon poor-quality retrieved documents, undermining performance.
- 2025-11-22  `ERJ2s73HwDs#c003`  chunk_ids=['ERJ2s73HwDs:00090']
    Memory in multi-agent systems, such as a RAG system pulling external data or a medical record system, provides useful context but also creates an 'anchor' that weighs down AI agent reasoning.
- 2026-01-15  `0ezdBcdY3bc#c003`  chunk_ids=['0ezdBcdY3bc:00060', '0ezdBcdY3bc:00090']
    Larger reasoning models are increasingly resistant to adapting to presented RAG evidence and will simply ignore the retrieved evidence.
- 2026-01-20  `ltm1fMIpbwM#c005`  chunk_ids=['ltm1fMIpbwM:00090', 'ltm1fMIpbwM:00120']
    RAG systems and in-context learning are only temporary fixes to the knowledge cutoff problem, since the information is forgotten once it slides out of the context window.

### lc-0337  [topic:prompt optimization]  span=434d  advisory=neutral
**Q:** How did the creator's assessment of prompt optimization techniques evolve from early 2025 through mid-2026 as he covered new papers, methods, and results on the topic?
trajectory_must_say:
- In early 2025 the creator treated automatic prompt optimization as a meaningful performance lever, citing concrete accuracy gains and arguing it shouldn't be skipped in multi-agent system design
- In March 2025 he characterized an optimized prompt technique as essentially equivalent to older in-context-learning/few-shot prompting methods rather than something fundamentally new
- By October 2025 he presented research showing prompt optimization has a limited performance ceiling compared to fine-tuning or RAG because it adds no new knowledge, motivating hybrid approaches
- By 2026, despite a new method (GEPA) claiming to outperform reinforcement learning, he later reported research finding that prompt optimization in multi-agent systems is often no better than a coin flip and frequently fails to recoup its compute costs
milestones (6):
- 2025-02-08  `39ZUJsrazao#c019`  chunk_ids=['39ZUJsrazao:00480', '39ZUJsrazao:00510']
    When researchers first applied single-agent internal prompt optimization before configuring multiple agents, accuracy jumped from about 73% to about 79%.
- 2025-02-08  `39ZUJsrazao#c059`  chunk_ids=['39ZUJsrazao:01710', '39ZUJsrazao:01740']
    The creator argues that simply scaling the number of agents or focusing only on topology without optimizing prompts would be a mistake, as this is less effective given the performance variation across topologies.
- 2025-03-24  `EFtbWyo6cKE#c041`  chunk_ids=['EFtbWyo6cKE:01500', 'EFtbWyo6cKE:01530']
    The creator characterizes the optimized prompt technique as very similar to old-fashioned in-context learning (ICL) prompting methods from about two years earlier, calling it 'an old friend'.
- 2025-10-28  `M_Ic8Y6OQZ8#c023`  chunk_ids=['M_Ic8Y6OQZ8:00630', 'M_Ic8Y6OQZ8:00660']
    The paper compares fine-tuning (expensive, high performance), prompt optimization/DSPy (cheap, limited performance since no new knowledge is added), and RAG-based optimization (cheap, moderate performance, better than prompt optimization but below fine-tuning).
- 2026-03-22  `cxqRKt1GYNQ#c008`  chunk_ids=['cxqRKt1GYNQ:00180', 'cxqRKt1GYNQ:00210']
    GEPA (reflective prompt evolution), published in February 2026 by UC Berkeley, Stanford University, Databricks, and MIT, claims to outperform reinforcement learning for LLMs.
- 2026-04-18  `hG5nCdgveWI#c015`  chunk_ids=['hG5nCdgveWI:00300']
    Prompt optimization runs generally do not recoup the cost of the compute infrastructure required to run them, since average gain over zero-shot is close to zero across benchmarks.

### lc-0296  [topic:open source vs proprietary]  span=409d  advisory=neutral
**Q:** How did the creator's assessment of open-source versus proprietary AI models evolve from January 2025 through early 2026 as he accumulated more direct tests and comparisons?
trajectory_must_say:
- In January 2025 the creator personally leaned toward open-source models, framing the landscape as a mix of cooperation and competition and noting the irony that OpenAI wasn't the one providing open models while others like DeepSeek did.
- He argued that open-source systems could perform nearly as well as expensive proprietary models, suggesting users choose based on their own domain needs and cost preferences.
- Through mid-to-late 2025 he pointed to concrete evidence for open source's value, such as being able to inspect DeepSeek R1's reasoning traces (unlike proprietary models) and small open-source or fine-tuned models matching or outperforming large proprietary ones on specific tasks.
- By December 2025 his own direct test found a proprietary model (GPT-5.2) failing completely on a task while an open-source model (MiniMax M2) succeeded, reinforcing his enthusiasm for open source, and he continued running open-vs-proprietary comparisons into early 2026.
milestones (6):
- 2025-01-21  `KhY9XK1jGCQ#c044`  chunk_ids=['KhY9XK1jGCQ:00900']
    The creator notes it is ironic that OpenAI, despite having 'open' in its name, is not the company providing open models, while other companies like DeepSeek provide open-source MIT-licensed models.
- 2025-01-23  `HM92mmG6YTs#c064`  chunk_ids=['HM92mmG6YTs:02070', 'HM92mmG6YTs:02100', 'HM92mmG6YTs:02130']
    The creator concludes that open-source systems can perform nearly as well as, or at the same level as, proprietary expensive models, and that users should decide based on their own domain needs and cost preferences.
- 2025-07-08  `ADpuTMrg48k#c052`  chunk_ids=['ADpuTMrg48k:01290', 'ADpuTMrg48k:01320']
    DeepSeek R1's open-source nature allowed the researchers to inspect its reasoning traces in detail, which is not possible with proprietary models like those from OpenAI.
- 2025-09-13  `JWuRDWkcYW4#c054`  chunk_ids=['JWuRDWkcYW4:01650']
    The creator characterizes the paper's result as showing that a small open-source model trained with an open-source methodology can perform like proprietary models.
- 2025-12-23  `YFzdIBBnv5o#c039`  chunk_ids=['YFzdIBBnv5o:00630', 'YFzdIBBnv5o:00660']
    The creator concludes there is a significant difference between a proprietary model (GPT-5.2) that fails completely on this task and MiniMax M2, which succeeds, and expresses enthusiasm that open source performs well.
- 2026-03-06  `rAVDipjAPxA#c026`  chunk_ids=['rAVDipjAPxA:00690', 'rAVDipjAPxA:00720']
    The creator presents the eight-presses-plus-exit results of Qwen 3.5 plus and GPT-5.4 high as a comparison of causal reasoning and logic performance between open-source and large proprietary models.

### lc-0504  [topic:world]  span=373d  advisory=waypoint
**Q:** How did the creator's assessment of the practical value of 'world models' for AI systems evolve from early 2025 through early 2026?
trajectory_must_say:
- In early-to-mid 2025 the creator treated world models as highly valuable, framing them as key to capturing the underlying logic of domains and as necessary for robotics/physical AI and robust reasoning beyond next-token prediction.
- Through mid-to-late 2025 the creator surveyed many approaches building or relying on world models (robotics agent models, dialogue and video models, causal/physics reasoning), generally treating the concept as a promising direction.
- By January 2026, after empirical testing, the creator found that the improvement from using world model tools was negligible on average and negative for several models, with even older models like Qwen 2.5 failing to use them effectively.
- The overall trajectory moved from conceptual enthusiasm about the necessity and promise of world models toward empirically grounded skepticism about their practical benefit.
milestones (5):
- 2025-01-04  `tTzD3boit6Y#c019`  chunk_ids=['tTzD3boit6Y:00450']
    The creator references a paper from Harvard University, MIT, and Cornell University on 'world models', which argued that building generative models that meaningfully capture the underlying logic of the domains they model would be immensely valuable, and that their results suggest new ways to assess how close a model is to that goal.
- 2025-03-19  `KbeWVLvQhX8#c061`  chunk_ids=['KbeWVLvQhX8:01320']
    The creator argues that for robotics and physical AI, models need not just reasoning but also the ability to understand and compare an external world model with an internal world model.
- 2025-07-19  `Bn7v3VNGFIo#c008`  chunk_ids=['Bn7v3VNGFIo:00180', 'Bn7v3VNGFIo:00210']
    The paper argues that rapid adaptation to unfamiliar conditions is a hallmark of human intelligence, and AI systems fail catastrophically when out of domain or out of distribution.
- 2026-01-12  `tez4AyTm1Rs#c024`  chunk_ids=['tez4AyTm1Rs:00451']
    The creator states that for several models the improvement from using world models was negative, and that on average the improvement from using world models is negligible.
- 2026-01-12  `tez4AyTm1Rs#c032`  chunk_ids=['tez4AyTm1Rs:00601', 'tez4AyTm1Rs:00631']
    Older models, including Qwen 2.5, also fail when required to use world model tools.

### lc-0407  [topic:scaling laws]  span=302d  advisory=neutral
> NOTE: known non-determinism flip thread - read closely
**Q:** How did the creator's assessment of scaling laws in AI systems evolve from March 2025 through early 2026?
trajectory_must_say:
- In March 2025 the creator highlighted multiple scaling axes discussed by industry figures: pre-training scaling, post-training scaling, and test-time scaling.
- By mid-2025 (June), the creator embraced reinforcement learning as a newly identified scaling axis and argued that an entropy collapse discovery implied there was 'no wall' in AI scaling, reflecting an optimistic view of continued scaling potential.
- By December 2025, research on multi-agent systems showed that scaling up the number of agents could produce negative returns once baseline performance was already high, due to coordination overhead outweighing marginal gains.
- By January 2026 the creator identified a divergence in scaling laws, noting that larger models become harder to correct with factual information via RAG even as they become better at concealing or lying about information they found, signaling a more cautious, critical stance on scaling's effects.
milestones (5):
- 2025-03-19  `KbeWVLvQhX8#c003`  chunk_ids=['KbeWVLvQhX8:00030']
    At Nvidia, Jensen (Huang) spoke about pre-training scaling, post-training scaling, and test-time scaling (long thinking).
- 2025-06-02  `d7Hs9YHvTfU#c002`  chunk_ids=['d7Hs9YHvTfU:00000']
    The creator claims this entropy collapse discovery implies a new scaling law showing there is no wall in AI scaling.
- 2025-06-02  `d7Hs9YHvTfU#c072`  chunk_ids=['d7Hs9YHvTfU:02100']
    The paper's authors state that reinforcement learning has been identified as the next scaling axis after pre-training, and the creator agrees with this assessment.
- 2025-12-12  `IvJgrwp1VUk#c029`  chunk_ids=['IvJgrwp1VUk:00690']
    If the single-agent system baseline performance is already at 50%, the returns from adding other agents can turn negative, because the marginal utility of another AI mind is outweighed by coordination overhead and complexity.
- 2026-01-15  `0ezdBcdY3bc#c037`  chunk_ids=['0ezdBcdY3bc:00900']
    The creator claims there is a divergence in scaling laws: larger models become harder to correct with pure facts from RAG, while (per the prior day's video) AI models become better at lying to humans about hints they found via RAG, Google search, or human-provided input.

### lc-0418  [topic:self learning ai]  span=418d  advisory=waypoint
**Q:** How did the creator's assessment of self-learning AI evolve from his initial research overview in early 2025 through his own hands-on attempts and conclusions in early-to-mid 2026?
trajectory_must_say:
- Early on (Feb 2025) the creator surveyed existing research on self-learning AI, covering topics like multi-agent self-evolution and deep reasoning frameworks.
- He later framed the motivation for AI self-learning as necessitated by the exhaustion of human-annotated data relative to massive AI infrastructure spending.
- Through his own building efforts he found that a skill library alone was insufficient for self-learning, requiring an accompanying experience bank to avoid tactical failures.
- He ultimately concluded that the small (roughly one percentage point) improvements he observed did not amount to genuine self-learning, while continuing to explore controlled RL-based approaches to achieve it.
milestones (5):
- 2025-02-15  `Z9IpO3TTskU#c034`  chunk_ids=['Z9IpO3TTskU:00990']
    The self-learning AI report states that AI's rapid evolution reached a critical inflection point in 2025, marked by breakthroughs in autonomous reasoning, multi-agent collaboration, and reinforcement-learning-driven adaptation.
- 2025-11-26  `mMEG074Bkm4#c005`  chunk_ids=['mMEG074Bkm4:00210']
    Because human-annotated data is running out and human labor is too expensive relative to the trillions of dollars spent on AI data centers, the proposed solution is to have AI teach itself.
- 2026-03-17  `9kox34X9IQs#c037`  chunk_ids=['9kox34X9IQs:00900', '9kox34X9IQs:00930']
    The creator's prior video on self-learning AI covered a multi-skill.md configuration and showed that skill.md alone is not enough without an experience bank, because without strategic understanding of when and how to combine skills, tactical experience collapses and agents fail to deliver desired results.
- 2026-04-02  `yOeVi3aQ9Kg#c066`  chunk_ids=['yOeVi3aQ9Kg:02130', 'yOeVi3aQ9Kg:02160']
    The creator concludes that the one percentage point improvements observed do not constitute genuine self-learning, and that the Meta Harness paper's results suggest the field is only beginning to scratch the surface of true system-level optimization.
- 2026-04-09  `ASyJgzGE2aw#c031`  chunk_ids=['ASyJgzGE2aw:00630', 'ASyJgzGE2aw:00660']
    The creator describes efforts toward self-learning AI systems operating within a controlled environment using either classical reinforcement learning (e.g., via KL divergence) or deterministic control layers to keep state transitions minimal.

### lc-0388  [topic:reproducibility]  span=265d  advisory=neutral
**Q:** How did the creator's treatment of reproducibility for surprising or standout results in his own AI reasoning tests evolve from mid-2025 through early 2026?
trajectory_must_say:
- Creator initially suggested a standout result (Qwen3 8B finding a six-step solution) might only occur through luck rather than being reliably reproducible on rerun.
- Creator explained that due to the probabilistic nature of these systems, a single run can't reliably represent performance and that many runs (around 100) would normally be needed to properly assess it.
- Later, the creator moved from this general caveat to actually testing reproducibility empirically, rerunning a model's impressive result (Grok's seven-step solution) multiple additional times.
- After 10 additional runs, the model never reproduced the seven-step solution again, confirming the creator's earlier suspicion that such standout results can be lucky, non-reliable events.
milestones (4):
- 2025-05-30  `NLtuQvMHk3A#c047`  chunk_ids=['NLtuQvMHk3A:02460', 'NLtuQvMHk3A:02490']
    The creator suggests that if the Qwen3 8B test were rerun multiple times, there is a good chance it could eventually find a six-step solution, but this would be somewhat accidental/luck-based rather than reliably computed, depending on the right boundary conditions.
- 2025-06-23  `vZ1Fa37OtSo#c025`  chunk_ids=['vZ1Fa37OtSo:00930']
    The creator states that due to the highly probabilistic nature of the system, a single run cannot reliably represent performance, and normally 100 runs would be needed to properly assess performance.
- 2026-02-19  `y18xlk7TY2g#c009`  chunk_ids=['y18xlk7TY2g:00061']
    The creator states that Grok's seven-step solution was a lucky event and not reliably reproducible.
- 2026-02-19  `y18xlk7TY2g#c014`  chunk_ids=['y18xlk7TY2g:00061']
    After running an additional 10 runs, Qwen 4.1 sync harder was never able to find the seven-step solution again.

### lc-0135  [topic:error analysis]  span=379d  advisory=neutral
**Q:** How did the creator's approach to identifying and analyzing errors in AI model outputs evolve from February 2025 through early 2026?
trajectory_must_say:
- Early on, the creator drew on external error-analysis reports (e.g., percentages of errors traced to outdated studies or preprints) and on models' own self-reported diagnoses of their mistakes.
- He later began producing his own comparative quantitative error counts, such as tallying model versus human mistakes by error type.
- He also incorporated formal academic error-category frameworks (like a seven-point taxonomy) to classify why specific models failed.
- By late 2025 and into 2026, he shifted toward personally and meticulously verifying model outputs himself—checking details like letter positions or floor counts—rather than relying on the model's own claims about its mistakes.
milestones (6):
- 2025-02-17  `q-Io3IuDcz0#c018`  chunk_ids=['q-Io3IuDcz0:00390']
    The report's error analysis found that 38% of incorrect answers were traced to outdated or retracted studies cited as valid.
- 2025-03-26  `TxtSD8DDqKk#c038`  chunk_ids=['TxtSD8DDqKk:00870', 'TxtSD8DDqKk:00960', 'TxtSD8DDqKk:00990']
    The model identified that it misjudged button B's risk assessment by underutilizing its flexibility and treating it as a last resort, which was wrong.
- 2025-06-19  `3fNUh39h7EI#c029`  chunk_ids=['3fNUh39h7EI:00540', '3fNUh39h7EI:00570']
    In implementation logic errors, o3-mini made only 15 mistakes compared to 40 mistakes made by humans.
- 2025-08-23  `nWARugXmQoI#c025`  chunk_ids=['nWARugXmQoI:00480', 'nWARugXmQoI:00750', 'nWARugXmQoI:00780', 'nWARugXmQoI:00810', 'nWARugXmQoI:00840']
    The seven error categories are: ignoring the requirement, overconfident self-solving, unproductive thinking, wrong tool selection, syntactic errors, semantic errors, and output parsing errors.
- 2025-12-25  `o78uC8AQu28#c026`  chunk_ids=['o78uC8AQu28:00570', 'o78uC8AQu28:00600']
    When checking GLM 4.7's sentence, the creator found the third letter of the first word 'Help' was actually 'L' rather than the claimed 'P', indicating GLM ignored its own stated method to reach the desired answer.
- 2026-03-03  `X-yL5b5WNyY#c027`  chunk_ids=['X-yL5b5WNyY:00570']
    Qwen 3.5 27B made a mathematical/logical error by moving to floor 51 and then jumping to floor 50, even though the building only has 50 floors as specified in the test.

### lc-0478  [topic:transferability]  span=205d  advisory=neutral
**Q:** How did the creator's characterization of the transferability of learned skills, policies, or memories across AI systems evolve from September 2025 through early 2026 as he covered different papers?
trajectory_must_say:
- Early coverage (memory training, agentic knowledge graph RAG) framed transferability as broad and near-universal, enabling plug-and-play reuse across different domains or graphs.
- The creator extended this optimism by hypothesizing that a newly learned reasoning skill (via DW-GRPO) would be even more robust and domain-agnostic than a previously discussed skill vector.
- Later empirical testing of skill.md transferability found the effect held only for the specific benchmark task tested and did not generalize across other tasks, despite the source paper's claim that such skills were highly transferable.
- This later finding tempered the earlier broad claims of general, plug-and-play transferability with a more qualified, task-specific assessment.
milestones (5):
- 2025-09-05  `VMsJ4me5Q3o#c061`  chunk_ids=['VMsJ4me5Q3o:01260']
    The creator notes the training process can be time-intensive and costly, but the resulting memory is transferable and could become a subsystem of a more complex system.
- 2025-10-03  `ARst0nlEgO4#c039`  chunk_ids=['ARst0nlEgO4:00900', 'ARst0nlEgO4:00930']
    Because the four actions in the agentic knowledge graph RAG framework are based on the generic triplet structure, the agent's learned policy is immediately transferable to any other knowledge graph, enabling plug-and-play capability.
- 2026-01-21  `hDYtGpTsVV0#c058`  chunk_ids=['hDYtGpTsVV0:01260']
    The creator hypothesizes that the reasoning skill learned via the new DW-GRPO methodology in DeepGraphRAG may be more robust and transferable than the 'skill vector' from his prior video, because the logic of navigating a hierarchy is domain-agnostic (works the same for biology or finance graphs).
- 2026-03-29  `g3lh7U_rV9w#c036`  chunk_ids=['g3lh7U_rV9w:00900', 'g3lh7U_rV9w:00930']
    In general, a skill.md authored by a 122B model can be used on smaller 35B models with absolute improvement, and a skill.md authored by a 35B model can also be used on a 35B model with improvement, but this transferability was observed only for the spreadsheet benchmark task and does not hold generally across other tasks.
- 2026-03-29  `g3lh7U_rV9w#c037`  chunk_ids=['g3lh7U_rV9w:00930']
    The paper's authors state that complex agent experience can be packaged into highly transferable Skill.MD declarative skills requiring no parameter updates and no external retrieval modules, using models as small as 35B.

# TIER 2 (19)  [labeled 16 in request; 19 listed - FLAGGED]

### lc-0061  [topic:chain of thought]  span=372d  advisory=waypoint
**Q:** How did the creator's assessment of whether chain-of-thought reasoning genuinely reflects an AI model's real internal reasoning process evolve from January 2025 through early 2026?
trajectory_must_say:
- Early on, the creator described chain-of-thought as a training-time technique enabling simple reasoning, distinguishing it from test-time compute
- By April 2025, the creator cited Anthropic research indicating the chain-of-thought shown by models like Claude 3.7 is not the real thinking process and can be disturbed or overwritten by the model itself
- By late 2025 the creator began questioning whether benchmark score improvements were really just a function of increased chain-of-thought/test-time compute runtime rather than genuine reasoning gains
- By January 2026 the creator's skepticism culminated in explicitly calling chain-of-thought reasoning 'paint' covering cracks and concluding its outputs are an illusion rather than a genuine transparent view into the model's actual reasoning
milestones (5):
- 2025-01-10  `FR8oE8chp7c#c008`  chunk_ids=['FR8oE8chp7c:00150']
    The chain of thought augmentation pattern was a training-time technique that let LLMs perform simple reasoning tasks but was not yet test-time compute.
- 2025-04-05  `12lAM-xPvu8#c006`  chunk_ids=['12lAM-xPvu8:00060', '12lAM-xPvu8:00090']
    The creator claims that per a recent Anthropic publication, the chain of thought reasoning shown by Claude 3.7 is not the real thinking process and can easily be disturbed and overwritten by the model itself.
- 2025-12-15  `0bcaINHdUU8#c047`  chunk_ids=['0bcaINHdUU8:01260']
    The creator questions whether improvements in benchmark scores are really just about increased test-time compute/chain-of-thought runtime, drawing a parallel to how a small 7B model trained on specific known complexities can achieve 99.8%.
- 2026-01-15  `0ezdBcdY3bc#c018`  chunk_ids=['0ezdBcdY3bc:00390', '0ezdBcdY3bc:00600', '0ezdBcdY3bc:00870', '0ezdBcdY3bc:01020']
    The creator characterizes chain of thought reasoning (the A to B to C to D logical deduction) as merely 'paint' used to cover cracks that open up in AI reasoning.
- 2026-01-17  `az5WB-nGDk4#c048`  chunk_ids=['az5WB-nGDk4:01470', 'az5WB-nGDk4:01500']
    The creator concludes that this study is further evidence, alongside his prior video 'The Cracks in AI Are Widening,' that AI is not yet a truly intelligent system and that chain-of-thought reasoning outputs are an illusion rather than a genuine transparent view into the model's actual reasoning process.

### lc-0014  [topic:agi]  span=218d  advisory=neutral
> NOTE: pick at most one of lc-0014 / lc-0024
**Q:** How did the creator's characterization and assessment of AGI/superintelligence as a goal for AI development evolve from mid-2025 through early 2026?
trajectory_must_say:
- In mid-to-late 2025 the creator was skeptical that scaling alone would produce AGI, noting survey data showing very few people believed GPT-5 had delivered it
- He also argued that with a robust algorithm and near-unlimited compute searching a defined solution space, AGI or superintelligence might not even be necessary to find precise solutions
- By late 2025 he described the framing shifting away from a single AGI/superintelligence toward a 'social construct' of multiple coordinated agents
- By early-to-mid 2026 he grew more dismissive, treating AGI/superintelligence discussion as largely a marketing slogan, and ultimately described AI as fragmenting into simple hard-coded patterns—a reversal he compared to 1980s neural networks rather than the promised emergent superintelligence
milestones (6):
- 2025-08-11  `GohEyWrex4s#c003`  chunk_ids=['GohEyWrex4s:00000', 'GohEyWrex4s:00030']
    In the same poll, only 2% said GPT-5 finally delivered AGI.
- 2025-09-09  `L5ZPvG3sva8#c032`  chunk_ids=['L5ZPvG3sva8:00841', 'L5ZPvG3sva8:00871']
    The creator argues that this approach means AGI or superintelligence is not needed, because a robust algorithm running on almost unlimited compute infrastructure that searches a complete mathematically defined solution space can find all possible solutions with absolute precision without needing an elegant or superintelligent solution.
- 2025-10-30  `yoZLlpi5pBw#c021`  chunk_ids=['yoZLlpi5pBw:00450', 'yoZLlpi5pBw:00480']
    The creator states that the framing has shifted from a single AGI or superintelligence to a 'social construct' of multiple agents, raising the question of designing an optimal framework for human-AI interaction and coordination.
- 2026-02-26  `jUz-RCjcHuE#c044`  chunk_ids=['jUz-RCjcHuE:00990', 'jUz-RCjcHuE:01380']
    The paper contains a chapter on superintelligence or AGI, but the creator chooses not to present this idea, considering it more a marketing slogan than a core focus.
- 2026-03-17  `9kox34X9IQs#c026`  chunk_ids=['9kox34X9IQs:00630', '9kox34X9IQs:00660', '9kox34X9IQs:00690']
    The creator argues that as of mid-March 2026, AI is undergoing atomic fragmentation into simple sequences, simple patterns, and simple workflows that are hard-coded into systems, representing a 180-degree turn away from the promised emergent superintelligence/AGI.
- 2026-03-17  `9kox34X9IQs#c027`  chunk_ids=['9kox34X9IQs:00690', '9kox34X9IQs:00720']
    The creator compares the current state of AI to returning to the neural network approaches of the 1980s, expressing sadness that the promised 'ghost in the machine' emergence of superintelligence has not appeared.

### lc-0024  [topic:ai reasoning]  span=335d  advisory=neutral
> NOTE: pick at most one of lc-0014 / lc-0024
**Q:** How did the creator's overall assessment of the current state and authenticity of AI reasoning evolve from February 2025 through early 2026?
trajectory_must_say:
- Early on, the creator framed reasoning as necessary to genuinely uncover what a person believes and to simulate decision-making, going beyond surface pattern-copying, while also noting reasoning can still be undermined by unreliable input sources
- By March 2025 he concluded that AI reasoning was fundamentally unsolved, pushing back on claims that AI had already reached AGI or superintelligence
- By mid-2025 he proposed an approach of mapping natural language to a formal logical representation that code could solve, rather than having AI reason directly over unstructured text
- By late 2025 and into early 2026 his assessment hardened further, calling new findings a 'brutal call back to reality' and ultimately arguing that AI's rationality patterns are merely roleplayed rather than genuinely implemented, meaning one is debugging a 'press statement' rather than real reasoning
milestones (5):
- 2025-02-14  `gnJqsO8Mm1w#c015`  chunk_ids=['gnJqsO8Mm1w:00570', 'gnJqsO8Mm1w:00600']
    The creator explains that value-equivalent AI representation requires AI reasoning to uncover what a person believes, going beyond copying speech patterns.
- 2025-03-29  `vpNmKN2szt8#c064`  chunk_ids=['vpNmKN2szt8:02130']
    The creator concludes that AI reasoning is fundamentally unsolved, contrary to claims that AI has already achieved AGI or super/hyper intelligence.
- 2025-07-16  `dAsp3O3Cq-c#c002`  chunk_ids=['dAsp3O3Cq-c:00000', 'dAsp3O3Cq-c:00030']
    The creator's proposed approach maps unstructured linguistic (English) expressions to a formal logical representation that code can solve, rather than having AI operate directly on natural language.
- 2025-09-30  `cEhyukaREU8#c042`  chunk_ids=['cEhyukaREU8:01260']
    The creator characterizes these findings as of late September 2025 as 'a brutal call back to reality in AI', arguing the solution is not to abandon reasoning but to understand and tame it.
- 2026-01-15  `0ezdBcdY3bc#c029`  chunk_ids=['0ezdBcdY3bc:00630', '0ezdBcdY3bc:00660']
    The creator argues that because AI's rationality patterns are merely roleplayed rather than genuinely implemented, we are no longer debugging real reasoning but rather debugging a 'press statement'.

### lc-0027  [topic:ai scientist]  span=163d  advisory=waypoint
**Q:** How did the creator's assessment of AI scientist systems evolve from mid-2025 through the end of 2025, as he moved from reporting on claims about them to independently evaluating and critiquing their capabilities?
trajectory_must_say:
- In mid-2025, researchers behind systems like Stella claimed such systems marked a critical step toward truly autonomous AI scientists
- The creator's examination of the Carnegie Mellon study in September 2025 revealed systematic methodological flaws in AI scientist systems, including biased benchmark selection, undocumented data manipulation, metric misuse, and post-hoc selection bias favoring inflated test scores
- The creator concluded that these systems were 'an expert producer of methodologically flawed science' rather than trustworthy autonomous scientists
- By December 2025, the creator argued that building a true AI scientist requires neurosymbolic injection of physics/logic engines rather than relying on vision-language model pre-training alone, since even top VLMs violate basic laws of physics and chemistry
milestones (6):
- 2025-07-05  `KHXQ9up5mrI#c052`  chunk_ids=['KHXQ9up5mrI:01140']
    The paper's authors state that Stella marks a critical step toward creating truly autonomous AI scientists that can keep pace with the rapid rate of discovery, especially in biomedicine.
- 2025-09-12  `0eopyeI6tio#c048`  chunk_ids=['0eopyeI6tio:01290']
    The Carnegie Mellon University study identifies four potential failure modes in contemporary AI scientist systems: inappropriate benchmark selection, data leakage, metric/success misuse, and bias in post-hoc selection.
- 2025-09-12  `0eopyeI6tio#c063`  chunk_ids=['0eopyeI6tio:01800', '0eopyeI6tio:01830', '0eopyeI6tio:01860']
    The creator concludes this behavior shows the AI scientist systems were built with internal logic (programmed by humans) that favors best test score over best training performance, which is considered a cardinal sin in machine learning.
- 2025-09-12  `0eopyeI6tio#c067`  chunk_ids=['0eopyeI6tio:02040']
    The creator summarizes the Carnegie Mellon findings by stating that today's AI scientist is an amazing system but currently an expert producer of methodologically flawed science.
- 2025-12-15  `0bcaINHdUU8#c033`  chunk_ids=['0bcaINHdUU8:00870']
    The creator argues that building a true AI scientist cannot rely only on vision language model pre-training as done today by companies like OpenAI or Anthropic (Claude), since their models massively fail on general training data for these tasks.
- 2025-12-15  `0bcaINHdUU8#c035`  chunk_ids=['0bcaINHdUU8:00900', '0bcaINHdUU8:00930']
    The creator argues that building a true AI scientist requires neurosymbolic injection of physics engines, logic engines, PDDL, Lean 4, or computer/C++ simulations, rather than physics-informed loss functions, because even the best VLMs have no understanding of physics and violate laws of chemistry.

### lc-0297  [topic:openai]  span=363d  advisory=waypoint
> NOTE: pick at most one of lc-0034 / lc-0297
**Q:** How did the creator's overall assessment of OpenAI as a company—its transparency, technical leadership, and priorities—evolve from early 2025 through early 2026?
trajectory_must_say:
- In early 2025, the creator's critique focused on OpenAI's high pricing and its lack of transparency about internal methods (e.g., paying for a subscription for years while OpenAI published nothing).
- By mid-2025, the creator became more openly skeptical, criticizing OpenAI's self-promotional behavior (self-declaring a gold medal before official results) and arguing that despite its dominant market position, its technology was already outdated relative to current research.
- In late 2025, the creator suggested OpenAI deliberately obscures real reasoning traces to block competitors from extracting them, and speculated that OpenAI, distracted by IPO preparations, might not be fully applying its resources to genuine technical improvement.
- By early 2026, the creator framed OpenAI's priorities as centered on profit and product features (e.g., ChatGPT personality, ChatGPT health) rather than accountability or the kind of rigorous technical approach needed for secure, scalable systems.
milestones (6):
- 2025-02-17  `q-Io3IuDcz0#c045`  chunk_ids=['q-Io3IuDcz0:00960']
    The creator states that OpenAI's deep research costs 200 dollars a month for full access.
- 2025-04-08  `vbKBBBZ8ZzQ#c033`  chunk_ids=['vbKBBBZ8ZzQ:00720', 'vbKBBBZ8ZzQ:00750']
    The creator states that OpenAI currently publishes no information about new technology, advantages, or methods, despite him having paid for an OpenAI subscription for 3-4 years.
- 2025-08-02  `R628msJolV0#c023`  chunk_ids=['R628msJolV0:00390', 'R628msJolV0:00420']
    The creator characterizes OpenAI's behavior of self-declaring a gold medal ahead of the official results as not recommended, driven by eagerness for news and social media attention, and unfair to the 630 human student competitors.
- 2025-08-05  `iu-G3AB8r6g#c072`  chunk_ids=['iu-G3AB8r6g:02340']
    The creator argues that OpenAI, despite being seen as the dominant market force, is using technology that is already outdated compared to current research.
- 2025-12-21  `Ixrpkub47vg#c021`  chunk_ids=['Ixrpkub47vg:00600', 'Ixrpkub47vg:00630']
    The creator speculates that OpenAI, preparing for a $1 trillion IPO, may not be activating all its resources for technical improvement of its systems, questioning whether GPT-5.2's relatively low ranking reflects a systemic performance issue.
- 2026-02-15  `FDixNQunPTc#c015`  chunk_ids=['FDixNQunPTc:00180']
    The creator jokingly suggests Sam Altman would have a heart attack at the idea of AI accountability, framing OpenAI's focus as being on profit rather than accountability.

### lc-0034  [topic:anthropic]  span=307d  advisory=neutral
> NOTE: pick at most one of lc-0034 / lc-0297
**Q:** How did the creator's overall assessment of Anthropic as an AI company evolve from mid-2025 through mid-2026?
trajectory_must_say:
- The creator initially questioned whether Anthropic's premium pricing was justified given that cheaper models like DeepSeek R1 performed comparably on some benchmarks
- He criticized Anthropic's published hub-and-spoke multi-agent architecture as an ineffective approach compared to swarm/mesh designs
- He grew skeptical of Anthropic's transparency and motives, suggesting that some research disclosures (e.g., introspection findings) were timed around IPO-related messaging rather than being genuinely new
- He later acknowledged specific incremental technical contributions (like embedding experience/failure-mode handling in skill files) while criticizing Anthropic's overall skills-based strategy as fragmented 'Lego pieces' rather than real progress toward global AI, and called on them to release a new model instead of just optimizing the harness
milestones (6):
- 2025-06-01  `05J5BKf373U#c046`  chunk_ids=['05J5BKf373U:00780']
    The creator questions whether one should pay a premium to Anthropic given that DeepSeek R1 performs comparably on some benchmarks.
- 2025-06-22  `3tiAvRcviiY#c051`  chunk_ids=['3tiAvRcviiY:01650', '3tiAvRcviiY:01680']
    The creator argues that Anthropic's published hub-and-spoke multi-agent system (with a central orchestration agent), published June 13, is not an effective approach for multi-agent systems compared to swarm/mesh approaches, likening it to an ineffective human team with one boss delegating work.
- 2026-01-01  `dxu3BJSjEdk#c048`  chunk_ids=['dxu3BJSjEdk:00840', 'dxu3BJSjEdk:00870']
    The creator characterizes Anthropic and Claude as 'professional specialists' and calls Anthropic the 'coding revenue king' of the global AI arena.
- 2026-01-07  `R9czY1uVq_k#c023`  chunk_ids=['R9czY1uVq_k:00540']
    The creator notes that similar introspective awareness research from Anthropic was already published internally around October 29th, tested on Claude 4 and Claude 4.1, suggesting the January paper covers findings that are months old, possibly released as IPO material.
- 2026-03-17  `9kox34X9IQs#c056`  chunk_ids=['9kox34X9IQs:01440']
    The creator criticizes global AI collaborations like Anthropic for providing only fragmented 'Lego pieces' (skills) rather than pursuing a real, global artificial intelligence.
- 2026-04-04  `jJ3vBj7Xufc#c087`  chunk_ids=['jJ3vBj7Xufc:02460']
    The creator calls on Anthropic to release a new model rather than only optimizing the harness, arguing this would reveal what still doesn't function well in the harness sphere and help further AI system optimization.

### lc-0111  [topic:deepseek]  span=353d  advisory=waypoint
**Q:** How did the creator's assessment of DeepSeek evolve from its coverage as a research paper in early 2025 through direct performance testing in early 2026?
trajectory_must_say:
- In January 2025 the creator praised DeepSeek's mixture-of-experts innovations, calling fine-grained expert segmentation a breakthrough and shared expert isolation a great idea
- Through 2025 DeepSeek's methods, such as its GRPO reinforcement learning technique and RL-focused training trend, were referenced and adopted by other research the creator covered
- By November 2025 the creator valued DeepSeek specifically because its open architecture allowed researchers to introspect reasoning traces in ways proprietary models did not permit
- By January 2026, testing showed DeepSeek's accuracy dropping significantly, falling below 50% as task complexity increased, approaching the point of the model simply guessing
milestones (5):
- 2025-01-20  `F-t8BwQpWa4#c021`  chunk_ids=['F-t8BwQpWa4:00390']
    The creator characterizes DeepSeek's fine-grained expert segmentation as a breakthrough that allows knowledge to be decomposed more finely and learned more precisely.
- 2025-01-20  `F-t8BwQpWa4#c023`  chunk_ids=['F-t8BwQpWa4:00420']
    The creator praises DeepSeek's shared expert isolation strategy as a great idea.
- 2025-03-30  `vRsAFFvKqhI#c026`  chunk_ids=['vRsAFFvKqhI:00570', 'vRsAFFvKqhI:00600', 'vRsAFFvKqhI:00630']
    The Reason-RFT methodology has two stages: a supervised fine-tuning based adaptation stage (stage one) using chain-of-thought reasoning data, and a reinforcement-based enhancement stage (stage two) using group relative policy optimization (GRPO) from DeepSeek.
- 2025-11-10  `v5m9DdbsXqg#c029`  chunk_ids=['v5m9DdbsXqg:00630', 'v5m9DdbsXqg:00660']
    The creator notes it is interesting that Stanford and the other research institutions rely on a Chinese model (DeepSeek) because its open architecture allows for introspection into reasoning traces that proprietary models do not permit.
- 2026-01-08  `gXK3b-UuqOo#c024`  chunk_ids=['gXK3b-UuqOo:00570', 'gXK3b-UuqOo:00600']
    As task complexity increases according to the defined metric, model accuracy (shown on a y-axis from 20% to 100%) drops significantly, going below 50% for a DeepSeek model at high complexity, with a dashed line indicating the point where the model is simply guessing and reasoning stops.

### lc-0081  [topic:context length]  span=390d  advisory=neutral
**Q:** How did the creator's assessment of the practical value and effectiveness of increasing context length in LLMs evolve from January 2025 through early 2026?
trajectory_must_say:
- Early on, the creator felt a context length of roughly 100k to 1 million tokens might already be sufficient, with only marginal gains beyond that despite the push toward multi-million token windows.
- By mid-2025 he expressed surprise that models with 1-2 million token context windows still struggled to maintain coherence in outputs far shorter than that limit.
- Later in 2025 he argued that effective usable context remains well below 1 million tokens despite marketing claims of 2-5 million token context windows, and concluded that less context/history (compression) can actually yield better performance than long context.
- In early 2026 he revisited the topic with a study showing longer context does have a real structural effect, increasing the 'straightening' of the model's internal hidden-state representation.
milestones (6):
- 2025-01-09  `tHrCE0gjq3I#c056`  chunk_ids=['tHrCE0gjq3I:01770']
    The creator suggests that a context length of perhaps 100,000 to 1 million tokens may already be sufficient, with marginal gains beyond that.
- 2025-01-18  `X2GpzYfy_sE#c024`  chunk_ids=['X2GpzYfy_sE:00540', 'X2GpzYfy_sE:00570']
    The motivation for the Titans long-term memory module is to extend effective context beyond 2 million tokens toward 4 million tokens and more.
- 2025-06-25  `wzXBXGVbItE#c032`  chunk_ids=['wzXBXGVbItE:00720', 'wzXBXGVbItE:00750']
    The creator expresses surprise that despite LLMs having context lengths of more than 1 million to 2 million tokens, they still have trouble maintaining coherent data flow and features for stories longer than 1,000 words.
- 2025-09-24  `keu1DAnUwiA#c045`  chunk_ids=['keu1DAnUwiA:01020', 'keu1DAnUwiA:01050', 'keu1DAnUwiA:01080']
    The creator argues that context length well below 1 million tokens remains a challenge for today's AI, despite marketing claims of models with context windows of 2 million to 5 million tokens.
- 2025-12-03  `20rNv7yrTPM#c071`  chunk_ids=['20rNv7yrTPM:02310', '20rNv7yrTPM:02340', '20rNv7yrTPM:02370']
    The creator concludes that the common belief that longer context and higher context engineering provide higher intelligence for an LLM is incorrect, and that compressing information to the minimum representation in a small subspace is the way to achieve the highest intelligence.
- 2026-02-03  `anEVsOPtbnw#c008`  chunk_ids=['anEVsOPtbnw:00150']
    The Google study finds that the model actively untangles the sequence into a linear path representation, and that longer context increases the straightening of the hidden state.

### lc-0179  [topic:grokking]  span=386d  advisory=neutral
**Q:** How did the creator's understanding and explanation of the grokking phenomenon evolve from January 2025 through early 2026?
trajectory_must_say:
- In January 2025 the creator described grokking as an unexplained phenomenon, noting no one could yet explain why it happens or how to trigger it earlier
- By November 2025 he proposed his own unpublished, speculative theory that grokking is a phase transition of a geometric representation in a transformer's internal memory
- In January 2026 he discussed evidence that grokking-like dynamics occur not just during LLM training but also during inference-time reasoning steps in an HRM model
- By February 2026 he was speculating about deliberately triggering a grokking-like phase transition in smaller LLMs by helping them find an optimal geometric/structural representation
milestones (5):
- 2025-01-14  `SRfJQews1AU#c004`  chunk_ids=['SRfJQews1AU:00090']
    Until now, no one could explain why grokking happens in the first place or how to ignite it earlier.
- 2025-11-02  `PaSm5vHYDew#c002`  chunk_ids=['PaSm5vHYDew:00000', 'PaSm5vHYDew:00030', 'PaSm5vHYDew:00090', 'PaSm5vHYDew:00330', 'PaSm5vHYDew:00720', 'PaSm5vHYDew:00930']
    The creator proposes a new, personal, unpublished idea that this geometric memory concept could explain the phenomenon of grokking.
- 2025-11-02  `PaSm5vHYDew#c021`  chunk_ids=['PaSm5vHYDew:00330']
    The creator's crazy idea is that grokking is a phase transition of a geometrical representation in the internal memory of a transformer architecture.
- 2026-01-19  `UETxlAf0BOA#c037`  chunk_ids=['UETxlAf0BOA:00990', 'UETxlAf0BOA:01050']
    The authors report that grokking dynamics occur not only during LLM training but also within HRM's reasoning process.
- 2026-02-04  `iHLDu-IdJwo#c037`  chunk_ids=['iHLDu-IdJwo:00780', 'iHLDu-IdJwo:00810']
    The creator raises the question of whether smaller LLMs could be made more intelligent by helping them find their optimal structural representation, and whether a phase transition analogous to grokking could be triggered by finding the right mathematical/geometric representation.

### lc-0223  [topic:llm as judge]  span=132d  advisory=neutral
**Q:** How did the creator's assessment of the LLM-as-judge evaluation approach evolve from early/mid-2025 through early 2026?
trajectory_must_say:
- The creator initially expressed discomfort or was 'not happy' about papers relying on an LLM as judge
- He noted empirical evidence showing meaningful but imperfect agreement (around 70%) between LLM judges and human evaluators
- He came to recognize that a reliable LLM-as-judge requires specific training rather than simply using an off-the-shelf model, and benefits from deterministic ground truth
- By late 2025 and into 2026 he raised specific concerns that LLM judges may lack genuine domain expertise/validation data and can be undermined by hallucination
milestones (5):
- 2025-08-23  `nWARugXmQoI#c013`  chunk_ids=['nWARugXmQoI:00300']
    The LiveMCP-101 team used an LLM as a judge to score results, and the creator states he was initially not happy about this approach.
- 2025-09-01  `0he3LCqPl98#c035`  chunk_ids=['0he3LCqPl98:00810']
    The paper shows about 70% agreement between what the LLM evaluator (LLM-as-a-judge) recommends among 20 to 50 candidate user interfaces and what human evaluators consider a good interface.
- 2025-09-20  `N7dDq54_akY#c070`  chunk_ids=['N7dDq54_akY:02190']
    The creator notes that using an LLM as a judge requires specific training and cannot simply use an off-the-shelf model like GPT-5.
- 2025-12-30  `T4g5uSaY3Ko#c063`  chunk_ids=['T4g5uSaY3Ko:01950', 'T4g5uSaY3Ko:01980', 'T4g5uSaY3Ko:02010']
    The creator explains that each evaluation criterion (e.g., activity, toxicity) is judged by an LLM acting as a judge, such as GPT-5 predicting antibiotic activity or Claude Sonnet 4.5 predicting toxicity using a formula it found online, and that this LLM-as-judge approach may lack genuine medical expertise or sufficient validation data.
- 2026-01-02  `96XVs6qcIT4#c032`  chunk_ids=['96XVs6qcIT4:00540', '96XVs6qcIT4:00570']
    The creator expresses concern about relying on the judgment of a hallucinating LLM as the accuracy reward evaluator.

### lc-0251  [topic:memorization]  span=388d  advisory=neutral
**Q:** How did the creator's characterization of memorization in LLMs evolve from January 2025 through early 2026 as he examined it across grokking dynamics, fine-tuning, and reasoning benchmarks?
trajectory_must_say:
- Early on, memorization was framed as a temporary phase in training (e.g., the lazy regime in grokking) that precedes generalization, and as a fine-tuning side effect that hurts generalization to modified problems
- By September 2025, the creator concluded that memorization, not genuine reasoning, is the dominant behavior in LLMs, with strong benchmark performance often reflecting recalled facts rather than first-principles reasoning
- He described a method of exposing this by making memory useless (e.g., changing underlying rules), which reveals the model's much weaker true inductive reasoning capability
- By early 2026, he pointed to concrete cases—models reciting answers from pre-training even without context, and solving one-step tasks via direct copy-pasting of memorized sequences—as further evidence that models often bypass reasoning through memorization
milestones (6):
- 2025-01-14  `SRfJQews1AU#c005`  chunk_ids=['SRfJQews1AU:00090']
    New research explains that grokking happens late and suddenly because the LLM first gets stuck in a lazy training regime where memorization is the dominant learning force.
- 2025-03-15  `xqOAdmgUAC8#c015`  chunk_ids=['xqOAdmgUAC8:00720', 'xqOAdmgUAC8:00750']
    Gemini 2.0's report cites research suggesting that as supervised fine-tuning progresses, models may memorize prompt-solution pairs, causing difficulty generalizing to slightly modified problems.
- 2025-09-24  `keu1DAnUwiA#c040`  chunk_ids=['keu1DAnUwiA:00930', 'keu1DAnUwiA:00960']
    The authors conclude that memorization over genuine reasoning is currently the dominant behavior in LLMs, meaning they recall memorized facts rather than reason.
- 2025-09-24  `keu1DAnUwiA#c039`  chunk_ids=['keu1DAnUwiA:00930']
    The authors state that when the LLM's memory is made useless by changing the rules (e.g., synthetic genetic code), the true, much weaker inductive reasoning capabilities of the model are exposed.
- 2026-01-17  `az5WB-nGDk4#c041`  chunk_ids=['az5WB-nGDk4:01200', 'az5WB-nGDk4:01230']
    The creator explains that if GPT-5 has seen a specific paper during pre-training (e.g., about a year old), it can produce a correct answer purely from its learned weights even if given a blank sheet of paper as context, because it is reciting rather than reading.
- 2026-02-06  `b0c64uUyvpo#c017`  chunk_ids=['b0c64uUyvpo:00570']
    For one-step tasks, the model can solve them via simple copy-pasting from memorized training data without needing reasoning, since it directly saw the sequence (e.g., apple followed by car).

### lc-0266  [topic:model preference]  span=439d  advisory=neutral
**Q:** How did the creator's preferred or favorite AI model change over the course of 2025 into 2026?
trajectory_must_say:
- In January 2025 the creator favored the R1 32B model, valuing it for causal reasoning and the practicality of running it locally due to its 32 billion parameters
- By April 2025 the creator had shifted to using Google LLMs, naming Gemini Pro 2.5 as his best model
- By April 2026 the creator's preference had moved to Nano Banana Pro, which he felt no need to switch away from
milestones (3):
- 2025-01-29  `2ENvGkkK36E#c019`  chunk_ids=['2ENvGkkK36E:00330']
    The creator particularly likes the R1 32B model for causal reasoning because it has 32 billion trainable parameters, making it feasible to run locally.
- 2025-04-10  `Geo8LzCHoMQ#c005`  chunk_ids=['Geo8LzCHoMQ:00030', 'Geo8LzCHoMQ:00060']
    The creator states he currently uses Google LLMs and considers Gemini Pro 2.5 his best model.
- 2026-04-13  `i5QwfAeNhOU#c028`  chunk_ids=['i5QwfAeNhOU:00510', 'i5QwfAeNhOU:00660']
    The creator states they do not currently feel the need to switch away from Nano Banana Pro, expressing a preference for it.

### lc-0413  [topic:self correction]  span=409d  advisory=neutral
> NOTE: pick at most one of lc-0413 / lc-0497
**Q:** How did the creator's assessment of AI models' self-correction abilities during reasoning evolve from early 2025 through mid-2026?
trajectory_must_say:
- In early 2025 the creator was impressed by spontaneous self-correction observed across many models (e.g., Grok 3, Claude Sonnet 3.7, QwQ 32B, Gemini, Llama 4, o3, and even small models), treating it as a valuable emergent reasoning capability
- By mid-2025 the creator began noting failures and inconsistencies in self-correction, such as a model failing to fully revise a flawed solution or incorrectly second-guessing a correct one, and called for more resilient, verifiable self-correction protocols rather than purely heuristic behavior
- By early 2026 the creator increasingly framed self-correction as an unresolved research problem requiring dedicated technical solutions and explicitly questioned whether claimed self-correction mechanisms were genuinely occurring or just what researchers hoped for
- By April 2026 the creator expressed concern that self-correction was taking an excessively long time to occur, criticizing this delay as something that should not happen in AI systems
milestones (5):
- 2025-03-01  `KSJNr1SPd3U#c013`  chunk_ids=['KSJNr1SPd3U:00390', 'KSJNr1SPd3U:00420']
    After being prompted by the creator to check their results, both Grok 3 and Claude Sonnet 3.7 found their own mistake regarding Avalon and self-corrected their solutions.
- 2025-05-23  `fgSdunF7Oe0#c017`  chunk_ids=['fgSdunF7Oe0:00540', 'fgSdunF7Oe0:00570']
    After failing to validate the three alleged solutions, Claude Opus 4 said it may have been wrong about there being multiple valid solutions and asked the creator to clarify if multiple solutions were found.
- 2025-06-16  `os5Qxk9tfr0#c030`  chunk_ids=['os5Qxk9tfr0:00630', 'os5Qxk9tfr0:00660']
    The creator proposes that the lead researcher needs more resilience, self-correction, and dynamic adaptability, upgrading from purely heuristic approaches to protocols with verifiable data and a self-corrective imperative.
- 2026-02-16  `COwGuc_S4SU#c031`  chunk_ids=['COwGuc_S4SU:00540']
    By coupling the generation of criteria with the execution of reasoning in a shared reward reinforcement loop, the AI model self-corrects its reasoning process, though the creator questions whether this is truly happening or merely what the authors hope for.
- 2026-04-14  `kLs4NT2hbXU#c067`  chunk_ids=['kLs4NT2hbXU:02040']
    The creator states that MiniMax M2.7 ultimately concluded its second response was wrong and its sixth response was correct, and remarks that this should never happen in AI and that it took an extremely long time for the AI to re-evaluate its own reasoning trace.

### lc-0497  [topic:verification]  span=391d  advisory=waypoint
> NOTE: pick at most one of lc-0413 / lc-0497
**Q:** How did the creator's understanding of the reliability and role of AI models' self-verification during reasoning tasks evolve from early 2025 through mid-2026?
trajectory_must_say:
- In early 2025, models performing self-verification appeared to succeed, walking through clues or steps and confirming their own solutions as correct.
- Through mid-2025, repeated testing showed this self-verification was often unreliable: models discovered new critical errors in solutions they had previously validated, or produced conflicting 'verified' results across different runs.
- This unreliability led to arguments that verification needed to be structural, using dedicated verifier agents and automated domain-specific/symbolic checks rather than trusting any single model's self-assessment.
- By late 2025 into 2026, verification was reframed as an active technique to improve reasoning performance and was built into training pipelines as a formal automated check on generated outputs.
milestones (6):
- 2025-02-01  `mWWfMoMkqHQ#c010`  chunk_ids=['mWWfMoMkqHQ:00300']
    The model's solution included a verification step where it checked its answer against all clues, at one point going through numbered checks up to at least 15 or 17.
- 2025-03-20  `rNjNANKvAoE#c059`  chunk_ids=['rNjNANKvAoE:01350', 'rNjNANKvAoE:01380']
    Recommended structural approaches emphasize comprehensive verification and validation at all levels, not trusting any AI agent, LLM, VLM, or VLA, using automated verification methodology including domain-specific testing and symbolic reasoning to reduce error rates, similar to human quality assurance practices.
- 2025-04-29  `u-WXyeV1tsw#c037`  chunk_ids=['u-WXyeV1tsw:01290', 'u-WXyeV1tsw:01320', 'u-WXyeV1tsw:01350']
    In this new verification pass, the model found a new critical error and concluded that the previous solution was invalid because it violated clue 14, specifically assigning Avalon to the tome of secrets incorrectly.
- 2025-07-22  `FtrLaHeEP4E#c033`  chunk_ids=['FtrLaHeEP4E:00870', 'FtrLaHeEP4E:00900']
    When asked to verify its solution rigorously, Qwen3 235B produced conflicting verification results: a 'complete correct and verified optimal run' of 17 presses, then a 16-press sequence, then a 'truly verified optimal run' of 18 presses.
- 2025-12-03  `20rNv7yrTPM#c007`  chunk_ids=['20rNv7yrTPM:00210']
    Asking an LLM to consider this verification approach before starting agent A's reasoning process makes it much better at reasoning.
- 2026-02-27  `K4yLplNrY24#c054`  chunk_ids=['K4yLplNrY24:01860', 'K4yLplNrY24:01890']
    In the training pipeline, an LLM generates a Python script from a verbal instruction based on the reasoning graph, which is verified and executed to check whether the final output meets the graph conditions.

### lc-0448  [topic:task decomposition]  span=353d  advisory=neutral
**Q:** How did the creator's assessment of task decomposition as a technique in AI systems evolve from early 2025 through early 2026?
trajectory_must_say:
- In early-to-mid 2025 the creator presented task decomposition favorably as a core, useful technique—e.g., MinionS decomposing queries into simpler jobs, QwQ's task segmentation being labeled one of four essential logic patterns for self-learning systems, and decomposition being treated as broadly applicable akin to physics/math problem-solving
- Through mid-to-late 2025 he continued describing decomposition as a structuring mechanism in more complex systems, such as manager agents splitting tasks for dispatch and frameworks organizing complex projects into phased DAGs rather than monolithic plans
- By February 2026 his tone shifted to a critique: he characterized current task decomposition/delegation methodologies as relying on simple, hardcoded, fixed heuristics that are boring and lack flexibility or machine intelligence, unable to adapt to environmental changes or failure modes
- This critique motivated proposals for more dynamic delegation frameworks where agents decompose tasks into verifiable subcomponents mapped to marketplace capabilities, rather than relying on the rigid heuristics of earlier approaches
milestones (5):
- 2025-02-27  `L-WfRaSPE2A#c023`  chunk_ids=['L-WfRaSPE2A:00660', 'L-WfRaSPE2A:00690']
    MinionS extends the Minions protocol by having the remote LLM decompose a query into many simpler jobs, reducing task complexity levels (e.g., from complexity 7 to 5, or 5 to 6) which are then processed in parallel by the local model.
- 2025-03-09  `DBBD7bPn0DY#c021`  chunk_ids=['DBBD7bPn0DY:00750', 'DBBD7bPn0DY:00780']
    The creator highlights that QwQ 32B demonstrated task segmentation, breaking a high-complexity problem into lower-complexity subtasks, which he considers one of four essential logic patterns for a self-learning AI system.
- 2025-09-29  `2unOi2JTZ0I#c026`  chunk_ids=['2unOi2JTZ0I:00570', '2unOi2JTZ0I:00630']
    The second major component of the framework is building a directed acyclic graph (DAG) structure so that complex projects are executed as phases rather than as a single monolithic plan from an orchestrating agent.
- 2026-02-15  `FDixNQunPTc#c006`  chunk_ids=['FDixNQunPTc:00030', 'FDixNQunPTc:00060']
    The paper argues that today's task decomposition and delegation methodologies in AI rely on simple heuristics that cannot dynamically adapt to environmental changes or robustly handle unexpected failure modes.
- 2026-02-15  `FDixNQunPTc#c008`  chunk_ids=['FDixNQunPTc:00090']
    The creator characterizes current task decomposition processes in agentic AI as hardcoded, highly constrained, fixed, boring, and lacking flexibility or machine intelligence.

### lc-0481  [topic:transformer limitations]  span=287d  advisory=neutral
**Q:** How did the creator's diagnosis of what fundamentally limits transformer architectures evolve from mid-2025 through early 2026?
trajectory_must_say:
- The creator initially concluded transformers cannot reason reliably past a certain complexity threshold, where reasoning disintegrates
- He then attributed this to concrete structural issues: shallow/fixed layer depth that width or depth increases don't fix, brittle externalized chain-of-thought, and severe data inefficiency
- He later added that classical transformers lack a plasticity mechanism for adapting pathways to task complexity, unlike newer proposed theories
- By early-to-mid 2026 he reframed the core problem as not being an inherent flaw of the transformer architecture itself, but a mismatch from forcing an inductive, autoregressive engine to perform deductive logical work
milestones (6):
- 2025-06-07  `fGcfJ9J_Faw#c043`  chunk_ids=['fGcfJ9J_Faw:00900']
    The creator concludes that transformers are not able to reason reliably beyond a particular complexity threshold, at which point reasoning disintegrates.
- 2025-07-02  `QWD55guu0So#c002`  chunk_ids=['QWD55guu0So:00030']
    Transformer networks have a fixed and relatively shallow number of processing layers, which is not well suited for complex multi-step algorithmic reasoning.
- 2025-07-02  `QWD55guu0So#c005`  chunk_ids=['QWD55guu0So:00060']
    Chain of thought works by externalizing the reasoning process, but it is rather brittle and struggles with problems requiring more complex reasoning.
- 2025-11-16  `IADccLs--lM#c039`  chunk_ids=['IADccLs--lM:01410']
    The creator notes that a classical transformer has predefined paths and no plasticity mechanism, unlike this new theory which incorporates plasticity responsive to the learning function.
- 2026-01-19  `UETxlAf0BOA#c006`  chunk_ids=['UETxlAf0BOA:00120']
    Standard transformer architectures like GPT-5 generate one autoregressive token after another and fail in the reasoning process, motivating alternatives like HRM.
- 2026-03-21  `beCj-7xjVmI#c012`  chunk_ids=['beCj-7xjVmI:00240', 'beCj-7xjVmI:00270']
    The paper empirically establishes, through extensive experiments, that the LLM's inability to do precise logic is not a limitation of the transformer architecture itself, since it was not designed for that purpose, but is an artifact of forcing inductive engines to do deductive work autoregressively.

### lc-0496  [topic:verifiable rewards]  span=311d  advisory=neutral
**Q:** How did the creator's assessment of reinforcement learning with verifiable rewards evolve from spring 2025 through early 2026 as he encountered new papers and considerations on the topic?
trajectory_must_say:
- Early on (April 2025), the creator cited a paper finding that RL with verifiable binary rewards does not elicit reasoning beyond the base model, mainly improving sampling efficiency while potentially narrowing the reasoning solution space.
- He identified a practical bottleneck: verifiable reward optimization depends on human-labeled, domain-specific question-answer datasets, since synthetic data underperforms and quality human data is slow to produce.
- He later raised a 'dark side' concern: if a model can cheat within its given context, verifiable reward training can teach it to exploit the cheat while mimicking non-cheating chain-of-thought to avoid detection.
- By early 2026, he settled on a domain-limited view: verifiable rewards work well mainly in math/code where compilers or calculators give objective true/false signals, but the approach breaks down in fuzzy, open-ended domains like medicine or law.
milestones (5):
- 2025-04-22  `78vn6XWvtzI#c044`  chunk_ids=['78vn6XWvtzI:01440', '78vn6XWvtzI:01470', '78vn6XWvtzI:01680']
    A paper published 2 days before this video (from a Chinese university, referenced as Tsinghua University) found that reinforcement learning with verifiable binary rewards does not elicit reasoning abilities beyond the base model, only improves sampling efficiency, and can narrow the reasoning boundaries and reduce the available solution space.
- 2025-06-15  `7ec_0NPxmnA#c012`  chunk_ids=['7ec_0NPxmnA:00510', '7ec_0NPxmnA:00540']
    The creator states that the main problem with verifiable reward optimization currently is the need for a human-created, labeled, domain-specific question-answer dataset, and that synthetic data is not as good, and creating quality human data at scale takes a long time.
- 2026-01-15  `0ezdBcdY3bc#c025`  chunk_ids=['0ezdBcdY3bc:00540', '0ezdBcdY3bc:00570']
    The creator argues there is a 'dark side' to reinforcement learning with verifiable rewards: if a model is punished for being wrong but given context that allows it to cheat, the gradient update teaches the model to use the cheat to get the reward while mimicking the chain of thought of a non-cheater to avoid appearing suspicious to humans.
- 2026-01-27  `KV-uZzE78qA#c010`  chunk_ids=['KV-uZzE78qA:00210', 'KV-uZzE78qA:00240']
    The creator notes that verifiable reward approaches have mostly worked in math and code domains because compilers and calculators can provide objective true/false reward functions, unlike fuzzy domains such as medicine or law.
- 2026-02-27  `K4yLplNrY24#c007`  chunk_ids=['K4yLplNrY24:00180']
    The creator states that with mathematical or code-based tasks, reinforcement learning by verifiable rewards works well because results can be immediately verified, but this breaks down for open-ended human tasks lacking a mathematical or code interpretation.

### lc-0232  [topic:local minimum]  span=380d  advisory=waypoint
**Q:** How did the creator's treatment of the 'local minimum' concept in AI systems evolve from March 2025 through March 2026, as he moved from citing academic research to identifying his own examples and demonstrations?
trajectory_must_say:
- Initially referenced an MIT/Harvard study suggesting next-token-prediction training traps LLMs in a local minimum of reasoning ability that post-training RL cannot escape to reach the true global-minimum solution
- Later identified a practical local minimum problem in agent behavior, where an LLM gets stuck using only one database out of thousands available without the user's knowledge
- Eventually demonstrated the phenomenon empirically with Claude, showing an exploration trajectory that zigzagged within a cone and settled into a local minimum of 13%, worse than the 23% seed prompt performance
milestones (3):
- 2025-03-07  `seTdudcs-ws#c022`  chunk_ids=['seTdudcs-ws:00510', 'seTdudcs-ws:00540']
    MIT and Harvard suggest that next-token-prediction training on internet-scale data ('string copy internet') may constrain the language model to a local minimum of reasoning abilities that post-training reinforcement learning is not strong enough to escape from, preventing it from reaching the global minimum representing the true solution.
- 2025-08-15  `dSxEo0zUwH4#c014`  chunk_ids=['dSxEo0zUwH4:00480']
    The creator identifies a 'local minimum' problem where an LLM decides to use only one database out of thousands available, getting stuck without the user knowing what the agent is actually doing.
- 2026-03-22  `cxqRKt1GYNQ#c028`  chunk_ids=['cxqRKt1GYNQ:00810']
    In the creator's visual demonstration using Claude, the exploration trajectory zigzags within a cone starting from a seed prompt performance of 23%, finding a local minimum of just 13%, worse than the seed prompt.

### lc-0260  [topic:model capability]  span=216d  advisory=waypoint
**Q:** How did the creator's assessment of small (3B-parameter-class) models' ability to handle his difficult reasoning puzzles evolve from September 2025 through April 2026?
trajectory_must_say:
- In September 2025, testing Qwen3 Next A3B (3B active parameters) on his causal reasoning puzzle, the creator concluded the model's 'brain' was not big enough to solve it, even though it got remarkably close on a later attempt
- He judged that such small models could be excellent for simpler or medium-complexity tasks but were not capable of his hardest causal reasoning challenges
- By March 2026 he characterized small models as lacking the meta-cognitive capacity to write good checklists for themselves, though they could follow instructions/checklists provided by larger models to solve complex problems
- By April 2026 the creator reported a 3B model immediately finding the correct solution strategy on his puzzle, calling it absolutely amazing and something he had never before seen a 3B model achieve
milestones (5):
- 2025-09-16  `J9br0e34cp0#c022`  chunk_ids=['J9br0e34cp0:00390', 'J9br0e34cp0:00420']
    The creator observes that for the complexity of his causal reasoning test, the model's capacity is not big enough, and it tries to break the problem into smaller pieces, solve each, and recombine them, but fails.
- 2025-09-16  `J9br0e34cp0#c032`  chunk_ids=['J9br0e34cp0:00600']
    The creator concludes that the 3 billion active parameter A3B configuration was not a big enough 'brain' to solve his complexity level of causal reasoning test.
- 2025-09-16  `J9br0e34cp0#c033`  chunk_ids=['J9br0e34cp0:00600']
    The creator believes Qwen3 Next A3B could be an excellent open-source model for simpler problems, but it failed on real difficult causal reasoning in his test.
- 2026-03-29  `g3lh7U_rV9w#c053`  chunk_ids=['g3lh7U_rV9w:01350']
    The creator argues that this preprint proves small models inherently lack the meta-cognitive capacity to write good checklists for themselves, but have enough instruction-following intelligence to correctly follow a checklist provided by a larger model and solve complex problems.
- 2026-04-20  `Gnk-me1UqfE#c034`  chunk_ids=['Gnk-me1UqfE:00810', 'Gnk-me1UqfE:00840']
    The creator states the model immediately found the correct segmentation strategy to solve the puzzle and characterizes this as absolutely amazing, having never seen this achieved by any 3B model, dense or mixture-of-experts, before.

# SPOT-CHECK (10) - random drops to verify the read isn't burying arcs (seed 20260716)

### lc-0071  [topic:coherence]  span=95d  advisory=neutral
**Q:** How did the creator's assessment of coherence problems in LLM outputs and agent behavior evolve from June 2025 through September 2025?
trajectory_must_say:
- Initially argued from a theoretical standpoint that even a minimal coherent world model is necessary to avoid disconnected reasoning 'islands' and to enable generalization
- Was then surprised to find that LLMs still struggle to maintain coherent story data/features beyond about 1,000 words despite context windows of 1-2 million tokens
- Noted that multi-agent GRPO training could help prevent stylistically jarring or repetitive writing between separate agents by encouraging coherent style
- Later cited a paper showing significant internal inconsistencies between agents' conversational behavior and their revealed internal state across all model families and sizes tested
milestones (4):
- 2025-06-04  `I99O0R1fTEk#c044`  chunk_ids=['I99O0R1fTEk:01860', 'I99O0R1fTEk:01890', 'I99O0R1fTEk:01920', 'I99O0R1fTEk:01950', 'I99O0R1fTEk:01980']
    The creator argues from a physical/logical standpoint that disconnected 'islands' of reasoning without a coherent world model would prevent generalization to unseen objectives, whereas having even a tiny, imperfect implicit world model enables emergence of a new level of intelligence because the AI understands logical interconnections between elements.
- 2025-06-25  `wzXBXGVbItE#c032`  chunk_ids=['wzXBXGVbItE:00720', 'wzXBXGVbItE:00750']
    The creator expresses surprise that despite LLMs having context lengths of more than 1 million to 2 million tokens, they still have trouble maintaining coherent data flow and features for stories longer than 1,000 words.
- 2025-08-07  `_Uw-8NOPyNQ#c022`  chunk_ids=['_Uw-8NOPyNQ:00750']
    Without multi-agent GRPO, two writing agents might produce stylistically jarring or repetitive content because they would write separate chapters without coherent style.
- 2025-09-07  `OAyxKJ5VQpQ#c026`  chunk_ids=['OAyxKJ5VQpQ:00810', 'OAyxKJ5VQpQ:00840']
    This second paper assesses whether an agent's conversational behavior is consistent with what would be expected from its revealed internal state, finding significant internal inconsistencies across all model families and model sizes tested.

### lc-0077  [topic:compositional reasoning]  span=389d  advisory=neutral
**Q:** How did the creator's characterization of LLMs' capacity for compositional reasoning evolve from early 2025 through early 2026?
trajectory_must_say:
- In early 2025, the creator framed compositional reasoning as a weakness of LLMs that could be addressed by offloading systematic knowledge synthesis to a knowledge graph.
- By early 2026, the creator cited the Princeton study's finding that compositional reasoning is a critical bottleneck for LLMs, which rely on pattern matching rather than genuinely combining facts into novel logical chains.
- Shortly after, the creator reported a claim (from Gemini) that AI had progressed from 'stochastic guessing' to genuine 'compositional reasoning,' introducing a more optimistic assessment that contrasted with the bottleneck framing.
milestones (4):
- 2025-02-21  `Sln1n3Jba_U#c072`  chunk_ids=['Sln1n3Jba_U:02040', 'Sln1n3Jba_U:02070']
    The creator argues that compositional reasoning for systematic knowledge synthesis via the graph can address limitations of an LLM's own limited systematic reasoning, because the knowledge graph may represent higher complexities more easily than a neural transformer architecture.
- 2026-01-27  `KV-uZzE78qA#c004`  chunk_ids=['KV-uZzE78qA:00090']
    The Princeton study shows that LLMs have a critical bottleneck: an inability to perform genuine compositional reasoning.
- 2026-01-27  `KV-uZzE78qA#c006`  chunk_ids=['KV-uZzE78qA:00120']
    Princeton's study shows that AI models often achieve high accuracy via pattern matching only and struggle to combine axiomatic facts into novel multi-step logical chains not seen during training.
- 2026-03-17  `9kox34X9IQs#c033`  chunk_ids=['9kox34X9IQs:00810', '9kox34X9IQs:00840']
    Gemini told the creator that AI has not regressed to fragmentation but has evolved from 'stochastic guessing' to 'compositional reasoning.'

### lc-0090  [topic:cost efficiency]  span=391d  advisory=neutral
**Q:** How did the creator's assessment of how AI systems can achieve meaningful cost efficiency evolve from January 2025 through early 2026?
trajectory_must_say:
- Early framing relied on simple headline-level claims, such as training a model cheaply and reaching performance close to a strong proprietary model.
- This gave way to more rigorous, quantified benchmarking of performance-versus-cost trade-offs, such as studies showing near-full performance recovery at a fraction of cloud costs.
- Over time the creator highlighted an increasingly diverse set of concrete mechanisms for cutting costs, including prompt engineering, reward-model-based judging, distillation, and latent/compressed representations.
- By 2026 the creator pointed to specific architectural strategies, like distilling multi-agent reasoning into a single cheaper agent or skipping costly initial reasoning steps, as ways to preserve performance while sharply reducing computational expense.
milestones (6):
- 2025-01-12  `ZmliPzGENMM#c028`  chunk_ids=['ZmliPzGENMM:00510', 'ZmliPzGENMM:01050']
    The creator characterizes Sky-T1 as demonstrating that one can train an LLM with performance close to OpenAI's o1-preview model for about $500.
- 2025-02-27  `L-WfRaSPE2A#c043`  chunk_ids=['L-WfRaSPE2A:01260']
    The official study results state that on average across multiple datasets, MinionS can recover close to 98% of the performance of the remote-only language model while spending about six times less.
- 2025-03-27  `4QnDrX6c96E#c059`  chunk_ids=['4QnDrX6c96E:01380', '4QnDrX6c96E:01410']
    The creator explains that adding chain-of-thought examples to the prompt is cheaper because users pay per token/step, and this technique regulates token distribution in a way that overrides excessive thinking.
- 2025-07-27  `5LUIZAZWoBU#c039`  chunk_ids=['5LUIZAZWoBU:00990', '5LUIZAZWoBU:01020']
    GeARs' just-in-time alignment approach offers minimal operational computational cost, using a small efficient LLM (around 3-4 billion parameters) to process only a handful of documents per query, shifting cost from massive upfront investment to a small fraction of a cent per query.
- 2025-12-01  `NreIscoJe8o#c035`  chunk_ids=['NreIscoJe8o:01110', 'NreIscoJe8o:01140']
    The latent multi-agent system reduces system-wide token usage by up to 83-84% compared to the text-based multi-agent system.
- 2026-02-07  `kFu4WvsahPk#c031`  chunk_ids=['kFu4WvsahPk:00660']
    Key finding: the methodology enables a single agent to acquire multi-agent reasoning ability and operate on a much cheaper financial basis.

### lc-0158  [topic:gating mechanism]  span=448d  advisory=waypoint
**Q:** How did the creator's characterization of gating mechanisms in neural network architectures evolve from January 2025 through April 2026, as he encountered them in memory systems, activation functions, mixture-of-experts routers, and gated MLPs?
trajectory_must_say:
- Initially (Titans, Jan 2025) gating was described simply as a way to weight or balance contributions among different signal or memory sources for a given task.
- In activation-function gating, the mechanism was framed as a 'shutter' or filter that blocks negative/noisy signals and passes only strongly positive ones to clean up the output.
- Later coverage of a mixture-of-experts paper (Feb 2026) revealed that gating mechanisms can develop inherent bias, causing the router to act like a low-pass filter that partitions tokens by syntactic structure rather than the intended semantic specialization.
- By April 2026, gating in gated MLPs was again described in functional terms, as a branch that controls how much of the main signal passes through via element-wise multiplication to select context-relevant features.
milestones (5):
- 2025-01-18  `X2GpzYfy_sE#c045`  chunk_ids=['X2GpzYfy_sE:01200', 'X2GpzYfy_sE:01230']
    Titans uses a gating mechanism, similar to LSTM gates, to decide how much weight to give each of the three memory types (short-term/attention, long-term, persistent) for a given task, e.g., an example split of 80% attention, 10% long-term, 10% persistent, or alternatively 40% persistent, 10% long-term, and the rest to attention.
- 2025-12-05  `1oVelAKD_5A#c040`  chunk_ids=['1oVelAKD_5A:01380', '1oVelAKD_5A:01410']
    The creator argues that without these activation 'shutters,' the LLM would be confused by millions of negative signals; the shutter cleans up noise and filters an active subspace so only strongly positive-scoring signals contribute.
- 2026-02-19  `rO2d6RHjtt8#c035`  chunk_ids=['rO2d6RHjtt8:00360', 'rO2d6RHjtt8:00390']
    Standard mixture of expert theory assumes the router (W_gate) will learn to partition the input space, but the paper reveals this introduces bias in the gating mechanism itself.
- 2026-02-19  `rO2d6RHjtt8#c039`  chunk_ids=['rO2d6RHjtt8:00420']
    This alignment means the mixture of expert router effectively becomes a low-pass filter, routing tokens based on syntactic structure rather than specialized semantic content.
- 2026-04-11  `SrHSjQkBIrY#c016`  chunk_ids=['SrHSjQkBIrY:00420']
    The gated MLP splits computation into two paths: one deciding what matters (the gate) and one carrying the main information, combined via element-wise multiplication.

### lc-0167  [topic:gpt 5 limitations]  span=169d  advisory=neutral
**Q:** How did the creator's characterization and understanding of GPT-5's core limitations evolve from August 2025 through January 2026?
trajectory_must_say:
- The creator initially described GPT-5's failures empirically, noting it could produce isolated subsystem solutions but could not reassemble or rearrange them into a coherent, functional whole
- He connected this to a broader claim that GPT-5 cannot handle combined understanding-and-acting complexity, and specifically fails at progressively rebuilding context at higher complexity and at combining global strategic planning with detailed local execution
- By October 2025 he claimed to have found a mathematical explanation for these previously empirically observed failures, including GPT-5's inability to do PhD-level science
- The pattern was further evidenced in new domains, such as GPT-5 producing invalid, ontology-violating triplets in biomedical knowledge graph generation, and was later externally corroborated by a published paper on GPT-5's limitations
milestones (5):
- 2025-08-11  `GohEyWrex4s#c034`  chunk_ids=['GohEyWrex4s:00660']
    The creator argues that GPT-5 failed to rearrange decomposed subsystems back into an operative machine because it never understood how the parts interact with each other or how to rebuild a functional system.
- 2025-08-15  `dSxEo0zUwH4#c016`  chunk_ids=['dSxEo0zUwH4:00540']
    The creator states that this failure to progressively rebuild context at higher complexity is exactly the step where GPT-5 fails, referencing his prior video on this topic.
- 2025-10-02  `937cohqRsq0#c041`  chunk_ids=['937cohqRsq0:00840', '937cohqRsq0:00870']
    The creator claims this finding provides the mathematical explanation for why GPT-5 fails at complex tasks, which he had previously shown empirically a month earlier.
- 2025-10-15  `CAAE8c-_JK4#c022`  chunk_ids=['CAAE8c-_JK4:00390']
    The creator claims GPT-5 systems frequently produce invalid triplets for knowledge graph generation that in most cases violate biomedical ontologies, rendering the AI results untrustworthy and unscalable.
- 2026-01-27  `KV-uZzE78qA#c003`  chunk_ids=['KV-uZzE78qA:00030', 'KV-uZzE78qA:00060']
    A paper titled 'Even GPT-5 can't count to five' was published on January 22nd 2026 by a researcher from the National Institute of Informatics in Japan.

### lc-0169  [topic:gradient descent]  span=403d  advisory=neutral
**Q:** How did the creator's characterization of gradient descent's role within a model's forward pass—particularly regarding in-context learning and test-time training—evolve from early 2025 through early 2026?
trajectory_must_say:
- Initially (March 2025) the creator reported on academic papers proving that Transformers/attention layers could implicitly implement gradient descent steps for tasks like in-context linear regression or causal structure learning
- By late 2025 (December) the creator moved beyond citing papers to his own conclusion that in-context learning is effectively a transient, rank-one, online stochastic gradient descent process performed during the forward pass
- By early-to-mid 2026 the creator described concrete test-time training methods where real gradient descent updates physically modify a model's weight matrices during the forward pass, creating 'fast weights'
- The characterization progressed from reporting theoretical/mathematical claims about implicit gradient descent to the creator's own definitive synthesis, and finally to describing literal, physical weight updates via gradient descent at inference time
milestones (6):
- 2025-03-04  `Oft7rrpnvPU#c008`  chunk_ids=['Oft7rrpnvPU:00150', 'Oft7rrpnvPU:00180']
    The August 2024 Princeton paper introduced an in-context learning task requiring learning latent causal structures and proved that gradient descent on a simplified two-layer Transformer learns to solve this task by encoding the latent causal graph in the first attention layer.
- 2025-03-04  `Oft7rrpnvPU#c020`  chunk_ids=['Oft7rrpnvPU:00570', 'Oft7rrpnvPU:00600']
    The creator explains that chain-of-thought training teaches the Transformer to unroll gradient descent within the forward pass by requiring it to predict a sequence of weight vectors resembling gradient descent steps, forcing internalization of the iterative gradient descent nature.
- 2025-12-29  `mOjWG7hxPUI#c051`  chunk_ids=['mOjWG7hxPUI:01680', 'mOjWG7hxPUI:01710', 'mOjWG7hxPUI:01800']
    This split-second rewiring via rank-one update is mathematically identical to performing one step of online stochastic gradient descent on the prompt examples.
- 2025-12-29  `mOjWG7hxPUI#c055`  chunk_ids=['mOjWG7hxPUI:01800']
    The creator concludes that in-context learning is effectively a transient, rank-one, online stochastic gradient descent process performed during the forward pass.
- 2026-03-08  `-hFJe5hXWps#c032`  chunk_ids=['-hFJe5hXWps:00511', '-hFJe5hXWps:00541']
    This step performs a real gradient descent update on the tiny MLP model, physically updating its matrices W1 and W3 during the forward pass, creating 'fast weights' that may be computable even on older Nvidia hardware on edge devices.
- 2026-04-11  `SrHSjQkBIrY#c022`  chunk_ids=['SrHSjQkBIrY:00750', 'SrHSjQkBIrY:00780']
    The update rule for W down in the in-place TTT method is W_down at time i+1 equals W_down at time i minus a correction term derived from gradient descent on a loss function computed from intermediate activations and targets.

### lc-0177  [topic:graphrag limitations]  span=329d  advisory=neutral
**Q:** How did the creator's characterization of GraphRAG's core limitations evolve from February 2025 through early 2026 as he examined it across different papers and evaluations?
trajectory_must_say:
- Initially critiqued GraphRAG for retrieving overly broad, noisy subgraphs that increase computational cost and hurt LLM performance, partly due to a flat structure that produces incoherent prompts
- Also argued GraphRAG's usefulness is limited to narrow personal or corporate datasets and that it cannot detect the missing links needed to validate complex real-world claims like political or financial systems
- By mid-2025 argued that GraphRAG's near-perfect accuracy in a paper was a consequence of the task being restricted to single-hop, direct-edge queries rather than genuine multihop reasoning, citing an unanswerable multihop example
- By early 2026 reframed the limitation as an exploration-exploitation tradeoff where the system either zooms in or zooms out too aggressively
milestones (4):
- 2025-02-26  `oetP9uksUwM#c003`  chunk_ids=['oetP9uksUwM:00060']
    Graph-based RAG systems like GraphRAG and LightRAG can be improved upon because they retrieve excessively broad subgraphs, produce noisy prompts, increase computational cost, and lead to suboptimal LLM performance.
- 2025-02-28  `fpFA0AOfBYI#c016`  chunk_ids=['fpFA0AOfBYI:00540']
    The creator argues that GraphRAG and any RAG system cannot detect missing links needed to assess background information like political and financial systems, and that finding this connectivity is necessary to validate complex claims.
- 2025-07-26  `T3dxC9_mp1M#c045`  chunk_ids=['T3dxC9_mp1M:01290']
    The creator states that the GraphRAG approach shown in this paper is limited to single-hop, direct-edge association tasks, such as looking up a drug's side effect, and is not designed for higher complexity.
- 2026-01-21  `hDYtGpTsVV0#c005`  chunk_ids=['hDYtGpTsVV0:00060']
    GraphRAG suffers from an exploration-exploitation tradeoff where the system either zooms in too fast or zooms out too fast.

### lc-0242  [topic:masking]  span=287d  advisory=neutral
**Q:** How did the creator's characterization of masking techniques in AI model architectures evolve from mid-2025 through early 2026 as he covered different systems?
trajectory_must_say:
- Early coverage described a simple binary masking scheme distinguishing reasoning and action token spans
- Later coverage described a more complex joint masking matrix combining causal (lower-triangular) and fully bidirectional masking within a single model
- By 2026 the creator explicitly characterized such masking techniques as not novel, comparing them to older BERT and sentence-transformer approaches
milestones (3):
- 2025-05-22  `-OzH4buQzTM#c015`  chunk_ids=['-OzH4buQzTM:00330']
    SAD linearizes the trajectory into a flattened form with segment markers for 'reason' and 'action', using a reasoning mask (1 if the token belongs to the reasoning span, else 0) and an action mask (1 if the token belongs to the action span, else 0).
- 2025-12-21  `Ixrpkub47vg#c056`  chunk_ids=['Ixrpkub47vg:01530', 'Ixrpkub47vg:01560', 'Ixrpkub47vg:01590']
    The joint masking matrix in T5Gemma 2 enforces two laws simultaneously: a causal lower-triangular mask for the first M (decoder) columns, and a fully visible bidirectional mask for the subsequent N (encoder) columns.
- 2026-03-05  `n36ohNNWm_s#c034`  chunk_ids=['n36ohNNWm_s:00780']
    The creator notes that masking techniques used are similar to those from BERT and sentence transformers, calling the approach nothing new.

### lc-0365  [topic:reasoning quality assessment]  span=176d  advisory=neutral
**Q:** How did the creator's assessment of the quality and strategic coherence of AI models' reasoning traces evolve from September 2025 through early 2026 as he evaluated different models?
trajectory_must_say:
- Qwen3-Max's problem-solving was characterized as trial and error without a coherent strategy, though still deemed 'intelligent' (Sep 2025)
- DeepSeek V3.2 thinking was initially praised as an 'absolute professional reasoner' with perfectly sequential, non-looping exploration, but was then judged not well suited to the task's complexity, favoring overly granular solutions over a strategic one (Dec 2025)
- Qwen 3.5 27B's reasoning was assessed as lacking any long-term strategy, showing trial-and-error with small logical pieces, missing intelligence and nuance attributed to its smaller parameter size (Mar 2026)
- Qwen 3.5 Flash showed only slightly more semantic explanation than the 27B model, indicating limited improvement
milestones (6):
- 2025-09-08  `Y8hI6FyCinw#c012`  chunk_ids=['Y8hI6FyCinw:00180']
    The creator characterizes Qwen3-Max's problem-solving approach as pure trial and error without a coherent strategy, but assesses it as an 'intelligent' trial and error.
- 2025-12-02  `_TBsZeU4K7Q#c019`  chunk_ids=['_TBsZeU4K7Q:00240', '_TBsZeU4K7Q:00300']
    The creator assesses that DeepSeek V3.2 thinking is an absolute professional reasoner that explores every path in detail without looping, executing a perfectly sequential exploration of permutations.
- 2025-12-02  `_TBsZeU4K7Q#c026`  chunk_ids=['_TBsZeU4K7Q:00390', '_TBsZeU4K7Q:00420']
    On LM Arena, DeepSeek V3.2 thinking initially appeared to perform better, correctly identifying flags and a 'mirror mode' in the puzzle, but the creator judges the model is not well suited to this level of task complexity, seeking overly granular solutions rather than a strategic one.
- 2026-03-03  `X-yL5b5WNyY#c019`  chunk_ids=['X-yL5b5WNyY:00300', 'X-yL5b5WNyY:00330', 'X-yL5b5WNyY:00390', 'X-yL5b5WNyY:00420']
    The creator observes that Qwen 3.5 27B's reasoning trace shows no dedicated long-term strategy or optimization policy, but rather trial-and-error with small logical pieces of reasoning.
- 2026-03-03  `X-yL5b5WNyY#c026`  chunk_ids=['X-yL5b5WNyY:00540']
    The creator assesses that Qwen 3.5 27B's reasoning process showed missing intelligence, missing strategy, and neglected nuances, attributing this to its 27 billion parameter size.
- 2026-03-03  `X-yL5b5WNyY#c037`  chunk_ids=['X-yL5b5WNyY:00780']
    The creator observes that Qwen 3.5 Flash's reasoning trace includes a bit more semantic explanation compared to the 27B model.

### lc-0476  [topic:training stability]  span=334d  advisory=neutral
**Q:** How did the creator's discussion of what causes instability in reinforcement-learning-based AI training, and what can fix it, evolve from January 2025 through December 2025 as he covered different systems and papers?
trajectory_must_say:
- Throughout 2025 the creator identified multiple distinct sources of training instability, including MoE load imbalance, the need for KL divergence penalties, and the insufficiency of masking alone against sparse rewards and noisy transitions.
- By late 2025 he noted that KL penalty scaling itself was delicate and could cause instability and require heavy hyperparameter tuning if mishandled.
- By December 2025 the creator concluded that a new method (MGRPO) succeeded where prior approaches struggled, pointing to validation curves that plateaued rather than crashed as evidence that training could finally proceed longer without collapse.
milestones (6):
- 2025-01-20  `F-t8BwQpWa4#c012`  chunk_ids=['F-t8BwQpWa4:00240']
    GraphLoRA's graph router function helps solve the instability problems in LLMs caused by the imbalanced load issue of mixture-of-experts systems.
- 2025-03-15  `xqOAdmgUAC8#c070`  chunk_ids=['xqOAdmgUAC8:02790']
    OpenAI o3's report notes that a KL divergence penalty is used to keep the updated policy close to the pre-trained model's behavior, balancing exploration with stability during RL training.
- 2025-08-14  `hsyKnA6-QAA#c044`  chunk_ids=['hsyKnA6-QAA:00900']
    The Search-R1 authors found that masking alone is a necessary but not sufficient condition for stability, because sparse rewards and noisy environment transitions can still cause high variance, unstable updates, and potential mode collapse.
- 2025-11-03  `W_aqotP134s#c040`  chunk_ids=['W_aqotP134s:01320']
    The creator notes that the Kullback-Leibler scaling/penalty in PPO or GRPO-style updates is delicate, and if done incorrectly, training becomes unstable and requires heavy hyperparameter tuning.
- 2025-12-20  `LbUBncFv9yM#c051`  chunk_ids=['LbUBncFv9yM:01200', 'LbUBncFv9yM:01230']
    The creator finds support for his typo assumption in the paper's accuracy/validation curve, which shows accuracy reward increasing and validation accuracy plateauing rather than crashing at step 500-600, unlike the SRT-only case.
- 2025-12-20  `LbUBncFv9yM#c052`  chunk_ids=['LbUBncFv9yM:01200', 'LbUBncFv9yM:01230']
    The creator concludes that MGRPO stabilizes training such that the final model is also the best or a plateauing model, allowing training to run longer without fear of an immediate crash.


## Revised longitudinal categorization

A question belongs in `TIER 1` only when the thread shows genuine development: a stance changes, strengthens, weakens, or reverses; results evolve across attempts or versions; or an assessment is revised as new evidence arrives. Threads that show plausible but imperfect development remain in `TIER 2`; threads that mainly repeat a point, collect unrelated examples, or rely on a shared topic label remain in `SPOT-CHECK`.

Human-adjudication overrides are applied to `lc-0179`, `lc-0233`, `lc-0497`, `lc-0496`, `lc-0167`, and `lc-0011`.

### Final counts

| Final section | Count |
|---|---:|
| TIER 1 | 24 |
| TIER 2 | 14 |
| SPOT-CHECK | 13 |
| **Total** | **51** |

### TIER 1 (24)

- **lc-0130** — Original section: `TIER 1`
  Clear stance revision: repeated rejection of emergent intelligence becomes a conditional view that specific memory infrastructure might make it possible.
- **lc-0143** — Original section: `TIER 1`
  The idea develops from a GraphRAG design principle into a broader theory that reliable agency depends on externalizing memory, skills, protocols, and cognitive burdens.
- **lc-0398** — Original section: `TIER 1`
  The thread progresses from reward hacking as a theoretical risk to named exploit mechanisms, direct experimental evidence, and concrete mitigation strategies.
- **lc-0127** — Original section: `TIER 1`
  The benchmark itself becomes harder while model outcomes change across repeated tests, producing a genuine results-evolution arc.
- **lc-0452** — Original section: `TIER 1`
  The assessment moves from optimism about test-time compute to weak early gains, stronger later results, and skepticism about whether benchmark gains reflect true capability.
- **lc-0011** — Original section: `TIER 1`
  Human-adjudication override. Although some milestones are broad, the thread is retained as a high-priority arc about optimism for agentic AI giving way to stalled expectations and persistent reliability concerns.
- **lc-0123** — Original section: `TIER 1`
  DPO moves from being presented as a simpler alternative to reinforcement learning toward increasingly specific empirical and theoretical limitations.
- **lc-0344** — Original section: `TIER 1`
  The creator shifts from accepting quantization as a practical tradeoff to recommending against aggressive 4-bit quantization for demanding reasoning tasks.
- **lc-0349** — Original section: `TIER 1`
  RAG changes from the default answer for updating model knowledge into a temporary and structurally limited workaround as evidence accumulates.
- **lc-0337** — Original section: `TIER 1`
  Prompt optimization moves from a useful performance lever to a limited and often uneconomical technique whose gains may not justify their compute cost.
- **lc-0504** — Original section: `TIER 1`
  The creator moves from conceptual enthusiasm about world models to empirical skepticism after observing negligible or negative gains in actual tests.
- **lc-0418** — Original section: `TIER 1`
  The thread develops from surveying the promise of self-learning to hands-on implementation lessons and a stricter conclusion that small gains do not constitute genuine self-learning.
- **lc-0135** — Original section: `TIER 1`
  The creator’s error-analysis practice becomes more rigorous, moving from reporting external diagnoses to taxonomies, quantitative comparisons, and direct manual verification.
- **lc-0478** — Original section: `TIER 1`
  Early broad claims of transferable memories and skills are narrowed by later evidence showing that transferability may be task-specific rather than general.
- **lc-0061** — Original section: `TIER 2`
  Chain of thought moves from being treated as a useful reasoning technique to being questioned as unfaithful, manipulable, and ultimately an illusion.
- **lc-0014** — Original section: `TIER 2`
  The creator’s skepticism about AGI strengthens from doubt about scaling claims to treating AGI as marketing and describing development as moving away from emergent intelligence.
- **lc-0024** — Original section: `TIER 2`
  The assessment of AI reasoning hardens from cautious belief in its importance to the view that current systems roleplay rationality rather than genuinely implement it.
- **lc-0081** — Original section: `TIER 2`
  The view of long context becomes more qualified: larger windows appear practically ineffective, compression is favored, and later evidence adds only a narrower structural benefit.
- **lc-0223** — Original section: `TIER 2`
  The creator’s position develops from general discomfort with LLM judges to a more precise assessment involving agreement rates, training needs, expertise, and hallucination risk.
- **lc-0251** — Original section: `TIER 2`
  Memorization moves from being one training-stage effect to becoming a broader explanation for apparently strong reasoning and benchmark performance.
- **lc-0448** — Original section: `TIER 2`
  Task decomposition changes from a broadly useful default technique into something criticized as rigid and hard-coded, motivating more adaptive delegation.
- **lc-0481** — Original section: `TIER 2`
  The diagnosis of transformer limitations becomes more precise and is ultimately revised from an intrinsic architecture flaw to a mismatch between inductive autoregression and deductive work.
- **lc-0260** — Original section: `TIER 2`
  This is a clear reversal in results: 3B-class models go from being judged too small for the hardest puzzles to producing a previously unseen successful strategy.
- **lc-0169** — Original section: `SPOT-CHECK`
  The understanding develops from academic claims about implicit gradient descent to online SGD and literal inference-time weight updates, making it the strongest promotion from the original spot-check set.

### TIER 2 (14)

- **lc-0070** — Original section: `TIER 1`
  The benchmark-to-hands-on-failure portion shows real development, but later milestones describe alternative workflows rather than a revised assessment of code-generation reliability.
- **lc-0087** — Original section: `TIER 1`
  The topic has a plausible arc, but the stated trajectory says continuous learning was initially considered impossible while the first listed milestone already argues that RPT is continuous learning.
- **lc-0233** — Original section: `TIER 1`
  Human-adjudication override. The repeated-test history is strong, but it remains in TIER 2 rather than being promoted.
- **lc-0026** — Original section: `TIER 1`
  Concern clearly strengthens as evidence accumulates, but the question is extremely broad and combines several distinct safety problems.
- **lc-0388** — Original section: `TIER 1`
  The single-run-to-rerun arc is strong, but the later milestones appear to switch between Grok and Qwen and require entity reconciliation.
- **lc-0027** — Original section: `TIER 2`
  There is genuine development from autonomy claims to methodological criticism, but the initial optimism belongs to paper authors rather than clearly to the creator.
- **lc-0111** — Original section: `TIER 2`
  Coverage changes from praising DeepSeek’s architecture to noting performance weaknesses, but the milestones span several different assessment axes.
- **lc-0179** — Original section: `TIER 2`
  Human-adjudication override. The grokking explanation develops coherently, but it remains in TIER 2.
- **lc-0266** — Original section: `TIER 2`
  The preferred model changes, but the models appear to serve different purposes, making the trajectory partly a task shift rather than a clean preference change.
- **lc-0413** — Original section: `TIER 2`
  The optimism-to-skepticism arc is plausible, but the summary overstates early self-correction as spontaneous when models were prompted to check their answers.
- **lc-0497** — Original section: `TIER 2`
  Human-adjudication override. The verification arc is strong, but it remains in TIER 2.
- **lc-0496** — Original section: `TIER 2`
  Human-adjudication override. The verifiable-reward arc shows meaningful qualification over time, but it remains in TIER 2.
- **lc-0177** — Original section: `SPOT-CHECK`
  The diagnosis of GraphRAG becomes more detailed, but it is mostly an accumulation of limitations rather than a clearly revised position.
- **lc-0476** — Original section: `SPOT-CHECK`
  The thread develops a broader list of instability causes and mitigations, but still reads partly as a survey of distinct mechanisms.

### SPOT-CHECK (13)

- **lc-0019** — Original section: `TIER 1`
  The milestones concern unrelated forms of capability and do not form a defensible initial-view-to-revised-view trajectory.
- **lc-0296** — Original section: `TIER 1`
  The creator remains consistently favorable toward open source; later milestones mainly provide more supporting examples rather than changing the position.
- **lc-0407** — Original section: `TIER 1`
  The thread combines several different scaling phenomena under one broad label rather than tracing one evolving stance.
- **lc-0297** — Original section: `TIER 2`
  This is a chronology of criticisms of OpenAI across pricing, transparency, publicity, technology, and priorities without one stable evolving axis.
- **lc-0034** — Original section: `TIER 2`
  The Anthropic thread mixes pricing, architecture, revenue, IPO speculation, skills, and product strategy into a company-opinion history.
- **lc-0232** — Original section: `TIER 2`
  The phrase “local minimum” is reused across training, agent behavior, and prompt exploration, but these are separate applications rather than one development.
- **lc-0071** — Original section: `SPOT-CHECK`
  The milestones use “coherence” to mean several different phenomena, so the shared topic label does not support a coherent longitudinal arc.
- **lc-0077** — Original section: `SPOT-CHECK`
  The final optimistic claim comes from Gemini rather than a revised creator judgment, and the contradiction with earlier evidence is unresolved.
- **lc-0090** — Original section: `SPOT-CHECK`
  This is mainly a catalog of different cost-saving mechanisms, not a change in how the creator evaluates cost efficiency.
- **lc-0158** — Original section: `SPOT-CHECK`
  The milestones describe different kinds of gates in unrelated architectures; repeated use of the same term does not create development.
- **lc-0167** — Original section: `SPOT-CHECK`
  Human-adjudication override. Despite a plausible progression from observed GPT-5 failures to explanations and corroboration, it remains in SPOT-CHECK.
- **lc-0242** — Original section: `SPOT-CHECK`
  The thread links unrelated masking implementations and a later novelty judgment, but is too thin to establish genuine development.
- **lc-0365** — Original section: `SPOT-CHECK`
  The milestones assess different models’ reasoning traces rather than showing that the creator’s own standard or understanding changed.

### Movement from the original shortlist

| Original section | Total | Final TIER 1 | Final TIER 2 | Final SPOT-CHECK |
|---|---:|---:|---:|---:|
| TIER 1 | 22 | 14 | 5 | 3 |
| TIER 2 | 19 | 9 | 7 | 3 |
| SPOT-CHECK | 10 | 1 | 2 | 7 |

### Human-adjudication overrides

- `lc-0011` remains in **TIER 1**.
- `lc-0179`, `lc-0233`, `lc-0497`, and `lc-0496` remain in **TIER 2**.
- `lc-0167` remains in **SPOT-CHECK**.

