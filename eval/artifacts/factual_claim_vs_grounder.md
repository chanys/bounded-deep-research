# Factual claim vs grounder chunks (50 candidates)

Per candidate: the claim's own source chunk ids, the grounder's chunk ids, and the union of the chunk text (each chunk once, ordered by start).

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

## fc-0003
**question id:** fc-0003
**claim id:** 6whj28Q6ujA#c045
**question:** How does dialogue tuning affect reasoning performance across basic, advanced, and challenging difficulty levels compared to other forms of training data?
**claim:** The study authors investigated three research questions and found that dialogue tuning improves reasoning across basic, advanced, and challenging levels compared to other data forms.
**claim source chunks:** 6whj28Q6ujA:00990
**grounder chunks:** 6whj28Q6ujA:00780, 6whj28Q6ujA:00990

**union chunk text:**
- `6whj28Q6ujA:00780` [grounder]  supervise or we fine tuned in this LLM exactly on this dialogue based data set so our Llama 3B or 8B become now a advanced supervised fine tuned llm that we then can have here the new Benchmark and if we do this we see that in the easiest case we have a 10% performance increase and this is interesting because if you go to higher complexity you see
- `6whj28Q6ujA:00990` [claim+grounder]  come to an end the authors investigated three different questions and now they provide us with their answer but the first question was hey what is the effect of the dialogue tuning here on the reasoning compared to the other forms and the result that the authors tell us hey it improves the reasoning across the board from basic advanced and challenging levels second does combining here the dialogue data sets improve the reasoning yes it outperforms every other choice and third can a dialogue tune

**verdict:** 
**notes:** The question is non specific. Not a good question. Drop. 

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

## fc-0008
**question id:** fc-0008
**claim id:** xHUgONA-x3g#c018
**question:** How did the 'agentic reasoning' approach compare to the other models or modes tested on a PhD-level benchmark?
**claim:** The paper's 'agentic reasoning' approach achieved the best performance among all compared models/modes on this PhD-level benchmark.
**claim source chunks:** xHUgONA-x3g:00450
**grounder chunks:** xHUgONA-x3g:00420, xHUgONA-x3g:00450

**union chunk text:**
- `xHUgONA-x3g:00420` [grounder]  but hey you know a mind map is just a two-dimensional projection from a three-dimensional or n-dimensional Knowledge Graph so we will not limit ourselves in our intellectual task here and here we have the results so this is here of uh University of Oxford official results performance comparison here on a PhD level multiple choice Q&A Benchmark where we have questions here physics chemistry and biology and here you have all the different modes beautiful and then you see of course in the last line
- `xHUgONA-x3g:00450` [claim+grounder]  here where they say agentic reasoning yeah they call this agentic reasoning and of course this has here more or less the best performance of all the other models beautiful so you see there is something to it if you have your multiple agents that are really specialized for their task where you have really numerical simulation that you can run that you get real data back here from the simulation to help you decide for example on your next investment and then here in the table two with human experts and as you

**verdict:** 
**notes:** The question is non specific. Suggest to drop this question. 

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

## fc-0011
**question id:** fc-0011
**claim id:** SgknC9B1dm8#c009
**question:** In an elevator puzzle test, o4-mini claimed its 20-step solution was Pareto optimal with no strictly shorter sequence possible - was that claim actually correct, especially compared to Gemini 2.5 Pro's solution?
**claim:** o4-mini claimed its 20-step solution was Pareto optimal and that no strictly shorter sequence was possible, despite Gemini 2.5 Pro finding a shorter 10-step solution.
**claim source chunks:** SgknC9B1dm8:00060, SgknC9B1dm8:00090, SgknC9B1dm8:00120, SgknC9B1dm8:00150, SgknC9B1dm8:00210
**grounder chunks:** SgknC9B1dm8:00060, SgknC9B1dm8:00090, SgknC9B1dm8:00120, SgknC9B1dm8:00150, SgknC9B1dm8:00270, SgknC9B1dm8:00300

**union chunk text:**
- `SgknC9B1dm8:00060` [claim+grounder]  Pareto optimal there is no strictly shorter sequence and Gemini comes now up here we see the reasoning traces here in much more detail exactly I define the output format so I can see immediately all the reasoning traces and here's proof of optimality there's no shorter the goal was to reach floor 50 in the elevator test beautiful it gives me more information more resources and it tells me it was a 10 action step. So, OpenAI 20
- `SgknC9B1dm8:00090` [claim+grounder]  steps, Gemini 10-step, the solution was the shortest path. So, you immediately see about the performance of the system. Great. So, but if I look now at o4 mini more in detail and I look here at the explanation, there's no strictly shorter sequence. Yes, everything is perfect. Yeah, let's start from the beginning. So 20 pushes is the solution. This is the sequence. And here is now the state of
- `SgknC9B1dm8:00120` [claim+grounder]  the system. And here we see exactly all the conditions for all the 20 step it performed. So I have a deeper insight even if o4 does not want to show me the reasoning traces. A little trick you can use too. The final result is yes. Here everything is okay. We never passed any random traps. Everything looks beautiful. Everything looks great. tells me to optimal any round claiming more ant resources master ether. Okay, therefore no
- `SgknC9B1dm8:00150` [claim+grounder]  strictly shorter sequence is possible. This 20 push plan sits on the Pareto frontier and you would believe it if you would not have seen that on the right hand side we have Gemini Pro and Gemini Pro does it in 10 steps. So never ever trust any system. So here's another optimal plan from Gemini 2.5 Pro. We have nine button presses and one special floor action with the emergency exit button pressed here. This is beautiful. This is great. And here
- `SgknC9B1dm8:00210` [claim]  optimality, can we have more code cards? What about more resources? And it argues beautifully. I think this is the best solution. And if you compare it here with o4 mini with 20, oh yes, definitely is. So I say, hey, validation run. Show me your final result. step-by-step explanation but try another perspective or try another method. Now we stay live because I want to show you this because now the systems here know exactly and they just have to
- `SgknC9B1dm8:00270` [grounder]  tell us hey 10 is the best result. Yes. So let's have a first look at o4 mini complete independent sanity check yet just a birectional search over the full state space. Beautiful. Yes. The frontier the backward frontier the meet in the middle. Okay. Yeah, complete different algorithm a birectional BFS and I can confirm tells us o4 pro says is the minimum the exact same 20-move
- `SgknC9B1dm8:00300` [grounder]  sequence arises. So o4-mini is perfect will be perfect has always been perfect gives me here a beautiful explanation because I asked for it. So always ask for explanation otherwise you do not get it. And now look at this and you would say what what is this? This is not a causal argumentation. It argues that it has a hidden model of world that is invented by o4 and it is

