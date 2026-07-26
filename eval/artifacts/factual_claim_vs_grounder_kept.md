# Factual claim vs grounder chunks - kept set (26 of 50)

Filtered view of `factual_claim_vs_grounder.md`, keeping only the candidates the human marked KEEP (empty `notes:` field). The 24 dropped candidates and their reasons are in `factual_skips.md`; the full 50-candidate worksheet remains the source of record. Per candidate: the claim's own source chunk ids, the grounder's chunk ids, and the union of the chunk text (each chunk once, ordered by start).

## fc-0001

**question id:** fc-0001
**claim id:** EK96uN4Xt1o#c019
**question:** Which universities published ReasonFlux, and when did the paper come out?
**claim:** The creator states that Princeton University and Peking University already implemented this exact approach, publishing it on February 10th, 2025, calling it ReasonFlux.
**claim source chunks:** EK96uN4Xt1o:00540, EK96uN4Xt1o:00570
**grounder chunks:** EK96uN4Xt1o:00540, EK96uN4Xt1o:00570, EK96uN4Xt1o:00960, EK96uN4Xt1o:01260

**union chunk text:**
- `EK96uN4Xt1o:00540` [claim+grounder]  new idea no no no Princeton University already did it we are three weeks too late and you know what they did exactly what we just discovered what we just tried to come up with they published this on February 10th 2025 all our three steps now you know exactly the background to this study and you know exactly what they did you don't have to read here to study anymore by
- `EK96uN4Xt1o:00570` [claim+grounder]  Princeton and Peking University because this is one to one what they implemented so sometimes the PhD students here looking here for a great PhD topic sometimes they are faster than we are here on this YouTube channel okay Princeton you won this time let's have a look at the performance and I think this is really interesting and just look here at GPT the o1 system which is a huge system system and then open source LLM and
- `EK96uN4Xt1o:00960` [grounder]  mean that all the reasoning models also trained on all the textbook and math in the world still fail and why so there's a lot of research topics to be discovered let's talk in general about the limitations here about is now especially here about the implementation here by Peking University and Princeton University this reason flux so the success depends on the quality of those stored templates of the library of the reasoning path of mathematic they deducted
- `EK96uN4Xt1o:01260` [grounder]  running for 7 minutes maybe it would have needed run time inference run time of 27 minutes I don't noce but you see there's so much new research so much new topics that you can explore it you can try out it you can publish that you can go for this and I think we are just living in some beautiful exciting times what else this is it for today okay so you see Princeton University yes beautiful reasoning flux

**verdict:** 
**notes:** 

---

## fc-0002

**question id:** fc-0002
**claim id:** HM92mmG6YTs#c016
**question:** In the Autonomy of Experts (AoE) paper for mixture-of-experts models, what alternative do the authors propose to using a traditional router?
**claim:** The Autonomy of Experts paper proposes removing the router entirely, having experts pre-compute internal activation functions for the input and rank themselves based on activation norms.
**claim source chunks:** HM92mmG6YTs:00360
**grounder chunks:** HM92mmG6YTs:00360, HM92mmG6YTs:00420, HM92mmG6YTs:00540, HM92mmG6YTs:00720, HM92mmG6YTs:00870, HM92mmG6YTs:00900, HM92mmG6YTs:00930

**union chunk text:**
- `HM92mmG6YTs:00360` [claim+grounder]  is for me today filming this video 2025 autonomy of expert models and here from our colleagues in this beautiful new paper and they tell us you know what we get rid of one of the complexity we remove the router completely and instead the experts pre-compute internal activation functions for the input and those are ranked based on activation
- `HM92mmG6YTs:00420` [grounder]  overhead is now reduced through a low rank weight factorization so simple now looks beautiful we reduce the system complexity by getting rid of the routing functionality and we let the system self learn self decide and self select all expert now have access to the input data and they decide what to learn when to learn and the extension of what they want to learn and we use here we utilize
- `HM92mmG6YTs:00540` [grounder]  router in a traditional mixture of expert with a self- selection mechanism by expert key idea is that expert validate their own ability to process an input based on their internal activation Norms so how does each expert do this they pre-compute some activation they rank themselves and only the top K proceed the original method yes I need to break down the architecture step by step let me start with the expert structure I explain here the feed forward network
- `HM92mmG6YTs:00720` [grounder]  graph changes compared to a mixture of expert system in a mixture of expert or logic determine expert selection while in this new autonomy of expert the expert's own activation determine the selection the self selection procedure and this removes here completely the need for a separate router Network we can make our architecture much more beautiful much more more Sleek more elegant we reduce the risk of hallucination and error and whatever
- `HM92mmG6YTs:00870` [grounder]  of expert layer separate router module computes here the scores for each expert and chooses here the top K this new Roa removes here the router entirely expert self- selects whether should process the current token by evaluating here a partial low dimensional activation Norm correct formally all experts perform an initial inexpensive computation on the input token hidden State each expert compute the norm of its own partial activation and the side score it wants to process the token not
- `HM92mmG6YTs:00900` [grounder]  only the top K experts are selected and an optional load balancing loss encourages the model to avoid collapsing onto too few expert everything correct let's go here to the other side R1 a new paradigm reimagines here traditional mixture of expert architecture by decentralizing expert selection allowing expert to autonomously determine the suitability for the process input and then they do something nice R1 gives
- `HM92mmG6YTs:00930` [grounder]  us here the core component but already in a kind of a process way and this is a a summarization I like look we have the expert each expert is a modified feed forward network with factorized weights to enable efficient pre-computation of the activation with our low rank unlike s expands a central rout and instead uses activation Norm to self select then we have you already the core

**verdict:** 
**notes:** 

---

## fc-0004

