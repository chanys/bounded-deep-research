# Task 7 review - comparative (claim slice)

grounded 27/40 (13 dropped as unanswerable); handoff carries all 40 candidates with per-side support + inline both-side text.
clean 1 | flagged 28 | excluded 11 (failure status)
PASS both-side-grounded (strongly verified comparisons): 5; the rest need the missing side verified by eye at the sitting (evidence is in the inline pre-attached chunks).
non-both-side PASS candidates by pair-family: topic:benchmark methodology=1, topic:benchmark scores=2, topic:chain of thought=2, topic:deep research=1, topic:elevator/causal-reasoning-test=1, topic:evaluation methodology=1, topic:fine tuning=2, topic:grpo=2, topic:in context learning=2, topic:loss function=1, topic:mixture of experts=2, topic:model release=1, topic:prior video reference=2, topic:supervised fine tuning=1, topic:terminology=1, topic:training methodology=1, topic:world=1

---
## CLEAN (pass, both sides grounded, no other flags)

### cc-0020 | -hFJe5hXWps#c012+HcZ2QKgFWPI#c006 | q:fa3489b4
**Q:** In the Xiaomi research setup versus Dream to Chat's dialogue system, what is each one's 'world model' component actually built to handle or predict?
source videos: -hFJe5hXWps (2026-03-08); HcZ2QKgFWPI (2025-08-29)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:world
**side A** `-hFJe5hXWps#c012`  support=YES  subject_in_gold=full
  gold claim: In that Xiaomi research, two dynamic adapters were used: one adapter for geometry and one adapter for the world model handling physics.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `-hFJe5hXWps:00151`  was new self-driving AI explained here a vision language action model on the Plus integrating a world model here for Xiaomi electric vehicles. They used in their latest research here as I told you two dynamic adapters. One adapter was here for the geometry and one adapter was for the world model for the physics. And now for the geometry adapter. And you remember they also used here V GGGD but this changes today because now we
**side B** `HcZ2QKgFWPI#c006`  support=YES  subject_in_gold=full
  gold claim: Dream to Chat constructs a dialogue world model that predicts user emotion, sentiment, and intention, such as a request to be driven to a meeting with a client.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `HcZ2QKgFWPI:00060`  Beihang University and they have a dream to chat. They say we will use a model based reinforcement learning on dialogues with a user belief modeling and you might say what are you talking about? You mean I'm talking to my car? Yeah, they are now exploring ways how you have a conversation with your car and how the car should respond to you. And you know how they do this? They construct a dialogue world model that we already talked about which could predict
  - [unverified] `HcZ2QKgFWPI:00090`  everything from the user emotion from the sentiment the intention of a user when the users hey bring me to my next meeting with my client XYZ and they define here a partially observable Markov decision process and they say this is the essence that we can do this and you might say hey what a coincidence because this was part of one of my last videos. So what they have they have a new principled approach to uncertainty. You don't know how what a user wants. If a

---
## FLAGGED (pass; per-side annotation - verify the unverified side by eye)

### cc-0002 | -0xKV2i6M4U#c004+-JiUyJVPM3Q#c013 | q:941c08fc
**Q:** On the elevator puzzle task, how did Claude Opus 4.6 (non-thinking mode)'s approach to working through it compare to how Gemini Flash Thinking tackled the same setup when code execution was enabled?
source videos: -0xKV2i6M4U (2026-02-05); -JiUyJVPM3Q (2025-03-11)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=none/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=claim_b
pair_key: topic:elevator/causal-reasoning-test
**side A** `-0xKV2i6M4U#c004`  support=NO  subject_in_gold=none
  gold claim: Claude Opus 4.6 non-thinking exhibited trial-and-error behavior and clean restarts during the elevator puzzle, which the creator says is expected for a non-reasoning model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-0xKV2i6M4U:00030`  elevator test. It is only going deep inside. Oh, revise the deterministic path. Okay, press one. Press two. Press three. And on the thinking side, you see we have some deep thinking process. Just preparing here a strategy to come up here with an action plan. The left side clean restart. We restart here to Opus 4.6. Okay, this breaks the requirement. We need to go back. So you see trial and error, trial and error here on 4.6. This
  - [unverified] `-0xKV2i6M4U:00060`  is okay. This is a non-reasoning model. This is exactly what we expect. Okay. Press seven. You know, eight is excellent. Nine is very good. 10 button presses is still good. So let's see. We have a revised strategy. Okay. Yeah. Emergency exit. This is the right way to go. Beautiful. Press seven. Yes. Oh, good. Okay. Press eight. Press nine. What happens if I go above 50? Press
**side B** `-JiUyJVPM3Q#c013`  support=NO  subject_in_gold=full
  gold claim: In a prior video, Gemini Flash Thinking, when given the creator's elevator task with code execution activated, redefined the task's rules as mathematical functions and wrote Python code implementing them.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-JiUyJVPM3Q:00240`  long chain of sort stability test and in the end of this video I showed you here Gemini Flash Thinking and it was a task my elevator task and then the model itself decided because I activated the code execution to redefine my rules now as mathematical functions and it was augg about this how to do this how to plan this and then it wrote here the python code exactly with the mathematical function the same content
  - [unverified] `-JiUyJVPM3Q:00270`  as I instructed them so we went from a human task description to a mathematical logic notation and you know mathematics is code and then this mathematical logic was coded in Python also another video here the video was called the AI reasoning lie where I showed you here if you have premises that are formulated in our natural human English then we have here and I showed you exactly how to do this here first

### cc-0004 | 14yPeonB2P4#c018+1igqokIKJvg#c054 | q:87db3d11
**Q:** CMU's fine-tuning method and ThinkLess both rely on supervised fine-tuning, but what exactly does each one train the underlying model to learn as a result?
source videos: 14yPeonB2P4 (2025-03-10); 1igqokIKJvg (2025-05-21)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=full/none  anaphora=['the model']  leak=0.056  final_status=pass  leaked_side=both
pair_key: topic:supervised fine tuning
**side A** `14yPeonB2P4#c018`  support=YES  subject_in_gold=full
  gold claim: CMU's approach involves supervised fine-tuning of a base language model on reasoning training data so that the model learns to generate an optimal reasoning topology policy.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `14yPeonB2P4:00480`  a look what Carnegie Mellon University came up with so training data we need training data we have some reasoning data somewhere yeah beautifully and then we have a supervised finetuning of a base language model and now the task is a little bit different because now we train this llm to generate here an optimal reasoning topology policy so the reasoning we choose chain of thought or tree of thought or graph of Thought is reasoning topology is now
**side B** `1igqokIKJvg#c054`  support=YES  subject_in_gold=none
  gold claim: ThinkLess fine-tunes the target reasoning model via supervised fine-tuning on this synthetic paired dataset to learn a multi-style response distribution conditioned on the control token, in a step the creator calls a distillation phase.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `1igqokIKJvg:01170`  Now we have a data set here with the thinking and with the short thinking if you want each respond is prefixed with this control token either short or think that conditions now the model on the intended reasoning style. And then we go here supervised fine-tuning and we fine-tune the target reasoning model PI data on this synthetic pair data set via supervised fine tuning. This is our classical hugging phase a supervised fine tuning because the objective is to learn here multi-style response
  - [unverified] `1igqokIKJvg:01200`  distribution conditioned here on the control token and either it's short or it's the long thinking mode. You can call this a distillation phase. I'll show you this in a second that the model is capable of generating both types of responses here with a high fidelity. The paired construction ensures that the model response distribution will be balanced and we will have no collapse of the system. So what we do, we start here with an intelligent supervised fine-tuning and then we go to the reinforcement learning. This is our

### cc-0005 | 14yPeonB2P4#c018+78vn6XWvtzI#c012 | q:25d399bb
**Q:** CMU's method and the UT Dallas paper both invoke supervised fine-tuning, but what do they each claim it actually teaches a model about how to reason?
source videos: 14yPeonB2P4 (2025-03-10); 78vn6XWvtzI (2025-04-22)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/none  anaphora=['the model']  leak=0.059  final_status=pass  leaked_side=both
pair_key: topic:supervised fine tuning
**side A** `14yPeonB2P4#c018`  support=NO  subject_in_gold=full
  gold claim: CMU's approach involves supervised fine-tuning of a base language model on reasoning training data so that the model learns to generate an optimal reasoning topology policy.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `14yPeonB2P4:00480`  a look what Carnegie Mellon University came up with so training data we need training data we have some reasoning data somewhere yeah beautifully and then we have a supervised finetuning of a base language model and now the task is a little bit different because now we train this llm to generate here an optimal reasoning topology policy so the reasoning we choose chain of thought or tree of thought or graph of Thought is reasoning topology is now
**side B** `78vn6XWvtzI#c012`  support=YES  subject_in_gold=none
  gold claim: The University of Texas at Dallas paper's two main statements were that supervised fine-tuning helps models learn reasoning formats but often locks aligned models into an imitative, rigid reasoning mode that impedes further learning, and that their reinforcement learning approach fosters more genuine adaptive reasoning behavior.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `78vn6XWvtzI:00270`  convinced strong evidence but you are right if you say hey let's have a look let's have a look at this so two main statements you see it here I just put it out here supervised fine-tuning helps our models to learn reasoning formats it often locks aligned models into an imitative rigid reasoning mode that impedes further learning. So supervised finetuning is not great at all to help here the model in its reasoning process.
  - [unverified] `78vn6XWvtzI:00300`  And regarding reinforcement learning, they looked here at GRPO with a they developed here a novel mixed reward model with four or five additional components here from format and whatever reward structure integrating now both the perception and the cognition signals and everything. and they say, "Hey, our reinforcement learning approach here fosters here more genuine adaptive reasoning behavior." Hm. Let's have a look at

### cc-0006 | 2ENvGkkK36E#c002+96XVs6qcIT4#c012 | q:9fbedb9b
**Q:** How does DeepSeek R1's use of the GRPO reinforcement learning algorithm compare to how MASTERS applies GRPO in its training process?
source videos: 2ENvGkkK36E (2025-01-29); 96XVs6qcIT4 (2026-01-02)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=partial/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=claim_b
pair_key: topic:grpo
**side A** `2ENvGkkK36E#c002`  support=NO  subject_in_gold=partial
  gold claim: DeepSeek published a research paper explaining R1 in detail, including the Group Relative Policy Optimization (GRPO) reinforcement learning algorithm.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `2ENvGkkK36E:00000`  hello Community open R1 what is it how can we use it now you know we have DeepSeek R1 download close to 200,000 downloads here for in the last days from Hugging Face we have it available we can use it and you might say what is open R1 now let's open up this video and let's have a deeper look now you know there's a beautiful research paper by DeepSeek explaining here R1 in
  - [unverified] `2ENvGkkK36E:00030`  detail and we have here the reinforcement learning algorithm we have here the group relative policy optimization described in detail and everything is beautiful but you know then there was this particular spark and in my video that I showed you here and I was talking here about R1 distilled version smaller version not the original huge r one but we have a 32 billion version we have even a 1.5 billion version that is distilled from