**verdict:** 
**notes:** Too much overlap between question and claim. Drop this question. 

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

## fc-0014
**question id:** fc-0014
**claim id:** 1IgPase-zjw#c039
**question:** How does continuous pre-training (CPT) alone compare to CPT combined with additional optimization methods in terms of cost, speed, and performance gain (e.g., moving accuracy from 80% to 86.7%)?
**claim:** The creator concludes that continuous pre-training alone provides the fastest, cheapest, and nearly optimal performance gain (80% to 86.7%), with only a 0.1 percentage point improvement from adding further optimization methods.
**claim source chunks:** 1IgPase-zjw:01020, 1IgPase-zjw:01050
**grounder chunks:** 1IgPase-zjw:00960, 1IgPase-zjw:00990, 1IgPase-zjw:01020

**union chunk text:**
- `1IgPase-zjw:00960` [grounder]  performance of 80%. Then we just add here this RPO. So we go from 80% to 83.8%. Great. But what if we just go here with the continuous pre-training? And you might say, wow, look at the continuous pre-training alone on the base model gives us a much better performance. So we see if we want to add knowledge for a general medical exam then CPT seems to be the right step
- `1IgPase-zjw:00990` [grounder]  to go because we had 86.7%. If we then add a DPO now this is really the classical DPO we just increase here from 86.7 to 86.88. So not really. And then if we do now the new RPO the preference optimization then you see it's identical. So for me now trying to understand is I see okay this is the
- `1IgPase-zjw:01020` [claim+grounder]  base model 80%. And what gives me for the simplest fastest improvement continuous pre-training I just add knowledge and I jump from 80% to 86.7%. Great. And the best thing I can achieve is 86.8%. So 0.1 percentage point I say okay given that I don't have to pay for this given I don't have to have the computer infrastructure for this given that it is faster I would say great so continuous
- `1IgPase-zjw:01050` [claim]  pre-training if you have a general exam this might be the way to go for the Japanese model here and then of course they decided hey let's go for other benchmark of course in Japanese so you can see here all the data and this is interesting Because somehow this is strange. Have a look at this. Take your time and then you will understand what I mean. And you know there's a simple explanation because if we look closer here at their performance test they they

**verdict:** 
**notes:** Too much overlap between the question and claim. Drop this question. 

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

## fc-0016
**question id:** fc-0016
**claim id:** DXjhPyoOXas#c039
**question:** What kind of new attention mechanism does GPDiT introduce to reduce computational cost?
**claim:** GPDiT introduces a new lightweight causal attention mechanism that is less computationally expensive.
**claim source chunks:** DXjhPyoOXas:01110, DXjhPyoOXas:01470
**grounder chunks:** DXjhPyoOXas:01110, DXjhPyoOXas:01470

**union chunk text:**
- `DXjhPyoOXas:01110` [claim+grounder]  making it autoregressive at a frame level and we operate here with our meta operations in a continuous latent frame. So this means we can even if you want optimize it further because now the computational infrastructure that you need here for video operations is not that simple. So whatever we can do make it simpler make it faster less memory. So we will have a new attention mechanism a lightweight causal attention mechanism that is quite good but less
- `DXjhPyoOXas:01470` [claim+grounder]  pixel distribution directly in our space. So you have an idea our latent space is a highdimensional space. The causal attention here, the simplified version here is that we say okay, we don't have to com to compute the complete complexity because we don't have this extra memory cost, but we go here with a precomputing of key value projection once and reusing them without further interaction amongst themselves for each new frame is the way to go. And

**verdict:** 
**notes:** I don't see GPDiT in the chunk texts. Drop this question.

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

## fc-0018
**question id:** fc-0018
**claim id:** imUnte-N0ec#c027
**question:** In a code evaluation setup where the one correct ('ground truth') code snippet was stripped down to plain text while all the incorrect candidate snippets kept their original well-documented, nicely formatted code and explanations, what did this asymmetric test reveal?
**claim:** The researchers conducted an asymmetric test where the single correct ('ground truth') code snippet was normalized (textually stripped) while incorrect code candidates retained their original, well-documented, pretty text and explanations.
**claim source chunks:** imUnte-N0ec:00600, imUnte-N0ec:00630
**grounder chunks:** imUnte-N0ec:00600, imUnte-N0ec:00630, imUnte-N0ec:00660, imUnte-N0ec:00690, imUnte-N0ec:00720, imUnte-N0ec:00750, imUnte-N0ec:00780