**question id:** fc-0004
**claim id:** Q36yEz8seqQ#c021
**question:** On a benchmark comparing Qwen 2.5 to Stanford's S1 model trained with Gemini 2.0-improved reasoning data, how did the scores break down between Qwen 2.5, S1 without its test-time compute algorithm, and S1 with the algorithm activated?
**claim:** On one benchmark, Qwen 2.5 scored about 26.7%, while S1 with Gemini 2.0-improved reasoning data (without the test-time algorithm) scored nearly 50%, and activating the test-time compute algorithm added another 6.7 percentage points.
**claim source chunks:** Q36yEz8seqQ:00510, Q36yEz8seqQ:00540
**grounder chunks:** Q36yEz8seqQ:00510, Q36yEz8seqQ:00540

**union chunk text:**
- `Q36yEz8seqQ:00510` [claim+grounder]  encourage you more exploration so you see beautiful idea optimize the data and optimize here the algorithm and now I showed you what is the effect of both systems now we have here in the video I give you a detail explanation the q1 2.5 and if you take whatever test here let's say 26.7% and then we take the S1 model now with the Google Gemini improved
- `Q36yEz8seqQ:00540` [claim+grounder]  reasoning without here the if you would like to call it here this Advanced reasoning and I jump into performance Almost 100% look I go from 26% to 50% and then if I activate this algorithm test time computer optimization I just go up 6.7 percentage points if I have another Benchmark you see I just go up from 92.6 to 93.0 so 0.4 percentage point if

**verdict:** 
**notes:** 

---

## fc-0005

**question id:** fc-0005
**claim id:** EFtbWyo6cKE#c025
**question:** How much did the 'think' tool improve performance when Anthropic added it to Claude Sonnet 3.7 on tau-bench, given that the same idea reportedly failed to help a year earlier?
**claim:** The creator finds it fascinating that the same think-function idea that failed to help a year ago in tau-bench now produces more than a 50% performance increase when Anthropic added it to Sonnet 3.7.
**claim source chunks:** EFtbWyo6cKE:00570, EFtbWyo6cKE:00600
**grounder chunks:** EFtbWyo6cKE:00570, EFtbWyo6cKE:01200, EFtbWyo6cKE:01230, EFtbWyo6cKE:01680

**union chunk text:**
- `EFtbWyo6cKE:00570` [claim+grounder]  that later Anthropic showed us here called Claude Sonnet 3.7 if you want tools and you know what already a year ago the authors here of τ-bench told us we have also experimented with adding a think function for those function calling agent but it did not boost the performance and I was absolutely fascinating reading this one year old sentence because this is exactly what Anthropic did now to Sonnet 3.7
- `EFtbWyo6cKE:00600` [claim]  It added a think tool for their function calling agents. But why at this time it had no effect and why now a year later it has a more than 50% performance increase. Yes, it gets even better. It's really interesting. So let's have a look at the core idea. The τ-bench benchmark is the main thing that we have to understand to understand here the if you want think
- `EFtbWyo6cKE:01200` [grounder]  doing this flight reservation for example. Well there is now the detail that is important. Have a look at this. This is here from the official Sonnet Claude 3.7 Sonnet performance paper here. This airline task no rebook a flight. So we have here in blue the baseline performance here and you say okay that's the baseline and then we have the pure thinking tool performance in yellow and
- `EFtbWyo6cKE:01230` [grounder]  you see this is almost here a little bit better than baseline but look here it is baseline so the improvement is marginal almost nothing and then we have the extended thinking that was published a month ago you remember test time compute scaling 2 minutes is really thinking and thinking about this. This is your orange line and then then we have here the performance line. Look so much better performance. But what is
- `EFtbWyo6cKE:01680` [grounder]  now. And here official our research tells us that Anthropic has demonstrated that a Think tool can significantly enhance Claude 3.7's performance on complex task requiring policy adherence and reasoning in long chain of tool calls. So I honestly thought that this is already implemented in Sonnet 3.7. Sonnet is a new model. I saw it is already optimized to have those tool calls and even chains of tool calls but

**verdict:** 
**notes:** 

---

## fc-0006

**question id:** fc-0006
**claim id:** 4828sGfx7dk#c032
**question:** According to a Stanford study on agent frameworks, how often does Microsoft's AutoGen rely on a generalist single LLM/VLM approach rather than invoking other tools?
**claim:** According to the Stanford study, AutoGen uses the generalist (single LLM/VLM) approach about 90% of the time, rarely leveraging other tools.
**claim source chunks:** 4828sGfx7dk:00600
**grounder chunks:** 4828sGfx7dk:00600

**union chunk text:**
- `4828sGfx7dk:00600` [claim+grounder]  see they are really all the tool at work if we follow here the publication by Stanford University and they looked at autogen you see autogen 90% they just use here the generalist so this is almost like hey I just only use one LLM or VLM and the rest of the tools hardly hardly at all at work here to solve my problem and GPT function calling or LangChain stand for tells us hey this is the same so what I

**verdict:** 
**notes:** 

---

## fc-0007

**question id:** fc-0007
**claim id:** L-WfRaSPE2A#c026
**question:** What did Stanford's research on MinionS find regarding performance and cost when using an 8 billion parameter local LLM compared to relying solely on remote cloud LLMs?
**claim:** Stanford's research found that with an 8 billion parameter local LLM, MinionS can recover close to 98% of the performance of remote-only cloud LLMs at 18% of the cost of using the cloud model exclusively.
**claim source chunks:** L-WfRaSPE2A:00810
**grounder chunks:** L-WfRaSPE2A:00810, L-WfRaSPE2A:01260, L-WfRaSPE2A:01290

**union chunk text:**
- `L-WfRaSPE2A:00810` [claim+grounder]  performance I was looking for talking about performance Stanford tells us say across all the task and all everything M has just the feeling you know so if you have an 8 billion parameter and your local computer we can recover close to 98% of the performance of the remote only llms in the cloud at 18% of the cost of the cloud that would be if we go here full Cloud only and
- `L-WfRaSPE2A:01260` [grounder]  official screenshot of the official results here by the study we had a look at and they say hey yeah MinionS of course they say on average across multiple data set MinionS can recover close to 98% of the performance of the remote only language model while spending about six times less what a nice idea and they identify protocol hyper parameters that you have a specific flexibility in the trade between cost and quality if you in network operation
- `L-WfRaSPE2A:01290` [grounder]  beautiful have it jump in a paper and they tell us hey as the local models grow stronger so you go from an 8 billion maybe to a higher performance 8 billion the MinionS protocol becomes increasingly more cost effective and I think this makes sense no indeed hey soon some commodity Hardware laptops AI devices will feature more powerful gpus enabling here always own local