**side B** `96XVs6qcIT4#c012`  support=NO  subject_in_gold=full
  gold claim: MASTERS simultaneously uses classical reinforcement learning (GRPO) not to explore new paths but to perform post hoc selection on pre-generated teacher responses, rewarding those that are both correct and transferable.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `96XVs6qcIT4:00210`  idea about the topic starts now training, the teacher is now progressively becoming more and more intelligent, more and more unmasked, gradually therefore increasing the complexity of the representation. Now you know this is our standard curriculum learning now done here in a very interesting way. Simultaneously Nvidia tells us the framework uses here our classical reinforcement learning our GRPO not to explore the new path but to perform now a post hoc selection on now
  - [unverified] `96XVs6qcIT4:00240`  hold on to your socks and the pre-generated responses by the teacher rewarding those that are both correct and transferable. And you see we are looking here probably for two different loss function we have to combine in an intelligent way. So masters here proves here that modifying the teacher capacity dynamically start slow and become more and more intelligent is just as important as the training data itself. It demonstrates here that an offline reinforcement learning with our

### cc-0007 | 2ENvGkkK36E#c002+7ec_0NPxmnA#c035 | q:1def444e
**Q:** DeepSeek's R1 paper documents GRPO as part of the model's design, while a 14B model's RPT setup also relies on GRPO to update weights every cycle—how does the way GRPO is presented in DeepSeek's writeup differ from its actual role in driving those continuous weight updates during RPT training?
source videos: 2ENvGkkK36E (2025-01-29); 7ec_0NPxmnA (2025-06-15)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=partial/full  anaphora=['the model']  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:grpo
**side A** `2ENvGkkK36E#c002`  support=NO  subject_in_gold=partial
  gold claim: DeepSeek published a research paper explaining R1 in detail, including the Group Relative Policy Optimization (GRPO) reinforcement learning algorithm.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `2ENvGkkK36E:00000`  hello Community open R1 what is it how can we use it now you know we have DeepSeek R1 download close to 200,000 downloads here for in the last days from Hugging Face we have it available we can use it and you might say what is open R1 now let's open up this video and let's have a deeper look now you know there's a beautiful research paper by DeepSeek explaining here R1 in
  - [unverified] `2ENvGkkK36E:00030`  detail and we have here the reinforcement learning algorithm we have here the group relative policy optimization described in detail and everything is beautiful but you know then there was this particular spark and in my video that I showed you here and I was talking here about R1 distilled version smaller version not the original huge r one but we have a 32 billion version we have even a 1.5 billion version that is distilled from
**side B** `7ec_0NPxmnA#c035`  support=YES  subject_in_gold=full
  gold claim: The creator argues that the 14B model does learn continuously throughout the RPT optimization process, based on the training loop where a forward pass generates reasoning traces, an automatic verifier compares outputs to ground truth, rewards are assigned, and weights are updated via GRPO (policy gradient algorithm) using backpropagation and an Adam optimizer.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `7ec_0NPxmnA:01620`  I showed you continuous learning is currently not possible this would be a way out of the dilemma. So you can ask hey how did this 14B model learn continuously or did it just apply its static knowledge to do here this new reinforcement pre-training learning and the answer is I think the model learns really continuously throughout the entire opt process why I would argue
  - [unverified] `7ec_0NPxmnA:01650`  in the following way given we have a specific textual context now this ex up less than t. So our model llm the policy pi data generates now its reasoning pool of g different responses and each each output is now a reasoning trace and a prediction. So this is the pure forward pass through our neural network. At this point no
  - [unverified] `7ec_0NPxmnA:01680`  learning is happening yet the model is just performing based on what it currently knows. And now the automatic verifier compares now each of the G predictions as I just showed you five minutes ago to the ground truth answer A from the data set from the training data set and if the completion is correct then it's an easy solution because then each of the G reasoning paths is assigned a reward function a reward R as scalar
  - [GROUNDED] `7ec_0NPxmnA:01710`  reward in the simplest case it's one for correct and zero for incorrect And using now what we know as a GRPO a policy gradient algorithm our nabla theta theta on j the system calculates how to change the model parameter data our what we are 14 billion free trainable parameter for example and the algorithm's core logic is for the reasoning path that led to a high reward
  - [GROUNDED] `7ec_0NPxmnA:01740`  in our reinforcement learning for the pre-training we just adjust here millions of weights it's indicator to make those specific path more likely to happen again in the future because this was a successful path. I want to have this in my memory. I want to have this representation encoded here in my weights and my biases and for all those path here in our J predictions with a chain of sort and a prediction that led to a low reward that was simply incorrect to the golden
  - [GROUNDED] `7ec_0NPxmnA:01770`  ground truth by the internet. adjust the weights in data to make this path less likely. We do not want to see this anymore in our neural network. So this adjustment is done using here the standard mechanism of a backprop and a gradient based optimizer like an Adam optimizer. And we achieved what we wanted. We wanted to modify here the tensor weight structure data of our LLM. And now we physically change them. So we did create a new slightly slightly
  - [unverified] `7ec_0NPxmnA:01800`  smarter model task and the loop starts again with the next one. This is now a complete new view how to do pre-training given the experience we have with reinforcement learning. And I think the question is how far can you go with this? Can you really go infinitely continuous learning with this opt process? I think this is fascinating. Yeah, of course the others

### cc-0008 | 4QnDrX6c96E#c008+7n5EVMtYA4I#c022 | q:6f8d1ca9
**Q:** How does Claude 3.7 Sonnet's thinking tool relate to in-context learning compared to how learning happens within CORAL's architecture?
source videos: 4QnDrX6c96E (2025-03-27); 7n5EVMtYA4I (2026-04-07)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=partial/none  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:in context learning
**side A** `4QnDrX6c96E#c008`  support=NO  subject_in_gold=partial
  gold claim: In a previous video, the creator showed an optimized prompt example for Claude 3.7 Sonnet and suggested that Anthropic's 'thinking tool' resembles in-context learning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `4QnDrX6c96E:00150`  particular system message tells me Open AI you highly capable beautiful yes think step by step through complex problems provide clear and accurate answer anticipate helpful followup information and beautiful and I said this does not explain anything of this so what do we have here I have a video on Claude 3.7 Sonnet the sonnet model and I show you here the example of the optimized prompt and I told you that looking here at the
  - [unverified] `4QnDrX6c96E:00180`  thinking tool example to this looks like an In-context learning now this is just days ago and I told you this I put it here said this is strange that this brings here this massive performance boost that goes beyond 100% Beyond Claude 3.7 extended thinking that I pay more than double so we need a SP of Genius so short question is you shot examples back
**side B** `7n5EVMtYA4I#c022`  support=YES  subject_in_gold=none
  gold claim: Learning in CORAL is entirely contextualized through in-context memory accumulation rather than weight updates.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `7n5EVMtYA4I:00510`  want, at test time, not at training time. So, it works at inference. And this is here a gradient-free search algorithm, if you take a step back and say, "What is the main cause of learning?" The learning is entirely contextualized through an in-context memory accumulation. So, around your LLM you have now this hopefully more intelligent file system, where all the multiple agents, four, five, eight agents, write into this file

### cc-0009 | 4QnDrX6c96E#c008+B4Ua8G-OZkw#c003 | q:9388e093
**Q:** How does Claude 3.7 Sonnet's 'thinking tool' resemblance to in-context learning compare to GeneGPT's use of in-context learning to integrate NCBI APIs for genomics tasks?
source videos: 4QnDrX6c96E (2025-03-27); B4Ua8G-OZkw (2025-09-26)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=partial/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:in context learning
**side A** `4QnDrX6c96E#c008`  support=NO  subject_in_gold=partial
  gold claim: In a previous video, the creator showed an optimized prompt example for Claude 3.7 Sonnet and suggested that Anthropic's 'thinking tool' resembles in-context learning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `4QnDrX6c96E:00150`  particular system message tells me Open AI you highly capable beautiful yes think step by step through complex problems provide clear and accurate answer anticipate helpful followup information and beautiful and I said this does not explain anything of this so what do we have here I have a video on Claude 3.7 Sonnet the sonnet model and I show you here the example of the optimized prompt and I told you that looking here at the
  - [unverified] `4QnDrX6c96E:00180`  thinking tool example to this looks like an In-context learning now this is just days ago and I told you this I put it here said this is strange that this brings here this massive performance boost that goes beyond 100% Beyond Claude 3.7 extended thinking that I pay more than double so we need a SP of Genius so short question is you shot examples back
**side B** `B4Ua8G-OZkw#c003`  support=NO  subject_in_gold=full
  gold claim: GeneGPT, a dedicated system trained for genomics that integrates NCBI APIs via in-context learning, improves accuracy on GeneTuring to 83%.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `B4Ua8G-OZkw:00030`  GeneGPT systems that we really trained for this, our improvement goes up to 83% accuracy by integrating now the NCBI APIs via in context learning ICL. But it degrades with smaller language model. So we need this huge huge LLMs. And the question is now how small can we go for genomics. Now if you're not GeneTuring familiar, this is the publication we have a GitHub. Everything is working for you beautifully. Now today we talk about

### cc-0010 | -HjPWrKavyA#c020+0oDgruiW7Gw#c018 | q:9a05a8f1
**Q:** When comparing how the finance study adapted Seed-OSS 36B into a domain-specific model against how a classical BERT system gets updated for knowledge graph maintenance, what does each approach's use of fine-tuning (plus, in one case, RL) look like in practice?
source videos: -HjPWrKavyA (2026-03-01); 0oDgruiW7Gw (2025-07-08)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:fine tuning
**side A** `-HjPWrKavyA#c020`  support=NO  subject_in_gold=full
  gold claim: The authors of the finance study took the Seed-OSS 36B base model and applied fine-tuning and reinforcement learning to create a finance-specialized model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-HjPWrKavyA:00480`  published here you see Apache 2.0 zero on hugging face and they released here a particular model they call it a seed OSS 36B base model and they released this here 2025 here in August 20th and the authors of today's paper took this particular model and said let's do some fine-tuning and reinforcement learning and let's make this open-source model a financial genius interested let's go on
  - [unverified] `-HjPWrKavyA:00510`  so they built here yuan 4.0 here if I'm not pronouncing this in the correct way I'm sorry and this is the latest flagship here for the financial sector 36 billion dense model initialized from the coss 36B base model but they had a very very specific training exercise so let's have a look this is the main study for today February 25th for financial intelligence and
**side B** `0oDgruiW7Gw#c018`  support=NO  subject_in_gold=full
  gold claim: To update a knowledge graph, a classical BERT system is fine-tuned on new data such as the latest publications from the last two years, using domain-specific vocabulary, technical terms, and new entity types.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `0oDgruiW7Gw:00330`  amount of text and we will use this now also for the update process and yes of course so we take here a classical BERT system and then we will fine-tune it for a highly specialized high performance tool. So we will have to have new data. So the latest publication of the last two years for example to update here this uh knowledge graph and here you fine-tune BERT with your domain specific
  - [unverified] `0oDgruiW7Gw:00360`  vocabulary with your domain specific new technical terms and with your new entity types that might emerge here in the knowledge graph. So great fantastic update absolutely what you want. So you have now a beautiful powerful neural engine. Remember you can use BERT here as a cross encoder and if you have the BERT architecture with a token classification head on top of you have a real powerful neural engine. So therefore