**union chunk text:**
- `imUnte-N0ec:00600` [claim+grounder]  I think this is a statement that you have really to enjoy and then they did a test here an asymmetric test and they say this is not possible this must be a mistake no it is so great we write code to build a web page every day everything for this simple task everything is working yeah and they said so let's do something an asymmetric test and for a given query they took here the one correct code snippet that was working that was
- `imUnte-N0ec:00630` [claim+grounder]  presenting the ground truth for the golden example and they normalized it and a lot of other code candidates that were not working that were incorrect candidates but they added original well documented pretty forms and explanation but remember the most important fact is nonworking code and then they said okay my little llm
- `imUnte-N0ec:00660` [grounder]  You are looking for new code. You don't know inherently how to solve this code example. Here you have a database full of code thousand GitHubs. Go and find retrieve here in a code RAG. Retrieve your code. And you know the result the retriever performance got even worse. You know why? Because it was not understanding the code that it needs. It was just looking at the textual description that was somewhere
- `imUnte-N0ec:00690` [grounder]  intermingled in the code. I think it's amazing now at the end of June 2025, we are understanding that the Code RAG are not working on code but on the text between the code. And here you have now their results in detail in a tabular form and they tell us the result demonstrate that when only the ground truth document is normalized. So here the S2 normalize the ground truth and the others incorrect stay the
- `imUnte-N0ec:00720` [grounder]  same. The ground truth documents rank the correct document rank deteriorates dramatically to 288 compared to when all documents are normalized. This is here the S1 case. So if you normalize everything the incorrect and the correct case okay it's real down. But if you normalize only the character, you leave the other here with the beautiful textual code and the in with
- `imUnte-N0ec:00750` [grounder]  the textual description of the code and the incorrect code example. Yeah, the average rank just crumbles down and you see this on multiple embedding model here OpenAI. So they checked it and this is a general behavior. And now Carnegie Mellon tells us you know we think this reveals a strong and a dangerous inductive bias of code AI because the model has learned one rule
- `imUnte-N0ec:00780` [grounder]  that well documented code is the good code and this is the code that I as an AI system will use for my user to answer the query. And when faced with a choice between the poorly documented correct code answer and a well documented incorrect code answer, it will overwhelmingly prefer the wrong one, the incorrect code sequence and it will learn the incorrect

**verdict:** 
**notes:** The claim did not answer the question. Drop this question. 

---

## fc-0019
**question id:** fc-0019
**claim id:** QWD55guu0So#c039
**question:** How does the Hierarchical Reasoning Model (HRM) use deep supervision, breaking training into segments with loss computed at multiple depths, to address long-horizon training instability?
**claim:** HRM solves the long-horizon training instability problem using a technique called deep supervision, which breaks the reasoning process into a series of smaller forward passes called segments, with loss calculated at multiple depths rather than only at the end.
**claim source chunks:** QWD55guu0So:00840, QWD55guu0So:00870
**grounder chunks:** QWD55guu0So:00810, QWD55guu0So:00840, QWD55guu0So:00870, QWD55guu0So:00900, QWD55guu0So:00930

**union chunk text:**
- `QWD55guu0So:00810` [grounder]  transformer block that has a graph that contains a cycle. So you see, they don't get up here in the technical terms because it is not implementing an RNN architecture but a transformer architecture I need another moment of your attention another trick that you have to understand adaptive computation time ACT now the challenge is training now here a
- `QWD55guu0So:00840` [claim+grounder]  recurrent model for some long reasoning traces not this simple one but really the long monster reasoning traces. No, and if you only provide now the loss at the very end after hundred of steps, you know the gradients have a very long and difficult path to travel backward in the back propagation making the learning absolutely inefficient and unstable and we know it's not working. So is there another trick or methodology that you can apply and the solution here is this? Yes, of course. We call it deep supervision.
- `QWD55guu0So:00870` [claim+grounder]  So instead of one single massive forward pass, this new method breaks the reasoning process into a series of smaller forward passes which the paper here the authors call segments. Have we heard this before? Well, yes, of course. And it is called deep because as deep supervision and the supervision is nothing else than a loss calculation method is applied at multiple depths of the computational process and not just at the very end. So
- `QWD55guu0So:00900` [grounder]  you understand simple no this results more or less since we benefit we have a frequent feedback. So if you think about it's a teacher in a classroom teacher checking in every 5 minutes instead of only checking at the end of a 2 hour exam. It makes learning much more stable and much more efficient for each student. Regularization. This is kind of a natural regularizer improving here the generalization and it is the foundation for ACT.
- `QWD55guu0So:00930` [grounder]  So let's have a look at ACT adaptive computation time. Now that the reasoning process is broken into discrete segments as I just showed you. Now the model needs only to know hey when should I stop? Should I run for one segment, eight segments? When is the right time to say this is it, this is the right result. And this is now where ACT comes in. Yeah, it is like a second hat here on our transformer on the model that acts

**verdict:** 
**notes:** Leakage between question and claim. Drop this question.

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

## fc-0022
**question id:** fc-0022
**claim id:** IFCAlGrmxq4#c003
**question:** What scores were reported for Opus 4.1 16k thinking versus Sonnet 4.5 on a benchmark comparison cited by the creator?
**claim:** According to stats cited by the creator, Opus 4.1 16k thinking scores 62% while Sonnet 4.5 scores 69% on a benchmark.
**claim source chunks:** IFCAlGrmxq4:00030
**grounder chunks:** IFCAlGrmxq4:00030

**union chunk text:**
- `IFCAlGrmxq4:00030` [claim+grounder]  On this particular very particular test and I thought hey this is amazing but what about the difference to 100%. Does it mean it fails and the rest? Well, I said unbelievable. Let's have a look at original. And here Anthropic tells us, hey, Sonnet 4.5 here, domain specific knowledge and reasoning is now so much better. And I have a look here at stats. And I see, oh yeah, Opus 4.1 16k thinking 62%. And now imagine we have 69%.

**verdict:** 
**notes:** The 'benchmark comparison cited by the creator' is non-specific ; not a natural question that a real user would ask.  

---

## fc-0023
**question id:** fc-0023
**claim id:** 5LUIZAZWoBU#c022
**question:** In the GeARs architecture, what happens during the 'triple link' step where each proximal triple is used as a search query against a large external knowledge graph like Wikidata?
**claim:** GeARs has a 'triple link' step where each proximal triple is used as a search query to find the most similar canonical triple in a massive external knowledge graph such as Wikidata, representing an online knowledge synchronization step.
**claim source chunks:** 5LUIZAZWoBU:00450, 5LUIZAZWoBU:00480, 5LUIZAZWoBU:00510
**grounder chunks:** 5LUIZAZWoBU:00480, 5LUIZAZWoBU:00510, 5LUIZAZWoBU:00540, 5LUIZAZWoBU:00570, 5LUIZAZWoBU:00600