**verdict:** 
**notes:** 

---

## fc-0009

**question id:** fc-0009
**claim id:** bLBScrWDm6M#c063
**question:** What kind of evidence does the L1 paper present to support the claim that models use distinct reasoning strategies at different response lengths?
**claim:** The L1 paper's evidence for distinct reasoning strategies is based on a graph showing that the words 'therefore' and 'so' are used more frequently in shorter (e.g., 500 token) answers than in longer answers.
**claim source chunks:** bLBScrWDm6M:01650, bLBScrWDm6M:01680
**grounder chunks:** bLBScrWDm6M:01620, bLBScrWDm6M:01650, bLBScrWDm6M:01680, bLBScrWDm6M:01710

**union chunk text:**
- `bLBScrWDm6M:01620` [grounder]  strategies of their model L1 and they have here descendants L1 employs distinct reasoning strategies at different token budgets and they say hey this is kind of the specialty of L1. So, different token budget, I get it. If you have here, let's say 500 tokens or 4,000 tokens, okay, great. But to claim now that the reasoning strategies are
- `bLBScrWDm6M:01650` [claim+grounder]  different if you have 500 tokens on 4,000 tokens, I thought I have to have a closer look. So, how is this possible? And their idea that this is a valid sentence comes from this graph here. And they say you know when we looked for the words therefore and for the words so those two words here when we got we have given here the the reasoning LLM for k tokens to reason.
- `bLBScrWDm6M:01680` [claim+grounder]  We found that the word therefore was so much more used than before with only a 500 token answer. So therefore this conclusion drawing so this strategies, they are now distinct reasoning strategies because the word therefore and so are now used more. I personally do have a problem that those are distinct reasoning strategies. if you just count the word
- `bLBScrWDm6M:01710` [grounder]  therefore and so so maybe I'm wrong maybe this is the way to go and con absolutely beautiful intelligent people but claiming that L1 employs here distinct reasoning strategy a strategy for me as a much more complex object now counting here the word therefore if you have here a long chain of thought reasoning okay so yeah maybe you have your own opinion about this particular

**verdict:** 
**notes:** 

---

## fc-0010

**question id:** fc-0010
**claim id:** otujjZVoMZ4#c052
**question:** On average across benchmark scenarios, how much did REMA's multi-agent meta-thinking training improve performance over the baseline approaches?
**claim:** Averaged across all benchmark scenarios, the baseline approaches scored around 50-51%, and after the full multi-agent meta-thinking REMA training and optimization process, performance improved to approximately 53%.
**claim source chunks:** otujjZVoMZ4:02910, otujjZVoMZ4:02940, otujjZVoMZ4:02970
**grounder chunks:** otujjZVoMZ4:02910, otujjZVoMZ4:02940, otujjZVoMZ4:02970

**union chunk text:**
- `otujjZVoMZ4:02910` [claim+grounder]  the other models but also they give us you this performance dat and this is now on mathematical benchmarks so this is now really interesting we have a llama 3 and a q 2.57 be instruct and here you kind of see an interesting thing at first it is not really always the best model it's not really always outperforming here but let's have a look here the last line at the average line if we calculate
- `otujjZVoMZ4:02940` [claim+grounder]  everything from this one two three four different scenarios you see here we have on average over everything here a performance let's say from 50 here we have also a performance of 50 here we have also a performance of 50 maybe 51 and then after doing all of these things having two agent train two agents iteratively have you this extreme amount of training and optimization and and and what we achieve
- `otujjZVoMZ4:02970` [claim+grounder]  at the end we go with from let's say 51 to 53 so this opens up now the question how significant is this performance Improvement of a multi-agent meta thinking reasoning eval done with this new reinforcement learning methodology REMA is this is really a systematic methodology

**verdict:** 
**notes:** 

---

## fc-0012

**question id:** fc-0012
**claim id:** nPCjf6dSVj4#c042
**question:** On missing-data questions where the correct answer is to admit data isn't available, how do abstain rates compare between reasoning models like QwQ, Stanford S1, DeepSeek, and o3-mini versus non-reasoning models?
**claim:** For missing-data questions, the study found abstain rates (correctly stating data is missing) of 10% for QwQ, 16% for Stanford S1, 16% for DeepSeek, and 23% for o3-mini, compared to over 50% abstain rate for non-reasoning models.
**claim source chunks:** nPCjf6dSVj4:01320, nPCjf6dSVj4:01350
**grounder chunks:** nPCjf6dSVj4:01320, nPCjf6dSVj4:01350

**union chunk text:**
- `nPCjf6dSVj4:01320` [claim+grounder]  might say, yeah, but maybe just one LLM. No. And they made a beautiful study from QwQ here stand for S1, DeepSeek R1, DeepSeek R1 distilled, Q1 03 mini1 mini GPT. And they had here the reasoning models on the left side and the non-reasoning models here on the right side. Now let's just look here at this red line that goes up here. So for the reasoning model the question is the abstain rate
- `nPCjf6dSVj4:01350` [claim+grounder]  for missing data question when did it abstain QwQ 10%. Stanford 16% DeepSeek 16% 03 mini 23%. So it tried to solve it. It didn't say like a non-reasoning model with more than 50%. Hey buddy, data are missing. Stop. It tried to solve it because it was trained to provide a chain of sort and a

**verdict:** 
**notes:** 

---

## fc-0013

**question id:** fc-0013
**claim id:** UGmPJibHweA#c034
**question:** How does performance change as the supervised fine-tuning dataset size increases from 20,000 samples to 1 million samples?
**claim:** Scaling the supervised fine-tuning dataset size improves performance: with 20,000 data samples performance rises from about 16% to 50%, and with 1 million data samples it reaches about 70%.
**claim source chunks:** UGmPJibHweA:00720, UGmPJibHweA:00750
**grounder chunks:** UGmPJibHweA:00720, UGmPJibHweA:00750, UGmPJibHweA:00780