### cc-0011 | -HjPWrKavyA#c020+1067jj67toY#c057 | q:7f55a878
**Q:** Between the finance study's approach to specializing Seed-OSS 36B and the way DSPy is framed relative to fine-tuning, how does each one's method of customizing model behavior—altering weights versus working through prompts and context—actually play out?
source videos: -HjPWrKavyA (2026-03-01); 1067jj67toY (2025-07-15)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/full  anaphora=['the model']  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:fine tuning
**side A** `-HjPWrKavyA#c020`  support=NO  subject_in_gold=full
  gold claim: The authors of the finance study took the Seed-OSS 36B base model and applied fine-tuning and reinforcement learning to create a finance-specialized model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-HjPWrKavyA:00480`  published here you see Apache 2.0 zero on hugging face and they released here a particular model they call it a seed OSS 36B base model and they released this here 2025 here in August 20th and the authors of today's paper took this particular model and said let's do some fine-tuning and reinforcement learning and let's make this open-source model a financial genius interested let's go on
  - [unverified] `-HjPWrKavyA:00510`  so they built here yuan 4.0 here if I'm not pronouncing this in the correct way I'm sorry and this is the latest flagship here for the financial sector 36 billion dense model initialized from the coss 36B base model but they had a very very specific training exercise so let's have a look this is the main study for today February 25th for financial intelligence and
**side B** `1067jj67toY#c057`  support=YES  subject_in_gold=full
  gold claim: The creator positions DSPy as a middle ground between manual prompting and fine-tuning: manual prompting changes only the prompt text; DSPy modifies prompt text via new instructions and few-shot examples through context engineering; fine-tuning modifies the model's weights.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `1067jj67toY:01560`  There other optimizing algorithms that are coordinate prompt optimization. This is all simpler. You just can have a look at it. DSPy is in a beautiful in between of fine-tuning and manual prompting and in context learning. Let's have a look at this. So first line is manual prompting. Second line is DSPy and then we have fine-tuning. So you see with manual prompting what changes here is simply the prompt. No,
  - [GROUNDED] `1067jj67toY:01590`  the text of the prompt string itself. Yeah. With DSPy you have context engineering. The text of the prompt is now modified. You get new instruction and few short examples. Just do this here with a JSON format in the output for in the output and few short example that are really specific to your task. No. Or you say refine tuning. You know, I really want that the model learns this and really modifies here its weight so that it's really a

### cc-0012 | 4jwLkVMrdhQ#c011+NaeeCTutYEY#c003 | q:b063c676
**Q:** How does MiroFlow's design as a dedicated open-source agent framework for deep research compare to OpenAI's o3-full model's approach when used directly to carry out a deep research task?
source videos: 4jwLkVMrdhQ (2026-02-28); NaeeCTutYEY (2025-04-25)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=none/partial  anaphora=-  leak=0.136  final_status=pass  leaked_side=claim_b
pair_key: topic:deep research
**side A** `4jwLkVMrdhQ#c011`  support=YES  subject_in_gold=none
  gold claim: MiroFlow is an open-source agent framework focused on the deep research task, and the current version is version three, built over more than a year of development.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `4jwLkVMrdhQ:00240`  itself as a node in a graph and there's some absolute fascinating new developments happening. This is now the second paper by Tsinghua University and they go for open source agent framework for particular task a deep research task here you have of course all the GitHub please notice yeah by the way this is here they have other mods so this is really something that's going on for more than a year so this is version three if I'm correct so if you
**side B** `NaeeCTutYEY#c003`  support=NO  subject_in_gold=partial
  gold claim: The creator used OpenAI's o3-full model to perform a deep research task on reinforcement fine-tuning, which took 17 minutes and consulted 28 internet sources.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `NaeeCTutYEY:00120`  pay. So, I didn't have access to the reinforcement fine-tuning. And I understand that this is here a proprietary a a closed thing here from OpenAI but now today today was the time I said hey now I'm going to break free I open this box of Pandora I want to know what is reinforcement fine-tuning so I went to OpenAI to GPT-03 the full one and I did a deep research and after 17 minutes and after having access to 28
  - [unverified] `NaeeCTutYEY:00150`  sources you know and I want to stress as 28 internet sources 03 came back with a beautiful deep research and look here at all their explanation. This is a screenshot here and you know what there's hardly any information because it is often used as a reward model but instead of seeing the correct answer the model only gets a score or reward and must adjust its policy but give me

### cc-0014 | 1igqokIKJvg#c045+9NcVpt5tpxs#c003 | q:4e9a1239
**Q:** For a 235-billion-parameter mixture-of-experts model that exposes a thinking-mode slider for capping reasoning length, how does that reasoning-control mechanism stack up against how Self-MoE reorganizes a single monolithic LLM into a set of specialized expert sub-models?
source videos: 1igqokIKJvg (2025-05-21); 9NcVpt5tpxs (2025-01-19)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=full/none  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:mixture of experts
**side A** `1igqokIKJvg#c045`  support=YES  subject_in_gold=full
  gold claim: The creator references a mixture-of-experts model with 235 billion total parameters and 22 billion active parameters that has a thinking mode with a slider to control maximum thinking length, shown in a previous video about the o3 model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `1igqokIKJvg:00900`  is here o3 achieves here a 3% success rate. So I think yeah, beautiful. We have a new hard benchmark. So this will be amazing. So we will see now here have a look at this publication. I cannot go into the details but have a look at it. I love it. But we know this I showed you in my video about the new o3 model. Now if we had a look at the mixture of expert model with 235 billion free trainable parameter with active 22
  - [GROUNDED] `1igqokIKJvg:00930`  billion free trainable parameter. I told you we have this thinking mode and here we have a slider and we can control the maximum length of thinking. This is more or less if you want our token length that we want to pay for. So you have a thinking budget and you have this entity and it's in US dollars and you see you can move it around and I have for example 21K token thinking is really great. So if you want a budget and you want to say
**side B** `9NcVpt5tpxs#c003`  support=NO  subject_in_gold=none
  gold claim: Self-MoE transforms a monolithic LLM into a compositional system of specialized expert models.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `9NcVpt5tpxs:00030`  and let's have a look that you have to read this paper first because I was stuck with the original paper so I went here and remember here from Georgia Tech MIT IBM MIT October 7 2024 self mixture of expert system two words here a compositional large language model with some selfs specialized expert system so we transform now a monolitic llm into a compositional model system of experts
  - [unverified] `9NcVpt5tpxs:00060`  specialized experts and you might ask why well this is the beauty because then we will pick some of those experts specialized expert from our llm and we will magnify them we will give them more power so we will have a different specialization pattern emerging in our monolithic llm so if you have read the two paper great let's define what is a self adaptive llm meaning this is even more

### cc-0015 | 1igqokIKJvg#c045+9KMxNZ2CvUg#c039 | q:e572248c
**Q:** For controlling and customizing behavior in a mixture-of-experts setup, how does the approach used by that 235B/22B-parameter thinking-mode model—with its slider for capping reasoning length—compare to what's being proposed for Llama 4 Maverick's 128 experts in terms of tailoring critique sets to each expert?
source videos: 1igqokIKJvg (2025-05-21); 9KMxNZ2CvUg (2025-04-06)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/none  anaphora=-  leak=0.033  final_status=pass  leaked_side=both
pair_key: topic:mixture of experts
**side A** `1igqokIKJvg#c045`  support=NO  subject_in_gold=full
  gold claim: The creator references a mixture-of-experts model with 235 billion total parameters and 22 billion active parameters that has a thinking mode with a slider to control maximum thinking length, shown in a previous video about the o3 model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `1igqokIKJvg:00900`  is here o3 achieves here a 3% success rate. So I think yeah, beautiful. We have a new hard benchmark. So this will be amazing. So we will see now here have a look at this publication. I cannot go into the details but have a look at it. I love it. But we know this I showed you in my video about the new o3 model. Now if we had a look at the mixture of expert model with 235 billion free trainable parameter with active 22
  - [unverified] `1igqokIKJvg:00930`  billion free trainable parameter. I told you we have this thinking mode and here we have a slider and we can control the maximum length of thinking. This is more or less if you want our token length that we want to pay for. So you have a thinking budget and you have this entity and it's in US dollars and you see you can move it around and I have for example 21K token thinking is really great. So if you want a budget and you want to say
**side B** `9KMxNZ2CvUg#c039`  support=YES  subject_in_gold=none
  gold claim: The creator speculates that Llama 4 Maverick, a 400 billion parameter mixture-of-experts model with 128 experts, could benefit from a similar approach of handcrafted principled critique sets tailored to each of its 128 experts.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `9KMxNZ2CvUg:00750`  space and the critique has now this opportunity to search in all the gradients of this search space and not lose some of these spaces. Now you know I thought when I did my video on Llama 4 the Maverick the 400 billion model and especially it's a mixture of expert and we have 128 experts and I thought you know this would be an opportunity for Llama I didn't know if they would take here this
  - [GROUNDED] `9KMxNZ2CvUg:00780`  new idea from DeepSeek that was just published two days ago by DeepSeek this golden set this this perfect set of principled critique and they are now handcrafted that hand-designed for each of those 128 experts in their specific expert domain. This would really provide here I think a reason a performance jump because now let's say one of those 128
  - [GROUNDED] `9KMxNZ2CvUg:00810`  experts is an expert in mathematics. One expert is an expert in financial mathematics and financial the next one is an expert in physics in medicine and biopharma. You get the idea. If you would provide them a starting set with the best principles and the best critique behavior for those principles, I think you could really make sense that you have so many experts here in this new Llama for Maverick. It's a 400 billion
  - [unverified] `9KMxNZ2CvUg:00840`  free trainable parameter model. So here you really would have the opportunity to further optimize or at least optimize the initial condition for the inference time scaling. Okay, let's come here to the core element. This shift now enables here the principle to be generated based on the input of the user query. So if I have a mathematical query here, the principles will be based here on

### cc-0018 | 12lAM-xPvu8#c005+14yPeonB2P4#c001 | q:c6573eda
**Q:** For someone comparing reasoning transparency across models, how does Claude 3.7 Sonnet's handling of chain-of-thought visibility to the end user stack up against what QwQ 32B does when it comes to exposing its own reasoning trace?
source videos: 12lAM-xPvu8 (2025-04-05); 14yPeonB2P4 (2025-03-10)
flags: observed_shape=single  side_support(A/B)=Y/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.083  final_status=pass  leaked_side=both
pair_key: topic:chain of thought
**side A** `12lAM-xPvu8#c005`  support=YES  subject_in_gold=full
  gold claim: The creator states that with Claude 3.7 Sonnet, users are not allowed to see the real thinking process or chain of thought.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `12lAM-xPvu8:00060`  yes Claude 3.7 Sonnet. Now we know with sonnet we are not allowed to see the real thinking process the chain of thought thinking. So therefore, as I showed you in my last video, we do not miss a lot of, but as I showed you here by the latest publication on Anthropic, the chain of thought reasoning that Claude 3.7 shows us is not the real thing, is not a real thinking process and can be very easily disturbed
**side B** `14yPeonB2P4#c001`  support=NO  subject_in_gold=full
  gold claim: QwQ 32B is a reasoning system that prints out each and every single thought of the machine explicitly.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `14yPeonB2P4:00000`  [Music] hello Community hello hello Community great that you are back and you might ask hey are you sure topological AI systems are we ready for that yes we are so let's start and if you are subscribe of this channel you know that in my last video where we looked at the explicit reasoning process and qwq 32B is a beautiful system because it really prints out each and every single thought of the machine