**union chunk text:**
- `5LUIZAZWoBU:00450` [claim]  of the reader of an LLM. Couldn't be easier. A small set of temporary informal triplets. You know this structure subject predicate object extracted direct here from the text passages here of my small domain specific corpus. That's it. First part done. Now we come to two elements. This they call triple link and graph expansions that are rather interesting. So yeah we are here in the sync KG part is where the system bridges here the gap between the text world this and the
- `5LUIZAZWoBU:00480` [claim+grounder]  graph world and our triple link is now interesting. So we have both no we have the approximate triples and this arrow here if you want represents the online knowledge synchronization step. So this is now interesting. So what you need? You need now a link to the monster huge planetary size database that has the real knowledge of everything. Let's call it Wikipedia or Wikidata.
- `5LUIZAZWoBU:00510` [claim+grounder]  This online knowledge synchronization is the main trick if you want. So each proximal triple T dash here is used here as a search query to find now the most similar canonical triple T the original triple T in the massive external knowledge graph of Wikidata T triples is here the result of the triple link this is a set of canonical triples from the Wikidata wiki data that are now linked to our query so what we
- `5LUIZAZWoBU:00540` [grounder]  found we found the entry points into the global graph And then comes now the interesting element of the graph expansion. It is rather easy if you got here the main idea of this. So starting now from the canonical triples T the system performs a search within the Wikipedia or Wikidata graph to find new multi-hop reasoning paths. You know this we talked about this already in my last videos and you can have different search algorithm and here in the paper they go with a
- `5LUIZAZWoBU:00570` [grounder]  classical diverse triple beam search algorithm. So this means you don't find just one path on the hypersurface of your knowledge graph but you explore in parallel multiple promising paths simultaneously to gather here a wider range of evidence. Great. This is it. So what you do have now additional information. So the new triplets now discovered now during the graph expansion are simply guess what
- `5LUIZAZWoBU:00600` [grounder]  used to require the original document corpus C. So this is your one of the crucial step you know the system understood that there's it learned now additional domain specific information and the system uses what it learned from exploring here the graph the wiki data graph to find now new documents that the initial base retrieval might have missed. So we are operating here in a beautiful loop. Now comes the next simple step. This is

**verdict:** 
**notes:** Too much leakage between question and claim. Drop the question.

---

## fc-0024
**question id:** fc-0024
**claim id:** HcZ2QKgFWPI#c054
**question:** How does LSD-3D compare to methods like Gaussian splatting scenes (3C) and MagicDrive 3D when generating novel driving trajectories?
**claim:** LSD-3D was compared to competing methods including Gaussian splatting scenes 3C and MagicDrive 3D, and outperformed them, as those methods struggle with generating consistent, 3D-plausible scenes for novel driving trajectories.
**claim source chunks:** HcZ2QKgFWPI:01650
**grounder chunks:** HcZ2QKgFWPI:01650

**union chunk text:**
- `HcZ2QKgFWPI:01650` [claim+grounder]  If you compare this now just to show you that it's really working there's a lot of additional data in the paper. Please have a look at the original paper as published by Princeton University and MSP. They compared now to competitive to other methods. No gaussian splatting scenes 3C MagicDrive 3D. I'm not familiar with this but if you compare this I can show you how it looks like. So here you have everything compared to two competitive products which also generate driving videos but they struggle with generating

**verdict:** 
**notes:** Too much leakage between question and claim. And I'm not sure that the claim is fully supported by the chunk text. 

---

## fc-0025
**question id:** fc-0025
**claim id:** FtrLaHeEP4E#c037
**question:** Was Qwen3 235B, running at maximum non-thinking effort, able to reliably solve the causal reasoning puzzle, and is a comparison planned once the thinking variant of the new Qwen3 is available?
**claim:** The creator concludes that even at maximum non-thinking effort, Qwen3 235B could not reliably solve the causal reasoning puzzle, and states they will need to wait for the thinking variant of the new Qwen3 to do a proper comparative evaluation.
**claim source chunks:** FtrLaHeEP4E:01050, FtrLaHeEP4E:01080
**grounder chunks:** FtrLaHeEP4E:00690, FtrLaHeEP4E:00840, FtrLaHeEP4E:00900, FtrLaHeEP4E:01050

**union chunk text:**
- `FtrLaHeEP4E:00690` [grounder]  run 17 presses. Okay. Step by step state table as requested in my instruction. Okay. Yes. Yeah. It was not to be expected that the non-thinking model is able to solve for you a logic causal reasoning puzzle at all. Absolutely. But I think it found some interesting subtargets. So it had
- `FtrLaHeEP4E:00840` [grounder]  15 minimum presses to achieve goals. But we need 17. I provide a core and verified solution. Oh, but instead I include now note this is a known hard puzzle. The above presents the best human verifiable solution within the constraint. So it tells me I found a solution with 17 presses. I have the energy. Okay, I
- `FtrLaHeEP4E:00900` [grounder]  complete correct and verified optimal run on 17 presses chosen sequence 16 button presses truly verified optimal run 18 presses Okay. Okay. It's It's still trying to find a better solution. The blue code. Okay. Here we go with the blue code. It's waiting. It's thinking. Okay.
- `FtrLaHeEP4E:01050` [claim+grounder]  given time I provide this as the best effort. The puzzle is unsolved due to EPC to energy package constraints but the closest is 18 presses recode nearly optimal. Okay. Okay. So you see also syncing at the maximum also this is a non-syncing model. I guess we simply have to wait for the sinking model of the new Q3. Hope it comes out in the
- `FtrLaHeEP4E:01080` [claim]  next day and we will have another evaluation run so you can compare it to the other models. Okay, community, we have here the Kim K2. So, Ala Marina, beautiful. So I just put in here my test identical test here that I've shown you already several times. Give me K2. Here it is. No. Wow. Non-syncing. I solved this step by step.

**verdict:** 
**notes:** 'the causal reasoning puzzle' is too non-specific. 

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