**union chunk text:**
- `UGmPJibHweA:00720` [claim+grounder]  is insufficient even with supervised fine tuning as long as you go. So the main obstacle here is an intrinsic instability in the deeper exploration and the computational demands. Have a look at this. This is a supervised fine-tuning data set scaling. So now we scale the data set size. And you know what? Look at this here on the y-axis zero to 100%. The more data sets we present here
- `UGmPJibHweA:00750` [claim+grounder]  to learn, the better the performance improvement. Look with 20,000 uh data samples. We are going here from whatever 16% to 50% and if we go to 1 million data set size for the supervised finetuning we come up to 70% performance. 70% is already where the big bosses play. This is the o1
- `UGmPJibHweA:00780` [grounder]  71%. You know I have a specific video on reinforcement learning how o1 was able to achieve this really interesting. So we can with supervised fine-tuning come close to the performance of reinforcement learning. So this means yes it is possible even for the hard level questions but now we have a different methodology because we have here logarithmic scaling pattern concerning now the supervised finetuning training data size for the

**verdict:** 
**notes:** 

---

## fc-0015

**question id:** fc-0015
**claim id:** Sl01ptD4u4Q#c033
**question:** What happens to entropy and reasoning quality when off-policy traces are naively combined with on-policy learning during training?
**claim:** Naively combining off-policy traces with on-policy learning causes an immediate entropy collapse to a single solution, leading to overly rapid convergence and the model latching onto superficial patterns rather than genuine reasoning.
**claim source chunks:** Sl01ptD4u4Q:00900, Sl01ptD4u4Q:00930
**grounder chunks:** Sl01ptD4u4Q:00900, Sl01ptD4u4Q:01110, Sl01ptD4u4Q:01170

**union chunk text:**
- `Sl01ptD4u4Q:00900` [claim+grounder]  computation little tiny insignificant problem. We have an immediate entropy collapse to one solution. Oh and you say okay so we encounter a problem. Never mind. So what is the problem? Naively combining now the off policy traces can lead now to an overly rapid convergence and a complete entropy collapse of the complete system causing the model to latch onto superficial patterns rather than acquiring here some real genuine
- `Sl01ptD4u4Q:00930` [claim]  reasoning capabilities. And if you think about it it's clear. So we have to come up with some new ideas. The results if we do that in Luffy and if we read here at the end of the publication of Luffy they say hey we found a way and it encourages the language model to imitate here the high quality reasoning traces from R1 while maintaining the exploration of its own
- `Sl01ptD4u4Q:01110` [grounder]  while the mixed policy incorporates now off policy rollouts successfully via importance sampling a new practical challenges a new problem emerges the importance sampling accelerates the convergence but significantly reduces the exploration. We don't want this. We want exploration. We want exactly this beautiful delicate equilibrium. Exploring here with our flashlight, the dark room in front of us
- `Sl01ptD4u4Q:01170` [grounder]  time. However, as it turns out we have again the entropy collapse even much faster than on the on policy reinforcement learning. So this is not what you want. Your collapse, your entropy collapse is now almost immediately. So indicating increasingly deterministic rollouts and a diminished capacity for exploring diverse reasoning trajectories. But you want your AI to be

**verdict:** 
**notes:** 

---

## fc-0017

**question id:** fc-0017
**claim id:** 11RCxGqXtKc#c017
**question:** In the context of an AI system built for laser fusion experiments, what is it actually designed to do if its purpose goes beyond just writing code?
**claim:** The creator explains that the system is not about writing code but about automating the scientific method itself: experiment, discover, reason about results, form new hypotheses, formulate new experiments with new parameters, run a digital twin simulation, and if successful, run the real laser fusion experiment, then repeat the loop.
**claim source chunks:** 11RCxGqXtKc:00300, 11RCxGqXtKc:00330
**grounder chunks:** 11RCxGqXtKc:00300, 11RCxGqXtKc:00330

**union chunk text:**
- `11RCxGqXtKc:00300` [claim+grounder]  critical science application. So they tell us great but you know there are also some gaps you you do not want to have in laser fusion no if you have an autonomous use of AI agents for safety critical science applications but to be clear it is not about writing code it is already the next step it is about automating the scientific method itself experiment discover reason about the
- `11RCxGqXtKc:00330` [claim+grounder]  results have a new hypothesis, have a new idea, formulate it, build a new experiment with new parameter, with new hyperparameter, run a digital twin, simulate this new idea and if the simulation works out, go to the big machine and run the laser fusion experiment in real time and then the loop starts all over again. So, I think a beautiful experiment here end of June 2025.

**verdict:** 
**notes:** 

---

## fc-0020

**question id:** fc-0020
**claim id:** cHVQj7w9TD4#c016
**question:** What recall rate did Deep Retrieval achieve on publication search compared to the state-of-the-art method?
**claim:** Deep Retrieval outperformed leading literature search methods, achieving 65% recall for publication search compared to a SOTA of 24% recall.
**claim source chunks:** cHVQj7w9TD4:00450
**grounder chunks:** cHVQj7w9TD4:00450

**union chunk text:**
- `cHVQj7w9TD4:00450` [claim+grounder]  literature search if you are searching you know literature search with 65% and SOTA is 24% recall for publication search. So this is a big jump. So this is something where we say okay if we let the system train to optimize itself not the human search query but hey let it search and let it optimize itself. This is where AI shines. If you

**verdict:** 
**notes:** 

---

## fc-0021

**question id:** fc-0021
**claim id:** bJSAcfQgxAg#c023
**question:** How many button presses did GPT-OSS-120B use in its solution to the elevator causal reasoning test?
**claim:** GPT-OSS-120B produced a 15-press solution to the elevator causal reasoning test.
**claim source chunks:** bJSAcfQgxAg:00270, bJSAcfQgxAg:00330
**grounder chunks:** bJSAcfQgxAg:00270, bJSAcfQgxAg:00330