### cc-0019 | 12lAM-xPvu8#c005+14yPeonB2P4#c004 | q:c39f2b60
**Q:** When people talk about visibility into a model's reasoning, how does the restriction on seeing Claude 3.7 Sonnet's actual chain of thought compare to the kinds of structural patterns—like chain of thought, tree of thought, and graph of thought—that researchers have identified within o1 and o3's reasoning traces?
source videos: 12lAM-xPvu8 (2025-04-05); 14yPeonB2P4 (2025-03-10)
flags: observed_shape=single  side_support(A/B)=Y/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.059  final_status=pass  leaked_side=both
pair_key: topic:chain of thought
**side A** `12lAM-xPvu8#c005`  support=YES  subject_in_gold=full
  gold claim: The creator states that with Claude 3.7 Sonnet, users are not allowed to see the real thinking process or chain of thought.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `12lAM-xPvu8:00060`  yes Claude 3.7 Sonnet. Now we know with sonnet we are not allowed to see the real thinking process the chain of thought thinking. So therefore, as I showed you in my last video, we do not miss a lot of, but as I showed you here by the latest publication on Anthropic, the chain of thought reasoning that Claude 3.7 shows us is not the real thing, is not a real thinking process and can be very easily disturbed
**side B** `14yPeonB2P4#c004`  support=NO  subject_in_gold=full
  gold claim: Chain of thought, tree of thought, and graph of thought structures were discovered in the reasoning process/answer structure of o1 and o3 models.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `14yPeonB2P4:00090`  topology for the right task so easiest way is now we have the chain of thought the tree of thought and the graph of thought that we discovered here in the answer structure here in the reasoning process of o1 o3 B so instead of relying on simple linear chain of thought you know from the very old models o1 or o3 let's have a look at the latest reasoning models and in this video I told you here by Princeton University if we go beyond chain of thought

### cc-0021 | -hFJe5hXWps#c012+388I4ugcf-0#c001 | q:02487b4a
**Q:** When you look at the Xiaomi research's dual-adapter setup for its world model versus how the web world model paper structures its own architecture, how does each one divide up the functional pieces handling physics versus the other components?
source videos: -hFJe5hXWps (2026-03-08); 388I4ugcf-0 (2025-12-31)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=full/full  anaphora=['the paper']  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:world
**side A** `-hFJe5hXWps#c012`  support=YES  subject_in_gold=full
  gold claim: In that Xiaomi research, two dynamic adapters were used: one adapter for geometry and one adapter for the world model handling physics.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `-hFJe5hXWps:00151`  was new self-driving AI explained here a vision language action model on the Plus integrating a world model here for Xiaomi electric vehicles. They used in their latest research here as I told you two dynamic adapters. One adapter was here for the geometry and one adapter was for the world model for the physics. And now for the geometry adapter. And you remember they also used here V GGGD but this changes today because now we
**side B** `388I4ugcf-0#c001`  support=NO  subject_in_gold=full
  gold claim: The paper introduces a 'web world model' that separates physics from imagination/generation.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `388I4ugcf-0:00000`  Hello communities, so great that you are back. Yes, today we talk about a new form of world model, the web world model. And as you can see, we will separate here the physics from the imagination. Welcome to my channel Discovery. We have a look at the latest AI research paper. And yeah, they built here a galaxy travel atlas. This is here sci-fi simulation where we do have real physics algorithm that dictate here the layout of galaxies of stars, planetary clusters. And then the LLM textures here this geometry with mission
  - [unverified] `388I4ugcf-0:00120`  this the next day. So tomorrow maybe you already have all the information. Now what is the idea? The idea is we have a web framework. Yeah, where we have text code based environment controllability beautiful and on the other side we have the full defined world model with an almost unlimited context and now they say let's build something in the middle let's build something where the framework set the rules and the LLMs just fill in the content so you see the LLM is not the mastermind it's not this
  - [unverified] `388I4ugcf-0:00150`  AGI but we have a framework physics if you want state transition between physical systems that set the rules that set the dynamic what is possible what moves you can do in this environment and then the LLM is just giving you the story the narration and this is here a much more powerful model because the AI does not have to do all the syncing so we have here with this web world model unlimited context text code based environment controllability beautiful
  - [unverified] `388I4ugcf-0:00180`  the best of both worlds this is yet a publication as I already showed here published December 29, 2025. A new web world model, a middle ground world of world state and the physics are implemented in ordinary web code to ensure a logical consistency of both worlds if you want while the LLMs generate only quotation mark the context, the narratives and the high-level decision on top of this structured

### cc-0023 | 1067jj67toY#c002+GohEyWrex4s#c006 | q:ed8ab735
**Q:** How does the argument that 'context engineering' is essentially rebranded prompt engineering compare to the proposal to rename AGI to 'AKI' (artificial kindergarten intelligence) for GPT-5?
source videos: 1067jj67toY (2025-07-15); GohEyWrex4s (2025-08-11)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:terminology
**side A** `1067jj67toY#c002`  support=NO  subject_in_gold=full
  gold claim: The creator characterizes 'context engineering' as marketing slang for what was previously called prompt engineering.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `1067jj67toY:00030`  context engineering if you prefer here the more marketing slang. So let's have a look context engineering with DSPy. You have more or less just two things that you do. You have DSP programming. What does it mean? It simply means you write a high-level pipeline in Python using here specific modules in DSPy that are given to you. And then you have an optimizer. This is a compiler. That's all you do. It's an optimizer that runs on your high
**side B** `GohEyWrex4s#c006`  support=NO  subject_in_gold=full
  gold claim: The creator proposes renaming the concept from AGI to 'AKI' (artificial kindergarten intelligence), arguing this better reflects GPT-5's actual technical level.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `GohEyWrex4s:00060`  can go hyper. Now on a technical level there is a completely different image because if you look at the technical implementation we have a different curve and I would like to talk about this curve today and I call it not AGI but AKI. Let me explain. Two new studies just want to show you. Remember RAG the retrieval augmented generation. We now have from the Hong Kong University Lag the logic
  - [unverified] `GohEyWrex4s:00570`  You saw this in my last video and I think here the poll I showed you at the beginning of this video also a clear indication this emergence this spontaneous breaking into the intelligent path it's not there. So what is AGI? It is an artificial kindergarten intelligence because this is the level that GPT-5 operates on. It just stacks together some of these newly computed elements here in the deconstructed problem space and then it

### cc-0025 | 3fNUh39h7EI#c006+Ch_tstGzDxE#c035 | q:26918393
**Q:** How does LiveCodeBench Pro's focus during code-generation evaluation compare to what the decision-maker-attribute framework from the alignable decision makers study is actually examining when it's applied within the medical triage setting?
source videos: 3fNUh39h7EI (2025-06-19); Ch_tstGzDxE (2025-05-31)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=claim_a
pair_key: topic:benchmark methodology
**side A** `3fNUh39h7EI#c006`  support=NO  subject_in_gold=full
  gold claim: LiveCodeBench Pro asks not just whether a model can solve a problem but how it solves it and where its reasoning fails during code generation.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `3fNUh39h7EI:00060`  exceptional and let's see if the AI models are able to catch up the code and everything and the programs are available live code git live codebench pro GitHub repo here for you everything is there and you know what they are asking is not can it solve a particular problem but they ask hey how does it solve the problem how does it code this and where does its reasoning fail in the code generation part so absolutely fascinating to see in our large language
  - [unverified] `3fNUh39h7EI:00090`  model the text generation reasoning failures and now we look here at our code AIs and we ask where does the reasoning fail for the code generation is there anything similar let's look at the results I give you the results right away. And here you have it here, the live results. You can also have it from 2024, the first quarter of 2025. And you see in the hard category of this live codebench pro, none. Absolutely nobody, no model is able to achieve at least
**side B** `Ch_tstGzDxE#c035`  support=NO  subject_in_gold=full
  gold claim: The benchmark methodology draws on a related study titled "Language models are alignable decision makers," which applies to the medical triage domain and defines decision maker attributes (DMAs) that can be given high or low relevance/priority.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `Ch_tstGzDxE:00930`  I'm a complete idiot because I don't immediately understand what they are talking about. And you really have to read the paper to understand it. But let's look at the benchmark data. Before we look at the benchmark data, it is important that you understand a detail that we will find here in the final benchmark data. And this is here the study for it. Language models are alignable decision makers applications for the medical triage domain because there they come up with the definition of we have now the same. No, we have a context. We have a
  - [unverified] `Ch_tstGzDxE:00960`  question. Hey, we have a triage. So many people are lying in front of you. you as a doctor on which patient you go first to help this patient. What is the alpha priority if you have 10 people lying in front of you in the hospital? So you have different attributes that you decide are your decision attributes your decision maker attributes they are called DMAs and you can give um high relevance or low relevance here to
  - [unverified] `Ch_tstGzDxE:00990`  particular attributes. So for example here if you have a risk aversion you do not like a risk at all you can go with choice A the company guarantees to deliver here the full amount in 7 days never mind what is the example or B the company equally likely to deliver in 3 days or maybe in 11 days you know it's your risk so you can calculate now and they did this to my knowledge for the first time here different DAs for a

### cc-0026 | -hFJe5hXWps#c031+14yPeonB2P4#c033 | q:dab49c4d
**Q:** Between the inner MLP's test-time training step and TRM's reward-prediction training, what kind of loss function does each one actually optimize during learning?
source videos: -hFJe5hXWps (2026-03-08); 14yPeonB2P4 (2025-03-10)
flags: observed_shape=multi-video  side_support(A/B)=Y/N  both_side=False  subject(A/B)=none/none  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:loss function
**side A** `-hFJe5hXWps#c031`  support=YES  subject_in_gold=none
  gold claim: Step two is training the inner MLP on the fly: the transformer uses key and value activations as training data for the tiny inner MLP, computing a virtual loss function that asks the MLP to adjust its parameters so that feeding it a key produces the corresponding value.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `-hFJe5hXWps:00511`  transformer takes the key and value activations and uses them as the training data set for the tiny inner MLP. So it does calculate a virtual loss function. This means essentially it is asking the inner network the MLP hey if I feed your key A can you adjust your parameters only your MLP parameters to output the value A. And now to use a very specific algorithm I explain this in a minute and it performs a real gradient descent update
**side B** `14yPeonB2P4#c033`  support=NO  subject_in_gold=none
  gold claim: The topological reward model (TRM) learns to predict an aggregated reward score by minimizing a loss function such as regression or ranking loss against target labels, using supervised learning with explicit examples.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `14yPeonB2P4:00930`  and it provides here the selection of the optimal response without a separate reinforcement learning training phase so careful they invented here something different what is the core idea well that's easy the topological reward model now this is now something interesting and you might say why do we need this so let's have a closer look it learns to predict aggregated this is the solution aggregated reward score by minimizing your particular loss
  - [unverified] `14yPeonB2P4:00960`  function beautiful such as regression or ranking loss against the targets so this this process here is essentially a form of supervised learning where the model is provided with explicit examples see our notion of what constitutes here a good response so this explicit resample examples you remember they have here the continuous confidence score these are our calculated traveling salesman distances that is salesman travel between the five

### cc-0027 | -hFJe5hXWps#c031+DTELTVYSua0#c041 | q:74b17bb1
**Q:** When you line up the virtual loss used to train the inner MLP on the fly against the loss function that trains a VQ-VAE, how does each one's underlying design actually differ?
source videos: -hFJe5hXWps (2026-03-08); DTELTVYSua0 (2025-03-21)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=none/partial  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:loss function
**side A** `-hFJe5hXWps#c031`  support=YES  subject_in_gold=none
  gold claim: Step two is training the inner MLP on the fly: the transformer uses key and value activations as training data for the tiny inner MLP, computing a virtual loss function that asks the MLP to adjust its parameters so that feeding it a key produces the corresponding value.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `-hFJe5hXWps:00511`  transformer takes the key and value activations and uses them as the training data set for the tiny inner MLP. So it does calculate a virtual loss function. This means essentially it is asking the inner network the MLP hey if I feed your key A can you adjust your parameters only your MLP parameters to output the value A. And now to use a very specific algorithm I explain this in a minute and it performs a real gradient descent update