## fc-0027
**question id:** fc-0027
**claim id:** bkL65H8awqM#c050
**question:** What is the 'Duncan experiment' thought experiment about testing whether an LLM's world model can predict the deflection angle of water hitting a newly invented object with novel angles it has never seen described in pretraining data?
**claim:** The creator poses a thought experiment (the 'Duncan experiment') involving a newly created object with a novel multitude of angles never described before, asking whether the LLM's world model would fail to predict the deflection angle of water hitting it since it lacks physical formulas and cannot deduce this from pretraining data.
**claim source chunks:** bkL65H8awqM:01440, bkL65H8awqM:01470
**grounder chunks:** bkL65H8awqM:01440, bkL65H8awqM:01470, bkL65H8awqM:01500

**union chunk text:**
- `bkL65H8awqM:01440` [claim+grounder]  hey if it would have emergence the system then when the water falls to the floor in this moment when you know the water splashes out of the glass it could accidentally hit another surface at a particular angle on its way down I place their new object and the linguistic trained LLM would not be able to calculate since it's missing the physical formula of the real world deflection angle given that a specific condition of the object
- `bkL65H8awqM:01470` [claim+grounder]  that the water hits. It can also not deduce this result from any pre-training body of knowledge because I just created this new object here in my Duncan experiment in the path of the water falling down by gravity and this object has a multitude of angles never described before in any combinatorial configuration. So when the LLM fails and the world model fails because it has never been described to the LLM, what happens in this case? So I try to counteract the the argumentation by the
- `bkL65H8awqM:01500` [grounder]  AI and the AI comes back and says a brilliant and perfectly articulated challenge. You have pinpointed the exact frontier where the nature of the LLM's world model becomes most clear. The LLM fails and the world model fails. Yeah. But how it succeeds by not calculating this. And now this is interesting because it tells me now the level of understanding of the LLM world model operates on an intuitive physics engine

**verdict:** 
**notes:** Too much overlap between question and claim. Plus, the Duncan experiment is specific to the creator. 

---

## fc-0028
**question id:** fc-0028
**claim id:** 2unOi2JTZ0I#c039
**question:** In a paper's worked example on agent matchmaking with a pool of 100 agents, cosine similarity is used to match agent self-descriptions to subtasks - which agent was identified as the best fit for subtask one, and what was its similarity score?
**claim:** In the paper's example, with a pool of 100 agents, cosine similarity scores are computed between agent self-descriptions and subtasks, and agent D scored 0.73 for subtask one, making it the best-fitting agent for that subtask.
**claim source chunks:** 2unOi2JTZ0I:00930, 2unOi2JTZ0I:00960
**grounder chunks:** 2unOi2JTZ0I:00930, 2unOi2JTZ0I:00960

**union chunk text:**
- `2unOi2JTZ0I:00930` [claim+grounder]  has a complex task for the system. The orchestrator looks at this and says my goodness what I'm going to do with this says okay I have to decompose the complexity into subtask 125 run check. suggest improvement, extract the code, write doc string and whatever do and then you find here the embeddings and then you have here let's say you have 100 agents then you say okay based on the embeddings now let's have a look let's have here now let's say a cosine similarity no which of the agent has
- `2unOi2JTZ0I:00960` [claim+grounder]  here a good fit from the description or the self description of the agent and you see here D agent D has 0.73 so Guess what? For subtask one, the first idea is use agent D because the other are not really fitting here in their self-description task for this specific subtask one. Got it? No problem. using similarity, the cost, the latency requirement, the policy constraint, the security and whatever it assigns here

**verdict:** 
**notes:** Too specific question ; the question is not likely to be asked by a real user.

---

## fc-0029
**question id:** fc-0029
**claim id:** aobihG5ig28#c015
**question:** What mistake did Grok 4 make in an elevator puzzle involving a 50-floor building, where it moved the elevator to floor 52 and then capped it at floor 50?
**claim:** Grok 4 made a major mistake by moving the elevator to floor 52 in a 50-floor building and then capping it to floor 50, treating this cap as a valid assumption.
**claim source chunks:** aobihG5ig28:00360, aobihG5ig28:00390
**grounder chunks:** aobihG5ig28:00360, aobihG5ig28:00390

**union chunk text:**
- `aobihG5ig28:00360` [claim+grounder]  Now this is now a major mistake. Minor error in the original. I said floor 48 even. Correct. But 42 cap to 50 is an assumption. If no cap, this move is invalid because it moved the elevator to floor 52. But assuming cap for validity. Oh wow. So it comes up with its own rule and interpretation that says, yeah, it's
- `aobihG5ig28:00390` [claim+grounder]  okay. If I have a 50 floor building, I go with the elevator to floor 52 and then I cap it to floor 50. And the search for a shorter path just go here to the end result is no shorter path exist. Okay. So the cap is not what I can accept. This is an illegal move. So easy I say hey if you cap floor 52 to floor 50 this is an illegal move. You have to land on floor 50 precisely. Please

**verdict:** 
**notes:** Too much overlap between question and claim.

---

## fc-0030
**question id:** fc-0030
**claim id:** VMsJ4me5Q3o#c052
**question:** Why does feedback quality matter so much in textual gradient methods, and why would using a small LLM such as a 1.5 billion parameter model likely cause unstable updates?
**claim:** The creator warns that feedback quality matters greatly because the textual gradient depends on LLM diagnostics, and using a small model (e.g., 1.5 billion trainable parameters) would likely cause unstable updates.
**claim source chunks:** VMsJ4me5Q3o:01050
**grounder chunks:** VMsJ4me5Q3o:01050, VMsJ4me5Q3o:01140

**union chunk text:**
- `VMsJ4me5Q3o:01050` [claim+grounder]  in the performance. But you don't only gain performance but it is a much more complicated system. So careful you have you have induced complexity and you have to be careful and let me point out some of those topics you have to be really careful about the feedback quality matters. The textual gradient depend on the LLM diagnostics. If you go with a little tiny LLM with 1.5 billion free trainable parameter, this is not really what you
- `VMsJ4me5Q3o:01140` [grounder]  that are highly reasonable that are highly domain specific that are highly precise that you can trust nothing has happened no hallucination nothing it is the perfect system otherwise given the highly dense interconnections you can have cascading errors and since we are working here not on a smooth mathematical differentiable manifold we are talking here about textual gradient descent that depend here on the LLM And on the knowledge graph optimality you understand. Oh wow. We are in for a