**union chunk text:**
- `bJSAcfQgxAg:00270` [claim+grounder]  Not bad at all. 4 seconds and we have a solution. The 15-press solution. Beautiful. So you see this is here the riddle that we have. Okay. Floor 4850. So it did not find here the shortcut. We have here different code cards. Item to run. It presses use 15. We have energy enough. We have the code cards collected. We have no trap hits.
- `bJSAcfQgxAg:00330` [claim+grounder]  the elevator from floor 0 to 15. 15 moves respecting every rule maybe, but the solution is horrible. The fewest possible presses that meet all the constraints simultaneously. So a 15 press solution is really bad. And especially if this is the new GPT, the open-source model here with 120 billion free trainable parameter. I think this is yeah this is not really

**verdict:** 
**notes:** 

---

## fc-0026

**question id:** fc-0026
**claim id:** C7WcaYjR2E8#c047
**question:** How does the 14B Deep-DxSearch model compare in performance to the much larger 671B DeepSeek R1 system on common versus rare disease diagnosis tasks?
**claim:** The 14B Deep-DxSearch model outperforms a 671B DeepSeek R1 system by nearly 20 percentage points on common disease diagnosis and nearly 30 percentage points on rare disease diagnosis.
**claim source chunks:** C7WcaYjR2E8:01110
**grounder chunks:** C7WcaYjR2E8:01110

**union chunk text:**
- `C7WcaYjR2E8:01110` [claim+grounder]  think this is the right track. Yeah, if you go here with the classical open-source system like a DeepSeek R1, you'll see that this 14 billion here outperforms here a 671 billion R1 system nearly 20 percentage points. And if you go here for the rare diseases, you see by nearly 30 percentage points and if you want to have the real percentage is an improvement of over 150%. If you go with

**verdict:** 
**notes:** 

---

## fc-0031

**question id:** fc-0031
**claim id:** mOjWG7hxPUI#c049
**question:** How does the rank of the weight update differ between standard fine-tuning and in-context learning (ICL), and why does this make ICL's update fast, temporary, and specific to the current token position?
**claim:** Standard fine-tuning updates the whole weight matrix (rank N), making it expensive and slow, whereas ICL uses only a rank-one update, making it fast, temporary, and hyper-specific to the current token position due to non-linearity.
**claim source chunks:** mOjWG7hxPUI:01590
**grounder chunks:** mOjWG7hxPUI:00810, mOjWG7hxPUI:00840, mOjWG7hxPUI:00990, mOjWG7hxPUI:01020, mOjWG7hxPUI:01500, mOjWG7hxPUI:01530, mOjWG7hxPUI:01560, mOjWG7hxPUI:01590, mOjWG7hxPUI:01620, mOjWG7hxPUI:01710, mOjWG7hxPUI:01740, mOjWG7hxPUI:01770, mOjWG7hxPUI:01800

**union chunk text:**
- `mOjWG7hxPUI:00810` [grounder]  And then this is here, if you want, a correction term that is now coming not from the content, from the attention, but now we can go and operate with virtual weight structures. So, we have now this bridge suddenly connecting fine-tuning and in-context learning. Now, of course, as I showed you, no? You can do this here with a rank-one solution, no? If you go with an outer product, simple, no?
- `mOjWG7hxPUI:00840` [grounder]  So, mathematically we can say adding now the attention output A to the input is identical to updating the weight matrix W by adding here a rank-one matrix delta W. So, the activation pattern A from the attention layer becomes the source of the weight update delta W in ICL. So, we have now this beautiful connection between fine-tuning and ICL
- `mOjWG7hxPUI:00990` [grounder]  connections, no? And this is why I did not take here this publication by Google here from July 2025 really that significant, no? Because I thought, hey, the simple algebra doesn't hold if you input non-linear activations, no? But this team of authors now proved here, just 2 weeks ago, that it holds. And this is something, okay. But they have a second insight that the update delta weight becomes specific to
- `mOjWG7hxPUI:01020` [grounder]  the token position. So, we calculate, in given the non-linearity, a delta W for each single token position. Now this thing becomes a little bit more interesting, no? So, the weights are effectively different for every single token that is generated by our auto-regressive system. The model isn't just fine-tuned once. It is now with ICL continuously refining tuning itself at every step of the generation of the next token prediction
- `mOjWG7hxPUI:01500` [grounder]  virtual weight updates. Yeah, this is the core contribution of these two papers today. They mathematically prove that you can take the vector rotation from step one and move it into the weight matrix representation. So, instead of now saying the input rotated, we say the input staying the same, but the weight matrix representation morphed into a new configuration with our delta W. So, we are newly learning just a rank
- `mOjWG7hxPUI:01530` [grounder]  one patch. Yeah. The paper has really proved that the update is rank one. Remember our outer product here? And this is crucial because a rank one matrix is the simplest possible modification you can make to this matrix, now. It doesn't rewrite your whole brain. It just creates this very specific bridge between one input pattern and one output pattern. And this is what we achieve.
- `mOjWG7hxPUI:01560` [grounder]  Yeah, if you have a question, what is a rank one matrix delta W? So, now we can really see ICL is the process of using the activations to temporarily fine-tune the AI model by injecting rank one patches into the frozen weight matrices. This is ICL now seen in the weight space. So, we have now a complete new interpretation for what is ICL and how
- `mOjWG7hxPUI:01590` [claim+grounder]  it connects now to the fine-tuning understanding that we have in a transformer. Again, well, fine-tuning updates the whole matrix, a rank N, expensive, slow. It changes everything in the tensor structure. ICL update using a rank one only. Therefore, it is fast, temporary, and hyper-specific because of the non-linearity to the current token position. So, this is done for each and every single token.
- `mOjWG7hxPUI:01620` [grounder]  Therefore, a rank one update is this one dimensional bridge. It doesn't rewrite the model's understanding of physics or grammar. What it does is it essentially draws a single straight line in a high-dimensional vector space to the neural space connecting here point A, this is our input, to the desired output. But mathematically, I can see it. I just cannot imagine it yet. I have not found the image, you know.
- `mOjWG7hxPUI:01710` [grounder]  old grandfather, on the prompt examples. So, now we have the connections between those two worlds. So, if the mathematics is indeed absolutely identical, why don't we just call ICL fine-tuning? Well, there is still a simplicity in this mathematical proof, now. The rank one constraint. Standard fine-tuning usually updates here every parameter in that matrix. So,
- `mOjWG7hxPUI:01740` [grounder]  we have a full rank matrix, now. ICL is restricted here in this first approach to a rank one update, the most important update. Now, we don't know if Let's see, you have here You don't know if the further ranks updates will really converge here to the full rank update. We have not yet seen a mathematical proof for this. I can imagine it, but I can't prove it. But the most important thing is we have
- `mOjWG7hxPUI:01770` [grounder]  now, given here the simplicity of a rank one, this is a simplified gradient descent, now. It updates the weight along a single most important direction. You see here, we go into our most important subspace, orthogonal subspace, defined by the attention mechanism. This I can imagine it cannot perform complex multi-directional optimization in a single step. So therefore here we have it. This is
- `mOjWG7hxPUI:01800` [grounder]  now the new understanding of ICL. In-context learning is effectively transient rank one online stochastic gradient descent performed hold on to your socks on the forward pass. I hope you enjoyed this video. It was really not easy to produce this video because I'm still struggling with this. I'm This is such a deviation from my old knowledge here