**side B** `DTELTVYSua0#c041`  support=YES  subject_in_gold=partial
  gold claim: The VQ-VAE training loss function has three main components: the reconstruction loss, the codebook loss from quantization, and the commitment loss with a beta hyperparameter controlling how strongly embeddings commit to the quantized vector.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `DTELTVYSua0:01020`  training loss function for this particular case of a vector quantized original aut encoder has three main components the pure reconstruction loss the codebook loss from the quantization and the commitment loss with our famous beta hyper parameter controlling how strongly the embeddings are committed to the quantized vector so VQ-VAE is now rather interesting we have our latent vector and codebook visually observed

### cc-0028 | 0ao20vRWgis#c003+DBBD7bPn0DY#c003 | q:63515d2e
**Q:** How does MiniMax-2.5's upgrade with stronger reasoning compare to what changed when Alibaba's Qwen team released the official non-preview version of QwQ 32B?
source videos: 0ao20vRWgis (2026-02-13); DBBD7bPn0DY (2025-03-09)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=claim_a
pair_key: topic:model release
**side A** `0ao20vRWgis#c003`  support=NO  subject_in_gold=full
  gold claim: MiniMax-2.5 (also referred to as MiniMax M2.5) is an upgraded general-purpose model with stronger reasoning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `0ao20vRWgis:00030`  model is here MiniMax-2.5. Also an upgraded general-purpose model with stronger reasoning. Absolutely what we are looking for. I'm not testing out agents. I'm not interested here if it can handle here any tool calls or whatever. I'm interested in the pure intelligence and the pure causal reasoning of a model. Let's say you want to apply this to finance, to medicine, to physics, anything to science or where the model has to make decisions, where
**side B** `DBBD7bPn0DY#c003`  support=NO  subject_in_gold=full
  gold claim: The new official non-preview version of QwQ 32B by Alibaba's Qwen team was released on March 5th.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `DBBD7bPn0DY:00000`  hello Community great that you are back we have a new qwq 32b and you know what compared to o1 it just uses 24 GB of V RAM have a look at this now I know three months ago I already did some videos on qwq but this was the preview version and three months ago we coded and I was really impressed by the coding abilities of this but now today on March 5th we have
  - [unverified] `DBBD7bPn0DY:00030`  now the brand new official non preview version and I have to tell you by Alibaba's Qwen team this is really impressive so let's have a look we have Apache 2.0 you can download it for free and they tell you here yeah qwq just 24 GB for Hardware requirement of VRAM compared to DeepSeek R1 I mean the real non-quantized version 1.5 terabyte of VRAM and they give you here

### cc-0030 | -HjPWrKavyA#c036+HcZ2QKgFWPI#c021 | q:6a096ec0
**Q:** Yuan 4.0's continual pre-training setup and Dream to Chat's world-model training both reference KL divergence regularization, but what role does that regularization actually play in each one's training objective?
source videos: -HjPWrKavyA (2026-03-01); HcZ2QKgFWPI (2025-08-29)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=none/none  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:training methodology
**side A** `-HjPWrKavyA#c036`  support=YES  subject_in_gold=none
  gold claim: Yuan 4.0's training used continual pre-training (CPT) with a Kullback-Leibler divergence self-regularization objective against a reference model to prevent catastrophic forgetting of base mathematical reasoning while infusing new financial data.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-HjPWrKavyA:00870`  decided now to develop now their own finance agent. Yeah. And they called it 4.0. You have guessed there are some other models before and this is just a 36 billion free trainable parameter model. So this you can run locally if you invest some thousands here for a unified memory for Mac or whatever. Now this model they trained in a very particular way that seems similar. Yeah, we have a continual pre-training of GPT.
  - [GROUNDED] `-HjPWrKavyA:00900`  They use our classical Kullback-Leibler divergence for the self-regularization objective against a reference model during CPT and this limits the gradient updates to prevent catastrophic forgetting of everything that we learn from base mathematical reasoning while infusing here this new dense financial data. You notice here we have a reference model our cookbook library and then we have reinforcement learning here with DPO and I say this is great fine
**side B** `HcZ2QKgFWPI#c021`  support=YES  subject_in_gold=none
  gold claim: Dream to Chat's dynamics learning part uses past experiences, such as pre-programmed theoretical car-user interactions, and trains the world model using an objective function based on an evidence lower bound with KL divergence regularization.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `HcZ2QKgFWPI:00570`  past experiences. No, we have to have something. So either we have a theoretical interaction or conversation of a car with a user and this is pre-programmed somewhere in the factory you know so you have classical communication patterns no beautiful train you have your world model you have an objective function you see here the formula for the objective function you have an evidence lower bound a classic technique from variational inference and as you see we have here KL divergence and this is simply a regularizing you
  - [GROUNDED] `HcZ2QKgFWPI:00600`  know that is to not to stray too far away here from the model dynamics from the previous step. And if you're not really familiar here, I have a particular video here, 52 minutes only on the new mathematics for AI and I explain every symbol, every notation, everything for you and then you are an expert. Part two, the behavior. Now once this if you want world model here in our conversation pattern is trained to a certain extent it becomes now yeah now

### cc-0031 | -HjPWrKavyA#c036+ARst0nlEgO4#c014 | q:17eac5da
**Q:** How does Yuan 4.0's continual pre-training strategy for absorbing new financial knowledge without losing its reasoning ability compare to the training-loop technique DEEPSEARCH uses to broaden the range of reasoning paths it explores?
source videos: -HjPWrKavyA (2026-03-01); ARst0nlEgO4 (2025-10-03)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=none/none  anaphora=['the model']  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:training methodology
**side A** `-HjPWrKavyA#c036`  support=YES  subject_in_gold=none
  gold claim: Yuan 4.0's training used continual pre-training (CPT) with a Kullback-Leibler divergence self-regularization objective against a reference model to prevent catastrophic forgetting of base mathematical reasoning while infusing new financial data.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-HjPWrKavyA:00870`  decided now to develop now their own finance agent. Yeah. And they called it 4.0. You have guessed there are some other models before and this is just a 36 billion free trainable parameter model. So this you can run locally if you invest some thousands here for a unified memory for Mac or whatever. Now this model they trained in a very particular way that seems similar. Yeah, we have a continual pre-training of GPT.
  - [GROUNDED] `-HjPWrKavyA:00900`  They use our classical Kullback-Leibler divergence for the self-regularization objective against a reference model during CPT and this limits the gradient updates to prevent catastrophic forgetting of everything that we learn from base mathematical reasoning while infusing here this new dense financial data. You notice here we have a reference model our cookbook library and then we have reinforcement learning here with DPO and I say this is great fine
**side B** `ARst0nlEgO4#c014`  support=NO  subject_in_gold=none
  gold claim: DEEPSEARCH's solution is to directly inject Monte Carlo tree search into the training loop, forcing the model to systematically map out a wider portion of the solution space via branching, exposing it to correct, incorrect, and partial reasoning paths.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `ARst0nlEgO4:00300`  problem but it fails to master the complete long horizon decision-making so let's solve this now and the idea here by Stanford is okay we take our good friend Monte Carlo search and directly inject it into the training loop and we just force the model to systematically map out a wider portion of the solution space because yes we have a tree and the tree is branching out so we don't collapse automatically here to an entropy trace exposes the model to a vast array of
  - [unverified] `ARst0nlEgO4:00330`  correct and also we have to learn also the incorrect one and partial reasoning but everything we want to discover the whole solution space we want to learn this is the main topic here no mic reward back propagation provides you the fine grade credit assignments we have a dozen videos on this and yes what a coincidence and here we have the direct connection to my last video directly rewarded with a higher Q value you remember in my last video we are talking about the solution to the plateauing is exactly here the Q

### cc-0032 | -OzH4buQzTM#c021+FAg4v2xaLYc#c026 | q:87152daa
**Q:** How does the benchmark score gap between the Llama 13B teacher and its distilled Llama 7B student on ALFWorld and Hotpot compare to the score gap between the Light-R1 32B model and the official DeepSeek R1 distilled 32B model?
source videos: -OzH4buQzTM (2025-05-22); FAg4v2xaLYc (2025-03-17)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=partial/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:benchmark scores
**side A** `-OzH4buQzTM#c021`  support=YES  subject_in_gold=partial
  gold claim: With a Llama 13B model as the teacher, the teacher achieved a task success score of 75 on one benchmark and 71 on another, while a distilled Llama 7B student achieved 68 and 61 respectively on those benchmarks (ALFWorld and Hotpot).
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-OzH4buQzTM:00450`  style. Great. If you want to see a detailed explanation here of the definition of those parameters here it is. But I'll say we go now and we have a look at the results. So here we are. Now let's look here at the last one. When the teacher model is here a llama model a 13 billion free trainable parameter model. And here you have this one two three benchmarks. And here in this benchmark you see now here from ALFWorld and Hotpot you see now the
  - [GROUNDED] `-OzH4buQzTM:00480`  parameter the task success the reasoning length the chain of sort matching and the latency as I told you so let's have a look so here's our teacher beautiful so we have I don't know 75 and then say if we do now a llama 7B and we do all the specific imitation learning from this teacher from 13b the student the 7B now comes is close to the teacher. Teacher has 75 and the student has 68. Teacher has 71. The student has 61. And yes, you can
**side B** `FAg4v2xaLYc#c026`  support=NO  subject_in_gold=full
  gold claim: The new Light-R1 32B model, released beginning of March 2025, achieved a performance score of 76.6, surpassing the official DeepSeek R1 distilled 32B's 72.6.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `FAg4v2xaLYc:00540`  Light-R1 32B but I'm going to show you in a minute this is now here the beginning of March 2025 has a performance of 76.6 so we not even come close but we so Close here to official DeepSeek variant is still from January so with less than two months we have now that we can build something that is even better than the original DeepSeek R1 32B isn't this

### cc-0033 | -OzH4buQzTM#c021+FAg4v2xaLYc#c035 | q:c2243407
**Q:** How does the performance gap between the Llama 13B teacher and its distilled Llama 7B student on ALFWorld and Hotpot compare to the performance jump observed between the Light-R1 14B and 32B models?
source videos: -OzH4buQzTM (2025-05-22); FAg4v2xaLYc (2025-03-17)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=partial/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:benchmark scores
**side A** `-OzH4buQzTM#c021`  support=YES  subject_in_gold=partial
  gold claim: With a Llama 13B model as the teacher, the teacher achieved a task success score of 75 on one benchmark and 71 on another, while a distilled Llama 7B student achieved 68 and 61 respectively on those benchmarks (ALFWorld and Hotpot).
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-OzH4buQzTM:00450`  style. Great. If you want to see a detailed explanation here of the definition of those parameters here it is. But I'll say we go now and we have a look at the results. So here we are. Now let's look here at the last one. When the teacher model is here a llama model a 13 billion free trainable parameter model. And here you have this one two three benchmarks. And here in this benchmark you see now here from ALFWorld and Hotpot you see now the
  - [GROUNDED] `-OzH4buQzTM:00480`  parameter the task success the reasoning length the chain of sort matching and the latency as I told you so let's have a look so here's our teacher beautiful so we have I don't know 75 and then say if we do now a llama 7B and we do all the specific imitation learning from this teacher from 13b the student the 7B now comes is close to the teacher. Teacher has 75 and the student has 68. Teacher has 71. The student has 61. And yes, you can
**side B** `FAg4v2xaLYc#c035`  support=NO  subject_in_gold=full
  gold claim: Comparing the 14B and 32B Light-R1 models, performance goes from 60% to 64.6%, a smaller jump than the previous size increase, indicating room for improvement.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `FAg4v2xaLYc:00750`  and if you want to compare the 14B to the 32B you see yeah it's it's not that it again doubles into performance in the next jump but it goes from 60 to 64.6% so interesting there's room for improvement but let's stay with this particular study today so they say here hey our little Light-R1 becomes really a mathematical wizard even outperforming some of the giant AI models and especially here the smaller 14B model