**verdict:** 
**notes:** Too much overlap between question and claim.

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

## fc-0034
**question id:** fc-0034
**claim id:** gNV2rDH7d4E#c040
**question:** Why do trained models place opposing concepts, like multiplication and addition, on opposite sides of a hyperplane in high-dimensional space?
**claim:** The creator explains that a trained model organizes information efficiently by placing opposing concepts (like multiplication and addition) on opposite sides of a hyperplane (a flat dividing line/plane in high-dimensional space).
**claim source chunks:** gNV2rDH7d4E:01020
**grounder chunks:** gNV2rDH7d4E:01020, gNV2rDH7d4E:01050

**union chunk text:**
- `gNV2rDH7d4E:01020` [claim+grounder]  to geometric memory configuration. So, this means means when a model is trained it learns to organize the information efficiently and the easiest way to store it, to opposing concepts even simple as multiplication or addition, is to put them in opposite sides of a simple flat dividing line and let's call this a hyperplane. And the linear probe's AI machine's only job is to find here the angle, that is the dividing line between those.
- `gNV2rDH7d4E:01050` [grounder]  And once it finds it for a math problem in general of this complexity on this domain with this LLM, it can then apply it to any new math problem of the same complexity because the new problem activation patterns will also fall on one side of that line or on the other side. So, we do achieve now kind of a new generalization plus and now hold on to your socks, to the emergent geometric pattern.

**verdict:** 
**notes:** Too much overlap between question and claim.

---

## fc-0035
**question id:** fc-0035
**claim id:** W_aqotP134s#c025
**question:** On average across the benchmarks tested, how much did SRL improve performance compared to classical reinforcement learning?
**claim:** On average across the chosen benchmarks, performance increased from 24.5% with classical reinforcement learning to 27.6% with SRL.
**claim source chunks:** W_aqotP134s:00870, W_aqotP134s:00900
**grounder chunks:** W_aqotP134s:00870

**union chunk text:**
- `W_aqotP134s:00870` [claim+grounder]  one 47 it increases here to 50 with supervised reinforcement learning. But in general, you go here for a particular choice of benchmarks that were cleverly chosen by Google. So on average, you go from 24.5% to 27.6% performance. So the increase is is there. It is noticeable. Let's put it in this way. Yeah, it is notable. So yeah, just be aware this is let's call it a best case scenario if you do
- `W_aqotP134s:00900` [claim]  this. Now you might ask why. And at the end of the video, I will give you several ideas why we what steps to take to further improve this because we want to get better than Google. Yeah, as I told you that was this particular step of the filtering process of the quality assurance. Now look, let's have a look here to numerical data. Again, we have here the training with the reinforcement learning and you see with the classical reinforcement learning very valuable feedback, we have 24.5%.

**verdict:** 
**notes:** 'the benchmarks tested' is too non-specific.

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

## fc-0037
**question id:** fc-0037
**claim id:** cHHy8XXPtuk#c041
**question:** Why might a t-SNE plot showing a supposed continuous manifold be misleading when the original data lives in roughly 896-dimensional space?
**claim:** The creator expresses skepticism about the t-SNE visualization, stating that what he sees looks like a mixed jumble of colors rather than a clear geometric separation, and questions whether it truly demonstrates a continuous manifold given that the visualization compresses an ~896-dimensional space down to two dimensions.
**claim source chunks:** cHHy8XXPtuk:01410, cHHy8XXPtuk:01440, cHHy8XXPtuk:01470, cHHy8XXPtuk:01500
**grounder chunks:** cHHy8XXPtuk:01350, cHHy8XXPtuk:01380, cHHy8XXPtuk:01410, cHHy8XXPtuk:01440, cHHy8XXPtuk:01470

**union chunk text:**
- `cHHy8XXPtuk:01350` [grounder]  anything at all. This is the beauty and this is why we built orthogonal spaces and why we built on a pre-training here the complexity that we wanted that is able to handle this talking about smooth manifold. Is it really a smooth manifold? Now they show us here this image and I'm a little bit I don't know let's have a look. So this is the geometric separation of the personality manifolds and here we have a
- `cHHy8XXPtuk:01380` [grounder]  simple t-SNE uh projection of 1,000 character embeddings that are already within the geometric space of the um model and we don't have to do any specific training for them and the points are colored here by a particular score the openness score. Beautiful. Now you see the clear gradient separation confirms that our auto encoder has successfully mapped discrete soological traits into a continuous geometric manifold.
- `cHHy8XXPtuk:01410` [claim+grounder]  So if I look now at this and maybe I'm simply not intelligent enough for this. Okay. So what do I see? I see what simply is a mixture. No, a mixture you see representing that should represent here a continuous manifold. So I have here the light red, orange, yellow, blue, dark blue. I have it here beautifully mixed. I don't have here only a red bunch and a and a dark red cluster and a
- `cHHy8XXPtuk:01440` [claim+grounder]  light red cluster. Everything is here continuous manifold and everything could look like a smooth manifold. But remember this is here uh like you shine with a flashlight on top of a 896 dimensional hypershape and at the bottom you just look at the shadows here and those are the shadows you see from a complexity that has almost 900 dimensions and now this is squeezed onto the ground where we have
- `cHHy8XXPtuk:01470` [claim+grounder]  just two dimensions to say now that we have a continuous manifold because I see this particular pattern with a t-SNE projection on a two-dimensional manifold, a flat manifold is is an interpretation I would say maybe, but yeah, I'm not really convinced here that we have a clear geometric separation of the personality manifolds. Okay, so there I would say I put
- `cHHy8XXPtuk:01500` [claim]  personally a question mark. If you find a better explanation or if you find something that tells us here that this is really a continuous manifold, please share your ideas here in the comments. Why do we have to separate them from reasoning? I showed you at the very beginning here. You're a genius at 10, a raw genius, and then you just go up here one other direction here and you see you got another feature. Now you're styled

**verdict:** 
**notes:** The claim does not really answer the question.

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