**verdict:** 
**notes:** 

---

## fc-0032

**question id:** fc-0032
**claim id:** SMdaxjkTIJA#c006
**question:** What score did Gemini 3 Deep Think achieve on the ARC-AGI-2 benchmark?
**claim:** Gemini 3 Deep Think scores 45% on the ARC-AGI-2 benchmark.
**claim source chunks:** SMdaxjkTIJA:00030
**grounder chunks:** SMdaxjkTIJA:00030

**union chunk text:**
- `SMdaxjkTIJA:00030` [claim+grounder]  thinking the extreme model? Look, it outperforms everything on this planet. No, not interested. And you say, what about an independent benchmark AGI 2 leaderboard? Look, Gemini 3 Pro outperforms Grok, Claude Sonnet, GPT-5, everything. And Gemini 3 Deep Thinking is even at 45% Agi 2. Come on, who is interested in this? If we can do our own testing, look at this. There are some logical dependencies that are really strange to guess. And you might

**verdict:** 
**notes:** 

---

## fc-0033

**question id:** fc-0033
**claim id:** nYKbnsZ-V3A#c051
**question:** In Nemotron Elastic's multi-size training setup with 6B, 9B, and 12B models, what went wrong when the training budget was sampled uniformly across the three sizes?
**claim:** Researchers found that if the training budget across the 6B, 9B, and 12B models was sampled uniformly, gradient updates from struggling smaller models overwhelmed the fine-tuning of the larger models, causing the 12B model to become less capable ('more stupid').
**claim source chunks:** nYKbnsZ-V3A:01200
**grounder chunks:** nYKbnsZ-V3A:01200

**union chunk text:**
- `nYKbnsZ-V3A:01200` [claim+grounder]  managed. Now, think about this. Normally would we have let's say chain of thought I only have about 100 videos about chain of thought. So they need let's say just thousands of tokens and the researcher found that if they sampled the budget uniformly so train here the 6B, 9B and 12B equally the gradient updates from the struggling small models overwhelmed now the fine tuning of the larger models and this had a simple effect that we know that the 12B model just became more stupid. So we

**verdict:** 
**notes:** 

---

## fc-0036

**question id:** fc-0036
**claim id:** 6XgoRzZ3Rw0#c011
**question:** What is 'equilibrium matching,' the technique developed by researchers from MIT, Oxford, and Harvard, and how does it bridge two different model architecture paradigms?
**claim:** The creator states that MIT, Oxford, and Harvard University built a bridge function between two model architecture 'kingdoms,' calling it 'equilibrium matching,' which the creator characterizes as a revolutionary unification.
**claim source chunks:** 6XgoRzZ3Rw0:00240
**grounder chunks:** 6XgoRzZ3Rw0:00240

**union chunk text:**
- `6XgoRzZ3Rw0:00240` [claim+grounder]  everywhere. So if you're really interested here in this particular architecture manifold in this video I showed you here we have diffusion models we have flow-based models we have energy based models and really in my last video I showed you here the results of MIT Oxford and Harvard University they build now here a bridge function between those two and they call it an equilibrium matching this is a revolutionary unification of these two kingdoms here and this is if you want have a deep

**verdict:** 
**notes:** 

---

## fc-0038

**question id:** fc-0038
**claim id:** 7d4bEfj7wmc#c014
**question:** What did the VLM4VA paper's ablation study find about the correlation between a vision-language model's performance on standard visual question-answering benchmarks and its success rate in robotic manipulation tasks?
**claim:** The VLM4VA paper's core innovation is a systematic ablation demonstrating the visual-semantic gap in real AI systems, finding zero correlation between a vision-language model's performance on standard vision question-answering benchmarks and its success rate in robotic manipulation.
**claim source chunks:** 7d4bEfj7wmc:00270, 7d4bEfj7wmc:00300
**grounder chunks:** 7d4bEfj7wmc:00300, 7d4bEfj7wmc:00330

**union chunk text:**
- `7d4bEfj7wmc:00270` [claim]  transformer. You have here the prediction here of a particular horizon. Let's say 10 steps into the future. And you have a particular loss function that you need here for this a movement weighted loss function because the standard L2 loss is sparse because most of the world here is static. We use here mask derived here from the ground truth movement. The beauty about VLM for real world for the action model is the semantic control gap. What is the core innovation
- `7d4bEfj7wmc:00300` [claim+grounder]  systematic ablation providing here the visual semantic gap in real AI systems. So zero correlation between a vision language model's performance on standard vision question and also benchmarks and its success rate in robotic manipulation. zero correlation between those two and even fine-tuning here on an embodied vision question and answer system here does not significantly improve here to control the robotic performance at all. So this is a massive
- `7d4bEfj7wmc:00330` [grounder]  problem that we have even when the vision encoder is frozen relying here on pre-trained semantic features the vision language action model performances simply collapses. So this means in a conclusion the feature required for the control are orthogonal to the semantic features. Therefore, the vision encoder must be updated to learn here a real physical physics representation. We cannot proceed with semantic alone. Mambbox simple core innovation replacing