### cc-0034 | -JiUyJVPM3Q#c033+3tiAvRcviiY#c066 | q:48fc52ea
**Q:** How does the approach of evaluating SoT by comparing its results against traditional chain-of-thought prompting differ from SwarmAgentic's use of a deterministic rule-based Python script as judge for the travel planner task?
source videos: -JiUyJVPM3Q (2025-03-11); 3tiAvRcviiY (2025-06-22)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=partial/none  anaphora=-  leak=0.3  final_status=pass  leaked_side=both
pair_key: topic:evaluation methodology
**side A** `-JiUyJVPM3Q#c033`  support=YES  subject_in_gold=partial
  gold claim: The results of SoT were compared against traditional chain-of-thought prompting.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `-JiUyJVPM3Q:00780`  just check for self-consistency you know what self-consistency is we have some cases we want to do this three different reasoning paths for generated multiple polls for generating and then we let the AI system itself vote we have different voting systems let's go with the easiest one a majority voting system to say hey of those multiple answers what do you think AI is the best answer given then we have the final answer and then the results are compared simply against a traditional chain of Thought prompting and
**side B** `3tiAvRcviiY#c066`  support=YES  subject_in_gold=none
  gold claim: For the travel planner task, SwarmAgentic uses a deterministic rule-based Python script as judge, checking outputs against explicit rules like city stopovers, timing, and budget constraints.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `3tiAvRcviiY:02310`  Yeah, this is open to interpretation. No, no, no. We have an objective function. we evaluate the result. So we have different task but let's go with a travel planner that's easy no with a judge is a deterministic rule-based Python script and it simply checks against the list of my rules and if I define my query I say hey on Monday I want to start in San Francisco on Tuesday I want to be in New York for a stepover I want to be there for I don't
  - [GROUNDED] `3tiAvRcviiY:02340`  know 18 hours I have a budget for a hotel of $20 and then I want to go three days to I don't know Madrid and then I want to go 4 days and visit my aunt in Rome and then I want to take the boat to go back to I don't know rules simple rules budget check Monday in San Francisco check Tuesday in New York check simple you have scores you can go with a scale one to five you can aggregate the scores

### cc-0035 | -JiUyJVPM3Q#c033+3tiAvRcviiY#c067 | q:55f99247
**Q:** When judging output quality, how does the way SoT's results get benchmarked against traditional chain-of-thought prompting differ from the approach of using GPT-4 as a stand-in judge to score creative writing on coherence, creativity, and adherence to source terms?
source videos: -JiUyJVPM3Q (2025-03-11); 3tiAvRcviiY (2025-06-22)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=partial/full  anaphora=-  leak=0.074  final_status=pass  leaked_side=both
pair_key: topic:evaluation methodology
**side A** `-JiUyJVPM3Q#c033`  support=NO  subject_in_gold=partial
  gold claim: The results of SoT were compared against traditional chain-of-thought prompting.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-JiUyJVPM3Q:00780`  just check for self-consistency you know what self-consistency is we have some cases we want to do this three different reasoning paths for generated multiple polls for generating and then we let the AI system itself vote we have different voting systems let's go with the easiest one a majority voting system to say hey of those multiple answers what do you think AI is the best answer given then we have the final answer and then the results are compared simply against a traditional chain of Thought prompting and
**side B** `3tiAvRcviiY#c067`  support=YES  subject_in_gold=full
  gold claim: For creative writing tasks, evaluation becomes more subjective, requiring a strong LLM like GPT-4 to act as a proxy for human critique, rating coherence, creativity, and adherence to source terms on a scale of 1 to 10.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `3tiAvRcviiY:02340`  know 18 hours I have a budget for a hotel of $20 and then I want to go three days to I don't know Madrid and then I want to go 4 days and visit my aunt in Rome and then I want to take the boat to go back to I don't know rules simple rules budget check Monday in San Francisco check Tuesday in New York check simple you have scores you can go with a scale one to five you can aggregate the scores
  - [GROUNDED] `3tiAvRcviiY:02370`  beautiful or other constraint super for some creative writing task it becomes much more wobbling. No. So what do you need? You need a better AI system like GPT-4. This acts like a proxy for a human critique. No, this will understand if I'm here very emotional maybe or creative writing or whatever. But it's also depending here on the pre-training data. No. And
  - [GROUNDED] `3tiAvRcviiY:02400`  then for me it's easy. say to the LLM, hey, please write or rate the story's coherence, the story creativity and the adherence to the source terms on a scale of 1 to 10. So this is easy, no, but this is highly subjective here to the quality and the experience and the training and the domain specificity of the LLM. If it's all language-based, language is not like a theoretical physics

### cc-0038 | -JiUyJVPM3Q#c014+N_MhjTkWg54#c036 | q:d014fac2
**Q:** How does the approach of converting natural language premises into first-order logic notation compare to the hierarchical reasoning model's (HRM) use of structured latent-space operations for handling multi-step reasoning tasks?
source videos: -JiUyJVPM3Q (2025-03-11); N_MhjTkWg54 (2025-07-06)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/none  anaphora=['the model']  leak=0.045  final_status=pass  leaked_side=both
pair_key: topic:prior video reference
**side A** `-JiUyJVPM3Q#c014`  support=NO  subject_in_gold=full
  gold claim: The creator references another prior video called 'The AI Reasoning Lie' in which natural language premises were converted into first-order logic notation.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-JiUyJVPM3Q:00270`  as I instructed them so we went from a human task description to a mathematical logic notation and you know mathematics is code and then this mathematical logic was coded in Python also another video here the video was called the AI reasoning lie where I showed you here if you have premises that are formulated in our natural human English then we have here and I showed you exactly how to do this here first
**side B** `N_MhjTkWg54#c036`  support=YES  subject_in_gold=none
  gold claim: The creator previously covered a hierarchical reasoning model (HRM) video two days earlier, in which the model authors claimed spectacular performance on tasks requiring multi-step reasoning via powerful, structured, algorithmically effective latent-space operations.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `N_MhjTkWg54:01140`  anything that comes close to a logical chain. And you might say, "But wait, wait a minute. No, two days ago you showed us here a new AI model about hierarchical reasoning. And there we also used here a recurrent model." And you were absolutely right if you are a subscriber of my channel. And at that time I told you here that the authors said our model achieves a spectacular performance on tasks that require multi-step reasoning. The operation happening in its latent space. So we are
  - [GROUNDED] `N_MhjTkWg54:01170`  again operating here in the vector space must be powerful structured and algorithmically effective. And in this video I showed you a result that was just amazing. And now now we have nothing. So what is the difference? Have you spotted it already? Do you know it? Well, it's very easy. Remember that here in this particular case of hierarchical reasoning models, we were operating in

### cc-0039 | -JiUyJVPM3Q#c014+4828sGfx7dk#c060 | q:949b014c
**Q:** How does the approach of converting natural language premises into first-order logic notation compare in design to the agent-to-agent knowledge graph setup using eight operational DeepSeek agents (including relational extraction, schema alignment, conflict resolution, and evaluator agents)?
source videos: -JiUyJVPM3Q (2025-03-11); 4828sGfx7dk (2025-02-25)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=pass  leaked_side=both
pair_key: topic:prior video reference
**side A** `-JiUyJVPM3Q#c014`  support=NO  subject_in_gold=full
  gold claim: The creator references another prior video called 'The AI Reasoning Lie' in which natural language premises were converted into first-order logic notation.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-JiUyJVPM3Q:00270`  as I instructed them so we went from a human task description to a mathematical logic notation and you know mathematics is code and then this mathematical logic was coded in Python also another video here the video was called the AI reasoning lie where I showed you here if you have premises that are formulated in our natural human English then we have here and I showed you exactly how to do this here first
**side B** `4828sGfx7dk#c060`  support=NO  subject_in_gold=full
  gold claim: The creator previously showed a system with nine DeepSeek agents in an agent-to-agent knowledge graph setup with eight operational agents, including a relational extraction agent, a schema alignment agent, a conflict resolution agent, and a pure evaluator agent.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `4828sGfx7dk:01170`  you want to issue a new license you have to stick with this license and you have to give credit to the authors please remember this don't forget to do this so here we are closing remarks we can integrate this new research now do you remember here my video where I showed you that we have nine DeepSeek agents to agent and Knowledge Graph and those were our eight operational agents where we had a relational EX action agent a schema alignment agent a conflict

---
## EXCLUDED (failure status carried through for reference)

### cc-0001 | 14yPeonB2P4#c030+1igqokIKJvg#c007 | q:b0dc05ed
**Q:** How does CMU's framework's relationship to reinforcement learning differ from that of AdaptThink?
source videos: 14yPeonB2P4 (2025-03-10); 1igqokIKJvg (2025-05-21)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=none/full  anaphora=-  leak=0.0  final_status=subject_unnameable  leaked_side=both
pair_key: topic:reinforcement learning
**side A** `14yPeonB2P4#c030`  support=YES  subject_in_gold=none
  gold claim: The creator notes that CMU's framework is not reinforcement learning; it is a separate training-time optimization process combined with a test-time reward system, where the reward model is an independent model rather than part of an RL loop.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `14yPeonB2P4:00810`  classical term high-level pipeline that integrates the post training here from the training time with an inference time rewarding system and this careful new marketing term enables now an Adaptive topology selection process and you are absolutely amazed by us marketing Geniuses and I have to tell you yes but did you notice something we are not here in reinforcement learning we are here just into separate process here in the training time
  - [GROUNDED] `14yPeonB2P4:00840`  optimization and then we have a test time reward so careful the reward system is now not doing reinforcement learning but is an independent model that is now a pure reward model in the test time compute carefully just to make this clear remember test-time compute scaling we had our CoT and go and I told you hey this is quite heavy if we do this here really at inference test-time compute
  - [GROUNDED] `14yPeonB2P4:00900`  range of quality metrics that it has been fine tuned on great but you remember those models have the same backbone but they have a different objective here and they have different output layers talking about objectives just to make it clear the reward model is not used to then optimize the policy model like in a reinforcement learning but the reward model is then transferred here to our test-time scaling here in in inference time
  - [GROUNDED] `14yPeonB2P4:00930`  and it provides here the selection of the optimal response without a separate reinforcement learning training phase so careful they invented here something different what is the core idea well that's easy the topological reward model now this is now something interesting and you might say why do we need this so let's have a closer look it learns to predict aggregated this is the solution aggregated reward score by minimizing your particular loss
  - [GROUNDED] `14yPeonB2P4:01080`  factors if you want so this is now depending on the quality of your llm that you use to get for example a right score for the clarity of the response or was it really concisely deduced was it logically perfect so you see ah this could be a little bit difficult just to make this clear again you typically we have a reward model might be used to refine policy model via reinforcement learning but in this
  - [GROUNDED] `14yPeonB2P4:01110`  particular framework CMU decided no we use the TRM just applied as a selection mechanism that we activate in the inference computation in test time compute scaling careful and the training of the TRM is a supervised finetuning on a high quality data set that's also used here for the other one so it doesn't have to explore here the complete exploration space or the solution space via a reinforcement learning methodology and they argue we