## fc-0039
**question id:** fc-0039
**claim id:** 1nd2oAt2rEU#c029
**question:** According to Nvidia's research on injecting reasoning data during pre-training, why can't supervised fine-tuning combined with reinforcement learning fully recover the performance gains achieved by that approach?
**claim:** The Nvidia paper found that injecting reasoning data during pre-training gives the highest gains, and supervised fine-tuning alone cannot fully recover this benefit even when combined with reinforcement learning, yielding about a 20% performance improvement.
**claim source chunks:** 1nd2oAt2rEU:00660, 1nd2oAt2rEU:00690
**grounder chunks:** 1nd2oAt2rEU:00660, 1nd2oAt2rEU:00690, 1nd2oAt2rEU:00720

**union chunk text:**
- `1nd2oAt2rEU:00660` [claim+grounder]  and the solution is easy it only works in the pre-training. Great let's have a look at this they did a huge experiment measure when pre-training versus supervised fine tuning and what type diversity quality and scale of reasoning data should be injected under what data to what amount how to optimize here the reasoning after reinforcement learning front loading matters. This is the result if you want injecting the reasoning data during the pre-training gives you here the highest gains that
- `1nd2oAt2rEU:00690` [claim+grounder]  even if you have then a supervised fine tuning and reinforcement learning the supervised fine tuning alone cannot fully recover. You have about plus 20% better. So therefore you have to import or already have the pre-training complexity of your pre-training data that you have to do in the pre-training otherwise you cannot have to simply inject it in the supervised fine tuning phase. You have an asymmetric allocation principle. Yes of course high quality pre-training can also be latent. So you
- `1nd2oAt2rEU:00720` [grounder]  maybe see just a small immediate effect if you only go with the pre-trained model. But the moment you do a little bit of a supervised fine-tuning in the domain of the pre-training in the complexity level of the pre-training suddenly you unlock all the gains here and your supervised finetuning performance will make a big jump forward upwards. Great. So high quality pre-training can be latent. And if you think you just invest in

**verdict:** 
**notes:** The claim is not answering the question.

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

## fc-0041
**question id:** fc-0041
**claim id:** KV-uZzE78qA#c036
**question:** At five reasoning hops, how do GPT-5.2's accuracy and a locally trained 14B-parameter model's accuracy compare?
**claim:** At five reasoning hops, GPT-5.2 achieves about 70% accuracy while the local 14B trainable parameter model reaches about 90% accuracy, a 20 percentage point difference.
**claim source chunks:** KV-uZzE78qA:00960, KV-uZzE78qA:00990
**grounder chunks:** KV-uZzE78qA:00930, KV-uZzE78qA:00960, KV-uZzE78qA:00990

**union chunk text:**
- `KV-uZzE78qA:00930` [grounder]  what if we take here GPT 5.2 and let's do this here in comparison to a 14B that I can run maybe locally on my computer. Here we have on the y-axis the accuracy and here on the x-axis we have the number of the reasoning hops. You know we train only for three then we just let's have out of distribution and we hope that they will improve the reasoning capabilities and if you pay here for the
- `KV-uZzE78qA:00960` [claim+grounder]  most expensive GPT 5.2 too. You see in the step from four to five in the reasoning hops, you see that you have a massive degradation here of the reasoning capability of the accuracy of your beloved GPT 5.2. It simply fails to perform. But look at the other side. Look at the bright side. What is so beautiful? Look at this. We have a local 14 billion free
- `KV-uZzE78qA:00990` [claim+grounder]  trainable parameter model that is so much better. Look, the GPT 5.2 is an accuracy of 70%. And with our maybe local model, we can reach 90%. 20 percentage point is gorgeous. And this is simply done here on a 14B model. So you see, we do not need more data center. We do not need more scaling. We

**verdict:** 
**notes:** Accuracy on what? Drop this question.

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

## fc-0046
**question id:** fc-0046
**claim id:** 5moW9ag8OPk#c020
**question:** Why does converting human similarity-based thinking (dot products of dense vectors) into explicit logical structures like DAGs and trees, with defined state transitions and causality, lose some of the complexity and beauty of human language?
**claim:** The creator argues that humans think in similarities (measured as a dot product of dense vectors), while logical reasoning requires explicit state transitions, causality, and structures like directed acyclic graphs (DAGs) and trees, and that converting similarity-based thinking into explicit state transitions loses complexity and beauty of human language.
**claim source chunks:** 5moW9ag8OPk:00660, 5moW9ag8OPk:00690, 5moW9ag8OPk:00720
**grounder chunks:** 5moW9ag8OPk:00660, 5moW9ag8OPk:00690, 5moW9ag8OPk:00960, 5moW9ag8OPk:00990, 5moW9ag8OPk:01590, 5moW9ag8OPk:01620, 5moW9ag8OPk:01710