**verdict:** 
**notes:** 

---

## fc-0040

**question id:** fc-0040
**claim id:** M_Ic8Y6OQZ8#c003
**question:** Approximately how many high-quality quintuples and how many 3D knee MRI volumes make up the dataset built by researchers affiliated with Harvard Medical School?
**claim:** The dataset comprises close to 500,000 high quality quintuples derived from about 8,000 three-dimensional knee MRI volumes.
**claim source chunks:** M_Ic8Y6OQZ8:00060
**grounder chunks:** M_Ic8Y6OQZ8:00060, M_Ic8Y6OQZ8:00090

**union chunk text:**
- `M_Ic8Y6OQZ8:00060` [claim+grounder]  are now much more capable of reasoning especially if we have complex three-dimensional visual medical data. So they said okay what we start with is humans. So we have here now we have to provide our data set. So we have to provide now human created data and they have close to 500,000 high quality quintuples derived from about 8,000 three-dimensional knee MRI volumes here and they said we have to build ground
- `M_Ic8Y6OQZ8:00090` [grounder]  reasoning data set that go with our 3D images but also with as in close to 450 hours here of human expert annotated reasoning traces each of those close to 500,000 quintuples include here the 3DMR, a diagnostic question targeting here the specific region, a bounding box here on this image plus and now the beauty is here a clinician generated diagnostic reasoning stepbystep

**verdict:** 
**notes:** 

---

## fc-0042

**question id:** fc-0042
**claim id:** QYQyATL0EbM#c041
**question:** How many button presses did Qwen 3.5 397B-A17B end up using to solve the elevator puzzle, and was that considered a good result?
**claim:** The final result for Qwen 3.5 397B-A17B was a 19-press solution, and the creator states this is not a good result.
**claim source chunks:** QYQyATL0EbM:00810
**grounder chunks:** QYQyATL0EbM:00780, QYQyATL0EbM:00810

**union chunk text:**
- `QYQyATL0EbM:00780` [grounder]  We have Yeah, another solution. 13 button presses. Okay, it's not good, but at least it would be a solution. Yeah. So, let's have a look. 13 button presses. We have the exit. Beautiful. Ah, the final APC is three. To meet the constraint, two additional B bonuses moves are inserted between N in the optimized run extending the run to 19 presses but securing. Okay.
- `QYQyATL0EbM:00810` [claim+grounder]  Okay. So it is not able to meet the energy domain. So therefore the final stats is here 19 presses. So no this is not it. Yeah.

**verdict:** 
**notes:** 

---

## fc-0043

**question id:** fc-0043
**claim id:** 2POdg38T1Ec#c027
**question:** How does ALOE's intrinsic reward function work, and why does it rely on eigenvectors of a state graph rather than a simple error signal?
**claim:** ALOE measures geometric diffusion on a topological space rather than a simple error, calculating eigenvectors of the state graph to reward the agent for reaching states that are mathematically furthest apart.
**claim source chunks:** 2POdg38T1Ec:00600, 2POdg38T1Ec:00630
**grounder chunks:** 2POdg38T1Ec:00600, 2POdg38T1Ec:00630, 2POdg38T1Ec:00660, 2POdg38T1Ec:00690, 2POdg38T1Ec:00780, 2POdg38T1Ec:00810, 2POdg38T1Ec:00840

**union chunk text:**
- `2POdg38T1Ec:00600` [claim+grounder]  extremely well in this specific paper if you want to have little bit of a mathematical deep dive. They experiment with a very sophisticated intrinsic reward function and they call aloe augmented lronian lelationian objective. Let me explain this a little bit. Normally you would measure an error. Now this thing measures a geometric diffusion on a topological space. So what it does it calculates the eigen
- `2POdg38T1Ec:00630` [claim+grounder]  vectors of the state graph to reward the agent for going to states that are mathematically furthest apart. So it is like rewarding here the the fleet of scouts for maximizing the spread of the search party. So you want to really go to every little corner of your mathematical space and explore that over there maybe there is the solution that you're looking for. has this extrinsic reward function that you are looking for. So this is a very advanced in intrinsic
- `2POdg38T1Ec:00660` [grounder]  reward function but it is really nice because the uh limitation they impose on it and the way they handle it tells us a lot of about if you want to code your next reinforcement. So you might ask now so what is ALOE what we do now it is rather simple look we just have three terms and you see oh a Lagrange multiplier and something about this smoothness and you immediately understand what we're doing we use here
- `2POdg38T1Ec:00690` [grounder]  the augmented Lagrangian method this is if you want a classical numerical optimization trick to turn our constraint that we have on the system like orthogonality here and vectors into a specific loss function. Just look at the Lagrange multiplier here with our lambda term. You immediately understand what I mean architecture and flow is now really important how to bring our insights back back to the base policy. So let's start.
- `2POdg38T1Ec:00780` [grounder]  it finds. Now the goal of this scout network is different. They want to maximize the intrinsic reward function. And of course, as I just showed you, we have now a topological optimization module called Alo. It's simply, if you want, calculating the vectors. And the role of the geometric is simple. It observes here the state and outputs you a particular vector representing where the agent is in the topology of our mathematical space. The goal is simply
- `2POdg38T1Ec:00810` [grounder]  to learn a smooth mapping of the environment or if you want a little bit more professional minimize the spectral loss. So let's have a look how they work together. A scout at the beginning enters an environment for n let's say five update steps. It interacts now with network 3 with aloe. So scout sees states and moves here to the next state resulting now alo. This cloud sends here the state
- `2POdg38T1Ec:00840` [grounder]  observation to the network 3 and network 3 simply calculates here the diffusion distance. How far apart are those two states in the metric structure of our space. So if you want the interpretation of this step is if this scout moved through a bottleneck a doorway if it's a robotic system and an exploring a house the values will change drastically. If a scout will hit a wall, our internal reward structure will stay low.