**side B** `1igqokIKJvg#c007`  support=YES  subject_in_gold=full
  gold claim: AdaptThink is a novel reinforcement learning algorithm designed to teach reasoning models (R1 models or distilled models) when to switch on complex thinking mode versus answering without reasoning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `1igqokIKJvg:00090`  from a particular benchmark and then you have here the deepseek R1 and we go with But it's still Qwen 7B and you see it takes 3,300 tokens because we switched on here the thinking mode complex thinking it's beautiful yes it's gorgeous it explains everything but do we need this if we just want to have the result so and the or tell us now hey we propose now a new methodology called AdaptThink Adapt think this is a novel reinforcement
  - [GROUNDED] `1igqokIKJvg:00120`  learning algorithm we have a look at detail about this to teach you the reasoning models or R1 models or a distilled model here when really to switch on here the complex thinking mode but maybe the system is able to do it without here reasoning because look if you take here this AdaptThink 7B this is the model that they built it's available for you free of charge no problem they only give also here 2,222 tokens isn't this nice so what is

### cc-0003 | -0xKV2i6M4U#c004+0ao20vRWgis#c019 | q:64f80454
**Q:** When you look at how Claude Opus 4.6 in non-thinking mode worked through the elevator puzzle versus how GLM-5 arrived at its candidate solution, what does that reveal about their respective problem-solving approaches and the quality of the answers each one landed on?
source videos: -0xKV2i6M4U (2026-02-05); 0ao20vRWgis (2026-02-13)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=none/full  anaphora=-  leak=0.0  final_status=gold_insufficient  leaked_side=both
pair_key: topic:elevator/causal-reasoning-test
**side A** `-0xKV2i6M4U#c004`  support=NO  subject_in_gold=none
  gold claim: Claude Opus 4.6 non-thinking exhibited trial-and-error behavior and clean restarts during the elevator puzzle, which the creator says is expected for a non-reasoning model.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `-0xKV2i6M4U:00030`  elevator test. It is only going deep inside. Oh, revise the deterministic path. Okay, press one. Press two. Press three. And on the thinking side, you see we have some deep thinking process. Just preparing here a strategy to come up here with an action plan. The left side clean restart. We restart here to Opus 4.6. Okay, this breaks the requirement. We need to go back. So you see trial and error, trial and error here on 4.6. This
  - [unverified] `-0xKV2i6M4U:00060`  is okay. This is a non-reasoning model. This is exactly what we expect. Okay. Press seven. You know, eight is excellent. Nine is very good. 10 button presses is still good. So let's see. We have a revised strategy. Okay. Yeah. Emergency exit. This is the right way to go. Beautiful. Press seven. Yes. Oh, good. Okay. Press eight. Press nine. What happens if I go above 50? Press
**side B** `0ao20vRWgis#c019`  support=YES  subject_in_gold=full
  gold claim: At one point during the test, GLM-5 produced a candidate solution using 11 steps, which the creator judged as maybe not the best result yet.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `0ao20vRWgis:00330`  As you can see both systems have a different strategy. Okay, we have here a win with GLM-5. This is interesting. Detailed run simulation. Okay, this looks good. How many steps do we have here? Oh, 11. Okay, maybe not the best yet, but we are still in the reasoning process. You see, MiniMax-2.5. Okay, we are not testing here as you can see the agentic

### cc-0013 | 4jwLkVMrdhQ#c011+SovT1iKHkaU#c015 | q:b6c80ed5
**Q:** MiroFlow and the Salesforce AI Research work on deep research both target the same task, but how does MiroFlow's overall structure as an agent framework compare to the way the Salesforce approach relies on a single reasoning agent to get the job done?
source videos: 4jwLkVMrdhQ (2026-02-28); SovT1iKHkaU (2025-09-10)
flags: observed_shape=adjacent  side_support(A/B)=Y/N  both_side=False  subject(A/B)=none/full  anaphora=-  leak=0.0  final_status=gold_insufficient  leaked_side=none
pair_key: topic:deep research
**side A** `4jwLkVMrdhQ#c011`  support=YES  subject_in_gold=none
  gold claim: MiroFlow is an open-source agent framework focused on the deep research task, and the current version is version three, built over more than a year of development.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `4jwLkVMrdhQ:00240`  itself as a node in a graph and there's some absolute fascinating new developments happening. This is now the second paper by Tsinghua University and they go for open source agent framework for particular task a deep research task here you have of course all the GitHub please notice yeah by the way this is here they have other mods so this is really something that's going on for more than a year so this is version three if I'm correct so if you
**side B** `SovT1iKHkaU#c015`  support=NO  subject_in_gold=full
  gold claim: A second paper discussed is from Salesforce AI Research, focused on deep research using a single autonomously reasoning agent, published September 8, 2025.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `SovT1iKHkaU:00240`  in total at the end of the discussion they switched from a correct to an incorrect answer. I'm loving this study. Have a look at this study. But of course I told you there's a second study Salesforce AI research. So Salesforce research and they focus now on deep research. Now yes absolutely deep research is the topic and they say you know what if those multi-agent is not so really perfect now let's look at single agent
  - [unverified] `SovT1iKHkaU:00270`  and you know what we need an autonomously reasoning single agent. So great. This is now September 8, 2025. And I selected this paper here as a counterpoint to the first paper. It is beautiful. So deep research, you're familiar with this wherever you go. It's a free or your paid service. And this requires an extensive internet search or database search or search whatever you have. And you have a reasoning over many sources. And hopefully you have a synthesis over many replies. Now George

### cc-0016 | 388I4ugcf-0#c016+4828sGfx7dk#c015 | q:5ce96d86
**Q:** Between the world-generation framework and OctoTools, how does keeping core physics and state logic separate from the creative generation side compare to how OctoTools splits planning from execution across its planner and executor modules?
source videos: 388I4ugcf-0 (2025-12-31); 4828sGfx7dk (2025-02-25)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/none  anaphora=['the paper']  leak=0.0  final_status=subject_unnameable  leaked_side=both
pair_key: topic:architecture
**side A** `388I4ugcf-0#c016`  support=NO  subject_in_gold=full
  gold claim: The paper is built on four core design principles: separation of concerns (core physics/state transition rules distinct from creative LLM generation), typed interfaces (latent world state represented as explicit typed web interfaces/JSON schemas rather than vector embeddings), infinite worlds via deterministic generation (expansion respects a fixed schema to avoid exploding the action space), and graceful degradation (falling back to template structures when model calls are slow or unavailable).
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `388I4ugcf-0:00240`  this? Now they started here with four core design principles for building the web world models. First a separation of concerns. So the core rules and the state transition what we call physics. Let's say the dynamics of this physical system must be distinct from the creative generation from all the imagination that is happening. This is our LLM. Second typed interfaces. So the latent world state should be represented as explicit typed web interfaces. Guess
  - [unverified] `388I4ugcf-0:00270`  what JSON schemas rather than here some embedding a vector representation on a high-dimensional vector space. And then third the infinite worlds via a deterministic generation. So the expansion must respect a fixed schema to allow the world to grow without exploding here the action space and finally a graceful degradation because let's say the model calls are slower or unavailable you should fall back to some template structure.
**side B** `4828sGfx7dk#c015`  support=NO  subject_in_gold=none
  gold claim: OctoTools separates strategic reasoning (planning) from the actual execution of tool commands, using two modules: a planner module and an executor module.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `4828sGfx7dk:00270`  perfect performance idea is simple for an advanced context management separate here the Strategic reasoning from the actual execution of the tool commands this is what they found doing here their experiments so what we have in essence we have two modules we have one module for the planning the Strategic reasoning the planning and then we have one module that executes here for example a python tool environment you see easy now the plan

### cc-0017 | 388I4ugcf-0#c016+B4Ua8G-OZkw#c021 | q:18c80ebe
**Q:** When you set the world-generation framework's overall architecture alongside the NBA framework's structure, how does each project's high-level approach to organizing its system components compare?
source videos: 388I4ugcf-0 (2025-12-31); B4Ua8G-OZkw (2025-09-26)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/none  anaphora=['the paper']  leak=0.0  final_status=subject_unnameable  leaked_side=both
pair_key: topic:architecture
**side A** `388I4ugcf-0#c016`  support=NO  subject_in_gold=full
  gold claim: The paper is built on four core design principles: separation of concerns (core physics/state transition rules distinct from creative LLM generation), typed interfaces (latent world state represented as explicit typed web interfaces/JSON schemas rather than vector embeddings), infinite worlds via deterministic generation (expansion respects a fixed schema to avoid exploding the action space), and graceful degradation (falling back to template structures when model calls are slow or unavailable).
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `388I4ugcf-0:00240`  this? Now they started here with four core design principles for building the web world models. First a separation of concerns. So the core rules and the state transition what we call physics. Let's say the dynamics of this physical system must be distinct from the creative generation from all the imagination that is happening. This is our LLM. Second typed interfaces. So the latent world state should be represented as explicit typed web interfaces. Guess
  - [unverified] `388I4ugcf-0:00270`  what JSON schemas rather than here some embedding a vector representation on a high-dimensional vector space. And then third the infinite worlds via a deterministic generation. So the expansion must respect a fixed schema to allow the world to grow without exploding here the action space and finally a graceful degradation because let's say the model calls are slower or unavailable you should fall back to some template structure.
**side B** `B4Ua8G-OZkw#c021`  support=NO  subject_in_gold=none
  gold claim: The NBA framework's overall architecture is structured as a linear directed acyclic graph (DAG), which the creator says is beneficial for debugging.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `B4Ua8G-OZkw:00360`  result passing and we have a generalist SLM that has been trained for this particular single particular task to formulate now a beautiful answer as it is in the literature. So you see what we have is a directed acyclic graph. We have a linear DAG and this is beautiful if you want to do some debugging or whatever. Plus they tell us you know just to make sure we have the code models and they say if we do not trust our small language model in genomics. No I mean

### cc-0022 | 1067jj67toY#c002+9KMxNZ2CvUg#c029 | q:73b6d832
**Q:** What's the reasoning behind calling something 'context engineering' as opposed to prior terminology, and how does that compare to the logic that led to naming a training process rejective fine-tuning (RFT) rather than reinforcement fine-tuning?
source videos: 1067jj67toY (2025-07-15); 9KMxNZ2CvUg (2025-04-06)
flags: observed_shape=single  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/none  anaphora=-  leak=0.091  final_status=two_factuals  leaked_side=both
pair_key: topic:terminology
**side A** `1067jj67toY#c002`  support=NO  subject_in_gold=full
  gold claim: The creator characterizes 'context engineering' as marketing slang for what was previously called prompt engineering.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `1067jj67toY:00030`  context engineering if you prefer here the more marketing slang. So let's have a look context engineering with DSPy. You have more or less just two things that you do. You have DSP programming. What does it mean? It simply means you write a high-level pipeline in Python using here specific modules in DSPy that are given to you. And then you have an optimizer. This is a compiler. That's all you do. It's an optimizer that runs on your high