**union chunk text:**
- `5moW9ag8OPk:00660` [claim+grounder]  we try to throw on AI to somehow make it reason you might ask why should it reason well it's about decision and decision lead to action and action lead here to strategy frameworks and strate Strategy frameworks lead to policy. Now we assume and we think in similarities. No, this is for any measured here a dotproduct here of a dense vector in a particular mathematical field. No, logical
- `5moW9ag8OPk:00690` [claim+grounder]  reasoning requires no explicit state transition. If you think about partially observable model of decision processes in mathematics, mutual exclusivity and causality and the causality we have as you've seen in my last video in AI research with directed basically graph our dag system and the tree structure that we have now so you see humans think in similarities and we convert this into a dot product into explicit state transition and
- `5moW9ag8OPk:00720` [claim]  somehow we lose a little bit of the complexity. enough of the beauty of human language. Now the first two studies that I showed you here in the first second of this video I call it graphing the mind to build graph out of something that is just here a beautiful idea but we have to take it we have to put it into our data center and we have to morph it trying to put it in our data center so we have to build graphs out of it
- `5moW9ag8OPk:00960` [grounder]  mathematical way a neural architecture that explicitly wires these hierarchies together back together. Now in a simpler way in the subconcept way allowing here maybe even humans to intervene at precise logical depths but we lose something. If you look here at the mathematical algorithms you see if you crack open here a high-level concept that we humans have in our mind if we have experienced it from so many different perspectives. You know I can reframe
- `5moW9ag8OPk:00990` [grounder]  here these studies four or five different times and you will always discover newer elements. If we break it down into one mathematical hierarchy. Yeah. And then we have only one mathematical method to solve it. So you see we lose we lose massive information. We use massive other paths of deciding of arguing of communicating. The density of our communication between AI agent is not
- `5moW9ag8OPk:01590` [grounder]  information, so much context. If we do this simplification, if we do this breakdown into subcategories, subclassifications just to handle it mathematically and therefore be able to code it. This is not the way forward. And you might ask, hey, what is lost when we force the human language into a purely computable hierarchy? I think human reasoning is powerful because it is associative and any
- `5moW9ag8OPk:01620` [grounder]  breakthrough in science. Go and read any book about physics for example. It rarely happens with strict pseudocode for step in plan. No, it happened because some unexpected associative leaps happened across unrelated domains. You have heard this. No, I was standing in the shower and suddenly had a beautiful idea about this is exactly what I'm talking about. You cannot logically deduce here creativity. It just happens
- `5moW9ag8OPk:01710` [grounder]  the tangles. If you want dynamic nature of the human understanding, yeah, it just fails to get all the nuances that we have and by forcing LLMs and this is the third paper in the code into the code primitives like in the mathematical primitives no we risk returning to the brittleness of a pure symbolic eye of the 1990s. So what is the final word? what is what

**verdict:** 
**notes:** The question is basically the claim. Drop this question.

---

## fc-0047
**question id:** fc-0047
**claim id:** OGT3NoFo-qg#c050
**question:** On a cost-per-query versus benchmark-score chart, how does KARL's pricing compare to models like GPT 5.2, Opus 4.5, and Opus 4.6, given that it reportedly matches Opus 4.6's performance?
**claim:** The creator claims KARL is one of the cheapest models on a cost-per-query vs. benchmark-score performance chart, outperforming other models like GPT 5.2, Opus 4.5, and Opus 4.6 on price while matching Opus 4.6's performance.
**claim source chunks:** OGT3NoFo-qg:01141, OGT3NoFo-qg:01171
**grounder chunks:** OGT3NoFo-qg:01141, OGT3NoFo-qg:01171

**union chunk text:**
- `OGT3NoFo-qg:01141` [claim+grounder]  everything else. Look at this. This is here the performance chart. Here we have the cost per query and here we have the benchmark score and you see Karl here is one of the cheapest model outperforming every other model on price. Here you have GPT 5.2, Opus 4.5, Opus 4.6 and Karl is just cheaper and better and at least the same performance like an Opus 4.6. And if you
- `OGT3NoFo-qg:01171` [claim+grounder]  look at the latency here in the second chart here where in the X-axis we have the latency plus the performance you see the lowest latency with Claude and again up to the best performance. So you have low latency, low cost, identical OPUS 4.6 performance. This is nice. This is nice for Databricks to have this model. How they did this? Not only do they have

**verdict:** 
**notes:** Too much overlap between question and claim.

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

## fc-0049
**question id:** fc-0049
**claim id:** VdPwMYHVOWE#c042
**question:** When the seed workflow was tested on a set of 100 problems, what results came back in terms of accuracy, token cost, and time taken, and where did it struggle?
**claim:** The seed workflow got 60 out of 100 problems right, cost $2 in tokens, took 45 seconds, and completely failed on complex mathematical operations.
**claim source chunks:** VdPwMYHVOWE:00900
**grounder chunks:** VdPwMYHVOWE:00870, VdPwMYHVOWE:00900

**union chunk text:**
- `VdPwMYHVOWE:00870` [grounder]  format, and solve those mathematical equations, huh? So, meta agent doesn't try to be clever yet. It creates here a seed workflow consisting exactly of one LLM node, and the task is read the text and output here an answer. Now, the system now takes this one node workflow, runs it on a validation set, let's say 100 mathematical problems that are of the same complexity and of the same mathematical depth like here the mathematical equation in my text, careful.
- `VdPwMYHVOWE:00900` [claim+grounder]  And then it collects the data, hm? It says, "Out of these 100 problems I given here in the validation set, it got 60 right, cost $2 in tokens, 45 seconds, but it completely failed on complex mathematical operations. Of course, we have an LLM node, not a code LLM. So, step three is now says, "Okay, the meta agent is looking here at the execution logs, token cost, latency, and the errors, and it says, "Okay, the LLM node keeps hallucinating some

**verdict:** 
**notes:** The 'seed workflow' is non-specific. Drop this question.

---

## fc-0050
**question id:** fc-0050
**claim id:** g1L8uOQ7Ids#c035
**question:** In a parallel multi-agent setup, what two conditions determine whether the approach fails versus whether success then hinges on Kimi K2.5's ability to summarize sub-results into a coherent final answer?
**claim:** The creator states that if a job cannot be separated, the parallel multi-agent approach will fail, and if it can be separated, the final result depends on Kimi K2.5's summarization capability to produce a coherent answer.
**claim source chunks:** g1L8uOQ7Ids:00721, g1L8uOQ7Ids:00751
**grounder chunks:** g1L8uOQ7Ids:00721, g1L8uOQ7Ids:00751

**union chunk text:**
- `g1L8uOQ7Ids:00721` [claim+grounder]  reasoning capabilities. We just added here the visual reasoning. And as a marketing gimmick here, you can now have 100 agents spun up here from the model itself. So this means either you ask the model here in a sequence for 100 complexities or you can pay up and you ask here the model to make 100 copies of itself and have a parallel execution if the job is absolutely separable. If not
- `g1L8uOQ7Ids:00751` [claim+grounder]  the thing will fail. If you can absolutely separate it then you get independent reports back and then it will depend here on the summarization capability of Kimi K 2.5 to find here a coherent answer first test indicate well needs a bit of improvement for Qwen 3 Max Thinking now from my side here if you think about the scientific reasoning about the complex reasoning

**verdict:** 
**notes:** This question is just weird.

---