**verdict:** 
**notes:** 

---

## fc-0044

**question id:** fc-0044
**claim id:** anEVsOPtbnw#c019
**question:** In few-shot Q&A examples like 'France->Paris' and 'Japan->Tokyo', why does the geometric transition from country to capital appear as a discontinuity rather than a straight line?
**claim:** In a few-shot Q&A example (e.g., 'France->Paris', 'Japan->Tokyo'), the transition from country to capital is not a straight line but a discontinuity, indicating the model uses a different, nonlinear geometric mechanism to jump from country to capital.
**claim source chunks:** anEVsOPtbnw:00540
**grounder chunks:** anEVsOPtbnw:00510, anEVsOPtbnw:00540, anEVsOPtbnw:00570, anEVsOPtbnw:00690, anEVsOPtbnw:00720, anEVsOPtbnw:00750

**union chunk text:**
- `anEVsOPtbnw:00510` [grounder]  makes the next generation of AI so much easier. And I know what you're going to say. Wait, you say, but I just looked at the study. And Google discovered in this new study that the straightening fails in particular cases. And those particular cases are now also important for in-context learning. Those are our few short Q&A. So prompt question France answer Paris
- `anEVsOPtbnw:00540` [claim+grounder]  question Japan answer Tokyo you know exactly that we are looking here for the capitals of those nations. How is this working? Now it turns out the transition here in a Q&A is not a straight line. It is not a continuation of the previous token. Of course look at this. This is an interruption. This is a discontinuity. So the model uses now a different geometric mechanism to jump here from the country to the capital. This is a
- `anEVsOPtbnw:00570` [grounder]  nonlinearity. But there's another way to think about this. The strongest argument that we have for this linear representation hypothesis is the architectural concept of our transformers today because the transformer is defined by the residual stream. So mathematically you see here the residual stream the output xL is just here the input plus a sum of updates where those are represented here as high dimensional vectors or tensor space.
- `anEVsOPtbnw:00690` [grounder]  And now the insight of this new study is that this linearity is only valid for the flow not for the reasoning of our. So suddenly we do have a threshold. We do have a phase transition where Google tells us listen we found something new. We found that this beautiful linearity theorem is valid for a natural coherent flow of information, but it falls apart
- `anEVsOPtbnw:00720` [grounder]  the moment we start to do reasoning. This linear extraction hypothesis is only valid for tasks that rely on continuity like the human English natural language flow or induction heads repeating here patterns here. This is what we know. This preprint shows us here for the first time that when the model performs reasoning, this straightening matrix here, this internal representation of the hidden state, this matrix collapses.
- `anEVsOPtbnw:00750` [grounder]  Some new mechanism emerges, some new manifold suddenly becomes active. And I tell you this with a big smile. Well, to solve here the reasoning task, Google tells us the model does not extrapolate anymore along a line. Now the transformers perform a nonlinear jump and of course you know this is a kind of a manifold hop to a higher dimensional rotational. So this means the IMAL is able to

**verdict:** 
**notes:** 

---

## fc-0045

**question id:** fc-0045
**claim id:** WpBdSdij28Y#c031
**question:** In a multi-agent system, how does the time required to reach consensus scale with population size, message bandwidth M, and the adaptation rate alpha?
**claim:** The paper's author derives that the time to reach consensus in a multi-agent system grows quadratically with population size, grows linearly with message bandwidth (M), and shrinks quadratically with the adaptation rate alpha.
**claim source chunks:** WpBdSdij28Y:00690, WpBdSdij28Y:00720
**grounder chunks:** WpBdSdij28Y:00720

**union chunk text:**
- `WpBdSdij28Y:00690` [claim]  in this communication protocol. Given here a specific entropy, given here a specific drift, given here some Yeah, I will show you the effect in a moment. Coming back here to the paper, we have here interesting elements about the consensus time and the scaling laws itself. And they have here some approximation, of course, but the authors derived here the author, singular, derives here the collective time to a consensus.
- `WpBdSdij28Y:00720` [claim+grounder]  And this is highly interesting because this means that the time to reach a consensus in a multi-agent system grows quadratically with the population size and linearly with the message bandwidth itself, or M. But it shrinks quadratically with the adaptation rate alpha. This is something that is absolutely fascinating. Now, before we enter now the geometric, my geometric interpretation of this mathematical methodology for you, just

**verdict:** 
**notes:** 

---

## fc-0048

**question id:** fc-0048
**claim id:** VcYngMi9gSI#c029
**question:** In the 'asymmetric prediction paradox' finding, what accuracy did an auto-rater achieve when predicting honest ('label A') outcomes from the reasoning traces of a Gemma 27B model?
**claim:** In the 'asymmetric prediction paradox' finding, an auto-rater reading the reasoning traces of a Gemma 27B model predicted honest ('label A') outcomes with 97% accuracy.
**claim source chunks:** VcYngMi9gSI:01080, VcYngMi9gSI:01110
**grounder chunks:** VcYngMi9gSI:01080, VcYngMi9gSI:01110

**union chunk text:**
- `VcYngMi9gSI:01080` [claim+grounder]  findings that I really love to show you and I would like to show you doing empirical um tests or experiments is just amazing giving you the insight but then somehow you have to bring them all together for a working theory and you decide if they succeed. So let's start the asymmetric prediction paradox beautifully. So an auto raider reading here a gamma 27B model the reasoning traces of it predict now the honest the
- `VcYngMi9gSI:01110` [claim+grounder]  label a outcomes with 97% accuracy and you say amazing so the reasoning traces really give us predict us what the decision will be honest label A but the deceptive outcomes are essentially at 50/50 chance, no 53% after reading about 1,000 samples so they say okay this is a result but now the interpretation of this result is interesting yeah but there's another specific finding the almost survival

**verdict:** 
**notes:** 

---