**side B** `9KMxNZ2CvUg#c029`  support=YES  subject_in_gold=none
  gold claim: During the critique step in training, votes are extracted and incorrect or too-easy answers are rejected, which is why the process is called rejective fine-tuning (RFT), not reinforcement fine-tuning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `9KMxNZ2CvUg:00480`  do this those are your principle that I wanted you have in your evaluation report then here the critique is here okay given the principle I vote here for this and this and this then you extract the votes what is incorrect or what is too easy you just forget about it you reject it this is why it's called rejective fine-tuning so RF is not reinforcement fine-tuning but rejective finetuning and then you build your data set for the
  - [unverified] `9KMxNZ2CvUg:00960`  domain, let's say this is an AI for a hospital, you don't need to train it on I don't know English poetry or how to cook a salad. No, you are only in medicine. So this reward model just focusing on medicine can have so much more deeper understanding than a general model. Yeah, just rejective fine tuning. We talked about it. Here we have a GRM to generate principle and critique in the

### cc-0024 | 3fNUh39h7EI#c006+6Prpuc5W5gw#c009 | q:432f3a31
**Q:** Compared to how LiveCodeBench Pro evaluates a model's reasoning process during code generation, what method did the researchers use to have GPT-4 Omni generate quiz-style prompts from full arXiv paper text?
source videos: 3fNUh39h7EI (2025-06-19); 6Prpuc5W5gw (2025-08-31)
flags: observed_shape=adjacent  side_support(A/B)=N/Y  both_side=False  subject(A/B)=full/full  anaphora=['the paper']  leak=0.042  final_status=leak  leaked_side=both
pair_key: topic:benchmark methodology
**side A** `3fNUh39h7EI#c006`  support=NO  subject_in_gold=full
  gold claim: LiveCodeBench Pro asks not just whether a model can solve a problem but how it solves it and where its reasoning fails during code generation.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `3fNUh39h7EI:00060`  exceptional and let's see if the AI models are able to catch up the code and everything and the programs are available live code git live codebench pro GitHub repo here for you everything is there and you know what they are asking is not can it solve a particular problem but they ask hey how does it solve the problem how does it code this and where does its reasoning fail in the code generation part so absolutely fascinating to see in our large language
  - [unverified] `3fNUh39h7EI:00090`  model the text generation reasoning failures and now we look here at our code AIs and we ask where does the reasoning fail for the code generation is there anything similar let's look at the results I give you the results right away. And here you have it here, the live results. You can also have it from 2024, the first quarter of 2025. And you see in the hard category of this live codebench pro, none. Absolutely nobody, no model is able to achieve at least
**side B** `6Prpuc5W5gw#c009`  support=YES  subject_in_gold=full
  gold claim: The authors fed the full text of each arXiv paper (including diagrams) to GPT-4 Omni and had it act like a quiz show host, generating a question (prompt) that the paper perfectly answers.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `6Prpuc5W5gw:00180`  Great. Just think about the amount of corpus you have in those papers. Now the if you want genius new idea what they had is to reverse prompt engineer from this point. So the owner said, "You know what? We give you the full text of the arXiv paper everything and and and diagram and everything to a powerful LLM like they decided for a GPT-4 Omni and the LM task is not to reproduce the paper but to act like a quiz show host and
  - [GROUNDED] `6Prpuc5W5gw:00210`  write here the question that this single particular arXiv paper perfectly answers. So the question is of course a prompt. So you see you have a detailed scientific explanation written by human authors and then you just ask here an LLM at GPT-4 omni hey now write questions where you are sure that in this single arXiv paper there's a perfect answer for this particular question now you understand that there are different

### cc-0029 | 0ao20vRWgis#c003+Ig4vqREYj4E#c001 | q:1a550940
**Q:** When MiniMax rolled out M2.5, they framed the upgrade around general reasoning gains, whereas OpenAI's GPT-5.4 launch on March 5th, 2026 was pitched around professional-work suitability—how do these two upgrade philosophies actually differ in what they're optimizing for?
source videos: 0ao20vRWgis (2026-02-13); Ig4vqREYj4E (2026-03-05)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/full  anaphora=-  leak=0.0  final_status=leak  leaked_side=both
pair_key: topic:model release
**side A** `0ao20vRWgis#c003`  support=NO  subject_in_gold=full
  gold claim: MiniMax-2.5 (also referred to as MiniMax M2.5) is an upgraded general-purpose model with stronger reasoning.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `0ao20vRWgis:00030`  model is here MiniMax-2.5. Also an upgraded general-purpose model with stronger reasoning. Absolutely what we are looking for. I'm not testing out agents. I'm not interested here if it can handle here any tool calls or whatever. I'm interested in the pure intelligence and the pure causal reasoning of a model. Let's say you want to apply this to finance, to medicine, to physics, anything to science or where the model has to make decisions, where
**side B** `Ig4vqREYj4E#c001`  support=NO  subject_in_gold=full
  gold claim: OpenAI introduced GPT-5.4, designed for professional work, on March 5th, 2026.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `Ig4vqREYj4E:00000`  Hello community. So great to see you. We have a new OpenAI GPT 5.4 AI model and I'm going to test it. So today March 5th, 2026 introducing here GPT 5.4 designed for professional work by Open AI. Now you know I have my own causal reasoning test. This is a scientific test. Can I use this while for science and you see here my YouTube playlist and everything is here. every model I tested to get a feeling if I can use this model

### cc-0036 | 3tM3yc9UI84#c047+Gnk-me1UqfE#c003 | q:35a6e138
**Q:** How does the availability of the S1 32B model on Hugging Face compare to the availability of the Qwen 3.6 A3B model in terms of the variety of versions offered?
source videos: 3tM3yc9UI84 (2025-02-04); Gnk-me1UqfE (2026-04-20)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/none  anaphora=-  leak=0.0  final_status=unneutralizable  leaked_side=claim_b
pair_key: topic:model availability
**side A** `3tM3yc9UI84#c047`  support=NO  subject_in_gold=full
  gold claim: The S1 32B model is available on Hugging Face under the name 'Simple scaling S1 32b' along with a tokenizer.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `3tM3yc9UI84:01050`  is there data evaluation training the visual everything available for you you have here the code you see as a about as symbol we have the llm and hugging face it's called Simple scaling S1 32b we have this intens of parallel beautiful we have a tokenizer for this yes yeah I told want to tell you the maximum token that is allowed by this model of 32k context length so this is your limiting factor or you go with any other model that you have to SFT beautiful and then
**side B** `Gnk-me1UqfE#c003`  support=NO  subject_in_gold=none
  gold claim: There are more than 151 quantizations of the Qwen 3.6 A3B model available on Hugging Face (referred to as 'face'), allowing users to find a version fitting their hardware.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `Gnk-me1UqfE:00030`  their causal reasoning performance. This is here on YouTube here an own playlist and you see everything here from Meta's new Mu Spark to GLM 5.1 to Qwen 3.6 plus, Gamma 4, GPT 5.4. So, here you have all the data about the other models. But now what we want to achieve today, maybe we can have this locally. And I know a 3.5B is quite a challenge, but look for the quantization on the
  - [unverified] `Gnk-me1UqfE:00060`  face, we have more than 151 model quantization. So, I guess whatever is your particular computer hardware infrastructure from VRAM, we find a model that maybe we can try to test it here locally. So, let's go. Now, you understand here we are here the whole week talking about here the core LLM and then the AI harnessing sphere. And today I my experiment I will utilize this harnessing sphere. And in a particular way,

### cc-0037 | 3tM3yc9UI84#c047+OoPVwK0KAF8#c006 | q:127a8e6f
**Q:** How does the availability of the S1 32B model on Hugging Face (including its tokenizer) compare to the availability of MiMo V2 Flash across GitHub and Hugging Face?
source videos: 3tM3yc9UI84 (2025-02-04); OoPVwK0KAF8 (2026-02-11)
flags: observed_shape=none  side_support(A/B)=N/N  both_side=False  subject(A/B)=full/partial  anaphora=-  leak=0.0  final_status=unneutralizable  leaked_side=claim_a
pair_key: topic:model availability
**side A** `3tM3yc9UI84#c047`  support=NO  subject_in_gold=full
  gold claim: The S1 32B model is available on Hugging Face under the name 'Simple scaling S1 32b' along with a tokenizer.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `3tM3yc9UI84:01050`  is there data evaluation training the visual everything available for you you have here the code you see as a about as symbol we have the llm and hugging face it's called Simple scaling S1 32b we have this intens of parallel beautiful we have a tokenizer for this yes yeah I told want to tell you the maximum token that is allowed by this model of 32k context length so this is your limiting factor or you go with any other model that you have to SFT beautiful and then
**side B** `OoPVwK0KAF8#c006`  support=NO  subject_in_gold=partial
  gold claim: MiMo V2 Flash is available on GitHub and Hugging Face.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [unverified] `OoPVwK0KAF8:00030`  attention. It has a multi-token prediction and [clears throat] it uses a new distillation process of a multi-tier on policy distillation. I have to try this model. So, here we are. This is here the GitHub repo. As you can see, 10,00 MiMo, you find it on Hugging Face, wherever you want to go. It's a mixture of expert model with 309 billion total parameters and 15 billion active

### cc-0040 | 05J5BKf373U#c046+4QnDrX6c96E#c003 | q:261e823f
**Q:** How does the argument for skipping an Anthropic premium in favor of DeepSeek R1, given their comparable benchmark scores, tie into the actual price gap between Claude 3.7 Sonnet's extended-thinking mode and its prompt-engineered scratch-pad base version?
source videos: 05J5BKf373U (2025-06-01); 4QnDrX6c96E (2025-03-27)
flags: observed_shape=multi-video  side_support(A/B)=Y/Y  both_side=True  subject(A/B)=partial/full  anaphora=-  leak=0.071  final_status=leak  leaked_side=both
pair_key: topic:pricing
**side A** `05J5BKf373U#c046`  support=YES  subject_in_gold=partial
  gold claim: The creator questions whether one should pay a premium to Anthropic given that DeepSeek R1 performs comparably on some benchmarks.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `05J5BKf373U:00780`  If you have this with DeepSeek going on, do you really have to pay Anthropic? I mean, CEO of Anthropic says of course you have to pay. No, but yeah, think about it. TBD4 Omni March 2025 is also so close by. So really have to compare the prices and you see now it's clear. No, not at all. Because look at Matt 500. This is an old very very old benchmark with competitive reasoning. And look, we
**side B** `4QnDrX6c96E#c003`  support=YES  subject_in_gold=full
  gold claim: The creator states that Claude 3.7 Sonnet with extended thinking costs more than double the price of the prompt-engineered scratch-pad base model version.
  pre-attached chunks ([GROUNDED]=independently re-found; [unverified]=verify by eye):
  - [GROUNDED] `4QnDrX6c96E:00030`  why the hell is the most expensive extended thinking Claude 3.7 Sonnet performance less than 50% of a scratch bad and a prompt engineer version how is this possible I mean just look at the prices no if I look at CLA son 3.7 no sying here for a particular Norm whatever I have here a normaliz $ 17 uh doll price beautiful so
  - [GROUNDED] `4QnDrX6c96E:00060`  this is here this Blue Line This Is Here the base model now if I take this base model and I just put in here a free scratch pad and I do a prompt engineering I can increase my performance I don't know significantly here but if I look at here the latest technology Claude 3.7 sonnet extended thinking the performance is far below a prompt engineering and and the price is more than
  - [unverified] `4QnDrX6c96E:00090`  double and I thought there's something wrong what's Happening Here how is it possible that for a solution that is half as good has half the performance as this one I pay double the price this cannot be here or no I mean what is an Tropic doing so I checked out OpenAI platform and I went for prompt engineering and I went in particular for the reasoning models no and here we have official OpenAI
