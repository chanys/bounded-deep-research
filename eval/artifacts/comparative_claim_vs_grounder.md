# Comparative claim vs grounder worksheet (27 candidates)

Per candidate, per side: claim, claim's own source chunks, grounder chunks, and the union chunk text (tagged). Both-side-grounded candidates first.
Write in **notes** to skip a question (with the reason); leave empty to keep.

## cc-0040
**question id:** cc-0040
**question:** How does the argument for skipping an Anthropic premium in favor of DeepSeek R1, given their comparable benchmark scores, tie into the actual price gap between Claude 3.7 Sonnet's extended-thinking mode and its prompt-engineered scratch-pad base version?
**comparison axis:** relationship between questioning Anthropic's price premium (vs DeepSeek R1) and the specific cost premium of Claude 3.7 Sonnet extended thinking vs base version  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.071  final_status=leak

### side A: 05J5BKf373U  claim `05J5BKf373U#c046`  (support=YES)
**claim:** The creator questions whether one should pay a premium to Anthropic given that DeepSeek R1 performs comparably on some benchmarks.
**claim source chunks:** 05J5BKf373U:00780
**grounder chunks:** 05J5BKf373U:00360, 05J5BKf373U:00390, 05J5BKf373U:00780
**union chunk text:**
- `05J5BKf373U:00360` [grounder]  2. But let's zoom in. You know there's always this question if you go with an older model and you ask me hey do I really have to pay up for a for Claude 4 well it really depends now on this particular task and you remember this is the ARC AGI 1 leaderboard now let's just look here at this benchmark data here on the right hand side you have Claude Opus 4 thinking 1k the AGI 1
- `05J5BKf373U:00390` [grounder]  scores 27% and you pay half a dollar per task Now you see there's another dot real close by a little bit better you know high up 28.6% but this is the Claude 3.7 in 16k thinking mode but it costs almost half. So which model should you choose? Well if you take here the sum and you say it has a better performance and it is quite cheaper I think you know
- `05J5BKf373U:00780` [claim+grounder]  If you have this with DeepSeek going on, do you really have to pay Anthropic? I mean, CEO of Anthropic says of course you have to pay. No, but yeah, think about it. TBD4 Omni March 2025 is also so close by. So really have to compare the prices and you see now it's clear. No, not at all. Because look at Matt 500. This is an old very very old benchmark with competitive reasoning. And look, we

### side B: 4QnDrX6c96E  claim `4QnDrX6c96E#c003`  (support=YES)
**claim:** The creator states that Claude 3.7 Sonnet with extended thinking costs more than double the price of the prompt-engineered scratch-pad base model version.
**claim source chunks:** 4QnDrX6c96E:00030, 4QnDrX6c96E:00060, 4QnDrX6c96E:00090
**grounder chunks:** 4QnDrX6c96E:00030, 4QnDrX6c96E:00060, 4QnDrX6c96E:00270
**union chunk text:**
- `4QnDrX6c96E:00030` [claim+grounder]  why the hell is the most expensive extended thinking Claude 3.7 Sonnet performance less than 50% of a scratch bad and a prompt engineer version how is this possible I mean just look at the prices no if I look at CLA son 3.7 no sying here for a particular Norm whatever I have here a normaliz $ 17 uh doll price beautiful so
- `4QnDrX6c96E:00060` [claim+grounder]  this is here this Blue Line This Is Here the base model now if I take this base model and I just put in here a free scratch pad and I do a prompt engineering I can increase my performance I don't know significantly here but if I look at here the latest technology Claude 3.7 sonnet extended thinking the performance is far below a prompt engineering and and the price is more than
- `4QnDrX6c96E:00090` [claim]  double and I thought there's something wrong what's Happening Here how is it possible that for a solution that is half as good has half the performance as this one I pay double the price this cannot be here or no I mean what is an Tropic doing so I checked out OpenAI platform and I went for prompt engineering and I went in particular for the reasoning models no and here we have official OpenAI
- `4QnDrX6c96E:00270` [grounder]  line and I'm for sure not going to pay here for the orange extended syncing performance line now the reasoning while I'm interested this is open source I don't want to pay 35 times more for I don't know an o1 or o3 or whatever I want to go open source to o1 now luckily from R1 we have distilled version 1.5b 3B 7B 32B and you remember

**verdict:** 
**notes:** 

---

## cc-0004
**question id:** cc-0004
**question:** CMU's fine-tuning method and ThinkLess both rely on supervised fine-tuning, but what exactly does each one train the underlying model to learn as a result?
**comparison axis:** what each SFT approach trains the model to learn  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.056  final_status=pass

### side A: 14yPeonB2P4  claim `14yPeonB2P4#c018`  (support=YES)
**claim:** CMU's approach involves supervised fine-tuning of a base language model on reasoning training data so that the model learns to generate an optimal reasoning topology policy.
**claim source chunks:** 14yPeonB2P4:00480
**grounder chunks:** 14yPeonB2P4:00480, 14yPeonB2P4:00510, 14yPeonB2P4:00540, 14yPeonB2P4:00660
**union chunk text:**
- `14yPeonB2P4:00480` [claim+grounder]  a look what Carnegie Mellon University came up with so training data we need training data we have some reasoning data somewhere yeah beautifully and then we have a supervised finetuning of a base language model and now the task is a little bit different because now we train this llm to generate here an optimal reasoning topology policy so the reasoning we choose chain of thought or tree of thought or graph of Thought is reasoning topology is now
- `14yPeonB2P4:00510` [grounder]  different given different tasks so you know in reinforcement learning we have a policy model and we have a reward model and yes you guessed it so uh C you came back and says you know for enhanced reasoning we do know a topological scaling and he would say hey finally some new marketing terms isn't this beautiful and he another marketing term and we start by a topological tuning so conal tells us hey we perform here classical supervised fine tuning
- `14yPeonB2P4:00540` [grounder]  using your high quality topological reasoning data set selected Now by careful another marketing slogan tag and we split here the training data into the training data set and the test data set and evaluation data set and whatever you like and the training data selected through a simple three-step process we make sure we have some diversity sampling we have the correct answer filtering and we have some rejection sampling that we know from the classical sft and then we we have the data then we have our training data set
- `14yPeonB2P4:00660` [grounder]  tuning we are training scaling here so this is here at the training time this is not a test time scaling a training scaling approach that fine tunes here at base llm and to learn how to generate optimal reasoning topology policy because you know the policy llm defines here the action that it will take and give you here the result by Carnegie Mellon University this leads here to a five % accuracy improvement over non

### side B: 1igqokIKJvg  claim `1igqokIKJvg#c054`  (support=YES)
**claim:** ThinkLess fine-tunes the target reasoning model via supervised fine-tuning on this synthetic paired dataset to learn a multi-style response distribution conditioned on the control token, in a step the creator calls a distillation phase.
**claim source chunks:** 1igqokIKJvg:01170, 1igqokIKJvg:01200
**grounder chunks:** 1igqokIKJvg:01140, 1igqokIKJvg:01170, 1igqokIKJvg:01380, 1igqokIKJvg:01410, 1igqokIKJvg:01440
**union chunk text:**
- `1igqokIKJvg:01140` [grounder]  here in the reward in a binary reward model minus one. And the same is for the correct short and the wrong short. So the reward system is is predefined. But of course, yeah, this is here what's really playing here. But reinforcement learning decouples separates the training in two objectives. Optimizing here the control token for effective mode selection and then refine the response. Let's have a look at this. So we generate now a synthetic pair a data set. Everything starts with a data set.
- `1igqokIKJvg:01170` [claim+grounder]  Now we have a data set here with the thinking and with the short thinking if you want each respond is prefixed with this control token either short or think that conditions now the model on the intended reasoning style. And then we go here supervised fine-tuning and we fine-tune the target reasoning model PI data on this synthetic pair data set via supervised fine tuning. This is our classical hugging phase a supervised fine tuning because the objective is to learn here multi-style response
- `1igqokIKJvg:01200` [claim]  distribution conditioned here on the control token and either it's short or it's the long thinking mode. You can call this a distillation phase. I'll show you this in a second that the model is capable of generating both types of responses here with a high fidelity. The paired construction ensures that the model response distribution will be balanced and we will have no collapse of the system. So what we do, we start here with an intelligent supervised fine-tuning and then we go to the reinforcement learning. This is our
- `1igqokIKJvg:01380` [grounder]  so step back short summary what we do we have to create very first step a data set and the data set is exactly what we want the system to turn. So a synthetic data set. The data set is created using here two expert models LLMs. We need a strong reasoning model for the long form responses with prefix with sync and an instruction following modeling for some concise short answer prefix with short. And this teaches now the other model to
- `1igqokIKJvg:01410` [grounder]  generate both styles condition on these control tokens. And what the artists did was nice. They said we employ DeepSeek R1 Qwen 1.5 billion free trainable parameter as the base model to train out the hybrid reasoning policy. So let's do this. So as we say here okay the first reasoning model with the switching control token they say we go with the full DeepSeek R1 671 billion free trainable parameters. They are beautiful. Do they generate here the long form data from an open source data
- `1igqokIKJvg:01440` [grounder]  set very well suited for multi-step complex reasoning chains? Great. So first point okay second point we need the short one and they say corresponding short form answers are derived using a Qwen 2.5 Math 1.5B Instruct and instruction tuned models optimized here for concise mathematical responses. So we have here all three LLMs perfectly attuned to their function in this concert and then you say let's start. So for the hybrid

**verdict:** 
**notes:** 

---

## cc-0020
**question id:** cc-0020
**question:** In the Xiaomi research setup versus Dream to Chat's dialogue system, what is each one's 'world model' component actually built to handle or predict?
**comparison axis:** what each system's 'world model' component is built to handle or predict  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.0  final_status=pass

### side A: -hFJe5hXWps  claim `-hFJe5hXWps#c012`  (support=YES)
**claim:** In that Xiaomi research, two dynamic adapters were used: one adapter for geometry and one adapter for the world model handling physics.
**claim source chunks:** -hFJe5hXWps:00151
**grounder chunks:** -hFJe5hXWps:00151
**union chunk text:**
- `-hFJe5hXWps:00151` [claim+grounder]  was new self-driving AI explained here a vision language action model on the Plus integrating a world model here for Xiaomi electric vehicles. They used in their latest research here as I told you two dynamic adapters. One adapter was here for the geometry and one adapter was for the world model for the physics. And now for the geometry adapter. And you remember they also used here V GGGD but this changes today because now we

### side B: HcZ2QKgFWPI  claim `HcZ2QKgFWPI#c006`  (support=YES)
**claim:** Dream to Chat constructs a dialogue world model that predicts user emotion, sentiment, and intention, such as a request to be driven to a meeting with a client.
**claim source chunks:** HcZ2QKgFWPI:00060, HcZ2QKgFWPI:00090
**grounder chunks:** HcZ2QKgFWPI:00060, HcZ2QKgFWPI:00390, HcZ2QKgFWPI:00450, HcZ2QKgFWPI:00480, HcZ2QKgFWPI:00900, HcZ2QKgFWPI:01020, HcZ2QKgFWPI:01320, HcZ2QKgFWPI:01980
**union chunk text:**
- `HcZ2QKgFWPI:00060` [claim+grounder]  Beihang University and they have a dream to chat. They say we will use a model based reinforcement learning on dialogues with a user belief modeling and you might say what are you talking about? You mean I'm talking to my car? Yeah, they are now exploring ways how you have a conversation with your car and how the car should respond to you. And you know how they do this? They construct a dialogue world model that we already talked about which could predict
- `HcZ2QKgFWPI:00090` [claim]  everything from the user emotion from the sentiment the intention of a user when the users hey bring me to my next meeting with my client XYZ and they define here a partially observable Markov decision process and they say this is the essence that we can do this and you might say hey what a coincidence because this was part of one of my last videos. So what they have they have a new principled approach to uncertainty. You don't know how what a user wants. If a
- `HcZ2QKgFWPI:00390` [grounder]  So the dialogue world model a learned model question is how they explain this layer that simulates here the conversation of the AI the car with the human. So instead of learning your policy directly from the real interaction for the AI agent the agent first learns this dialogue world model and it has three interconnected parts if you want. The first one is the belief inference model and I call this now here kind of a mind reader. So
- `HcZ2QKgFWPI:00450` [grounder]  sentiment, intent here from the text, from the conversation. And then we have a dynamic. No, we have to predict the future. AI is only to predict the future. So we have here and this is now my wording in in in gray or here in little bit green. You see here this is what I call here the crystal ball. I mean poor little AI here in my car has now to predict the future not knowing in what mood I will be when I enter the car. So if the agent is in state S at a particular time T and takes an action A
- `HcZ2QKgFWPI:00480` [grounder]  at a particular time T. What happens next? What is the future? Now the I model here in my car has to predict the next state and the immediate reward and it is composed here of two sub-models. Of course we have a transition model here between the state of the system. So the model imagines here the user reply what I will say and then the reward model and with the reward model this is our feedback. This predicts the quality of the conversation and only the best successful conversations will be
- `HcZ2QKgFWPI:00900` [grounder]  real nice also a car company but now they look at something different they generate now completely unseen driving environments. So it is not about the emotional state or the linguistic experience that the AI will have in a conversation with the human user. Now it is about the safety the driving environment and especially the unseen physical space of driving. So you see now we are dealing here with
- `HcZ2QKgFWPI:01020` [grounder]  Large-scale 3D driving scene generation with a geometry grounding now in our AI system. And they have the beautiful title LSD 3D. Okay, let's go with this. So you see again uncertainty and the AI has to deal with uncertainty, unseen driving environments. And the AI the task of the AI is now build thousands and tens of thousands of unseen driving environments we have not on video on camera. You have to check for every
- `HcZ2QKgFWPI:01320` [grounder]  whatever you want to have here the LLM the AI capacity to have really to generate all the driving scenes so your autonomous driving vehicle the AI in the car can learn how to cope with this environmental condition whenever the AI car will encounter In this video, you see here the driving trajectory is rendered from these generated 3D scenes. All video rendered in real time and feature here diverse geometry, lighting and different
- `HcZ2QKgFWPI:01980` [grounder]  here the uncertainty here in the three-dimensional representation space. And this allows you for a real-time rendering of physically grounded videos along novel, completely unseen trajectories like flooding in New York or a snowstorm in Miami or whatever you have. You can generate everything with this AI system. So you can build this virtual environments where the AI simulators here can now learn how a car should behave in those severe

**verdict:** 
**notes:** 

---

## cc-0026
**question id:** cc-0026
**question:** Between the inner MLP's test-time training step and TRM's reward-prediction training, what kind of loss function does each one actually optimize during learning?
**comparison axis:** type of loss function used to train each component  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.0  final_status=pass

### side A: -hFJe5hXWps  claim `-hFJe5hXWps#c031`  (support=YES)
**claim:** Step two is training the inner MLP on the fly: the transformer uses key and value activations as training data for the tiny inner MLP, computing a virtual loss function that asks the MLP to adjust its parameters so that feeding it a key produces the corresponding value.
**claim source chunks:** -hFJe5hXWps:00511
**grounder chunks:** -hFJe5hXWps:00511
**union chunk text:**
- `-hFJe5hXWps:00511` [claim+grounder]  transformer takes the key and value activations and uses them as the training data set for the tiny inner MLP. So it does calculate a virtual loss function. This means essentially it is asking the inner network the MLP hey if I feed your key A can you adjust your parameters only your MLP parameters to output the value A. And now to use a very specific algorithm I explain this in a minute and it performs a real gradient descent update

### side B: 14yPeonB2P4  claim `14yPeonB2P4#c033`  (support=YES)
**claim:** The topological reward model (TRM) learns to predict an aggregated reward score by minimizing a loss function such as regression or ranking loss against target labels, using supervised learning with explicit examples.
**claim source chunks:** 14yPeonB2P4:00930, 14yPeonB2P4:00960
**grounder chunks:** 14yPeonB2P4:01170
**union chunk text:**
- `14yPeonB2P4:00930` [claim]  and it provides here the selection of the optimal response without a separate reinforcement learning training phase so careful they invented here something different what is the core idea well that's easy the topological reward model now this is now something interesting and you might say why do we need this so let's have a closer look it learns to predict aggregated this is the solution aggregated reward score by minimizing your particular loss
- `14yPeonB2P4:00960` [claim]  function beautiful such as regression or ranking loss against the targets so this this process here is essentially a form of supervised learning where the model is provided with explicit examples see our notion of what constitutes here a good response so this explicit resample examples you remember they have here the continuous confidence score these are our calculated traveling salesman distances that is salesman travel between the five
- `14yPeonB2P4:01170` [grounder]  tokens it's training loss it's using a particular loss function is based on how well it predicts the next token in a linear sequence now normally the reward model outputs here a scalar reward value or a ranking score whatever you like to call it and it's typically trained using a regression or a ranking loss function and this is really different here for the cross entropy loss that we use here normally for the prediction of the next language token in a linear sequence but of

**verdict:** 
**notes:** 

---

## cc-0027
**question id:** cc-0027
**question:** When you line up the virtual loss used to train the inner MLP on the fly against the loss function that trains a VQ-VAE, how does each one's underlying design actually differ?
**comparison axis:** design of the training loss function (what it optimizes and its components)  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.0  final_status=pass

### side A: -hFJe5hXWps  claim `-hFJe5hXWps#c031`  (support=YES)
**claim:** Step two is training the inner MLP on the fly: the transformer uses key and value activations as training data for the tiny inner MLP, computing a virtual loss function that asks the MLP to adjust its parameters so that feeding it a key produces the corresponding value.
**claim source chunks:** -hFJe5hXWps:00511
**grounder chunks:** -hFJe5hXWps:00511, -hFJe5hXWps:00541
**union chunk text:**
- `-hFJe5hXWps:00511` [claim+grounder]  transformer takes the key and value activations and uses them as the training data set for the tiny inner MLP. So it does calculate a virtual loss function. This means essentially it is asking the inner network the MLP hey if I feed your key A can you adjust your parameters only your MLP parameters to output the value A. And now to use a very specific algorithm I explain this in a minute and it performs a real gradient descent update
- `-hFJe5hXWps:00541` [grounder]  on this tiny MLP model. Our matrix W1 and W3 inside this tiny MLP are really physically updated and they change their values during the forward pass. So we do have suddenly weights because they are the parameter of this second inner neural network layer but they are fast and they are able now therefore maybe to be computed even on an old-fashioned Nvidia platform on edge

### side B: DTELTVYSua0  claim `DTELTVYSua0#c041`  (support=YES)
**claim:** The VQ-VAE training loss function has three main components: the reconstruction loss, the codebook loss from quantization, and the commitment loss with a beta hyperparameter controlling how strongly embeddings commit to the quantized vector.
**claim source chunks:** DTELTVYSua0:01020
**grounder chunks:** DTELTVYSua0:01020, DTELTVYSua0:01560, DTELTVYSua0:01590, DTELTVYSua0:01680
**union chunk text:**
- `DTELTVYSua0:01020` [claim+grounder]  training loss function for this particular case of a vector quantized original aut encoder has three main components the pure reconstruction loss the codebook loss from the quantization and the commitment loss with our famous beta hyper parameter controlling how strongly the embeddings are committed to the quantized vector so VQ-VAE is now rather interesting we have our latent vector and codebook visually observed
- `DTELTVYSua0:01560` [grounder]  can really work here in a real-time environment where we have a robotic system with some continuous flow in the inference run so therefore we have to make it easier we have the flow matching now discretized into smaller step and we hope those steps convert real fast little bit of mathematics if you enjoy it if not flow matching now is the interesting technique of this paper used to train here the diffusion Transformer N1 to generate the real robot actions
- `DTELTVYSua0:01590` [grounder]  works by learning here a time dependent vector field that guides you the noisy action sequence toward meaningful task relevant action sequences couldn't be easier so this vector field is learn through a process now you know like any AI system we have to minimize the loss function and here the process is to minimize the flow matching loss function and during the inference run when we are time critical here with 120 HZ this layer
- `DTELTVYSua0:01680` [grounder]  coming next a small LLM language model with the action generation we have our diffusion transformer for the artificial annotation of data from only watching videos without having here the actuated data we have the latent action representation via vector vector quantized variational auto encoders we have as the loss function a specific flow matching loss function for the denoising and during inference run the number of iteration they found hey

**verdict:** 
**notes:** 

---

## cc-0030
**question id:** cc-0030
**question:** Yuan 4.0's continual pre-training setup and Dream to Chat's world-model training both reference KL divergence regularization, but what role does that regularization actually play in each one's training objective?
**comparison axis:** role/purpose of KL divergence regularization in each model's training objective  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.0  final_status=pass

### side A: -HjPWrKavyA  claim `-HjPWrKavyA#c036`  (support=YES)
**claim:** Yuan 4.0's training used continual pre-training (CPT) with a Kullback-Leibler divergence self-regularization objective against a reference model to prevent catastrophic forgetting of base mathematical reasoning while infusing new financial data.
**claim source chunks:** -HjPWrKavyA:00870, -HjPWrKavyA:00900
**grounder chunks:** -HjPWrKavyA:00900, -HjPWrKavyA:01650, -HjPWrKavyA:01860, -HjPWrKavyA:01890
**union chunk text:**
- `-HjPWrKavyA:00870` [claim]  decided now to develop now their own finance agent. Yeah. And they called it 4.0. You have guessed there are some other models before and this is just a 36 billion free trainable parameter model. So this you can run locally if you invest some thousands here for a unified memory for Mac or whatever. Now this model they trained in a very particular way that seems similar. Yeah, we have a continual pre-training of GPT.
- `-HjPWrKavyA:00900` [claim+grounder]  They use our classical Kullback-Leibler divergence for the self-regularization objective against a reference model during CPT and this limits the gradient updates to prevent catastrophic forgetting of everything that we learn from base mathematical reasoning while infusing here this new dense financial data. You notice here we have a reference model our cookbook library and then we have reinforcement learning here with DPO and I say this is great fine
- `-HjPWrKavyA:01650` [grounder]  highly professional absolutely convincing but lead to complete nonsense. So therefore now the second step here of this if you want 32 billion model that um kind of simulates you the human reasoning aspect here we have to have a modified dapo and the modified dapo is simple the order remove the KL divergences and the length penalty and if you think
- `-HjPWrKavyA:01860` [grounder]  have to depend here on huge proprietary models. Just wanted to show you open- source model. They do have the opportunity also to be really performant here in the financial sector. And if you really go here with a particular training here for the financial sector, you can easily outperform here all the proprietary models. Limitation. Yes, of course. If we remove the Kullback-Leibler penalty in the scoring here, this yeah drives up the accuracy on the training distribution and this
- `-HjPWrKavyA:01890` [grounder]  risks here the severe overoptimization and a model stripped of a Kullback-Leibler regularization is prone to catastrophic exploitation of its own reward function. Yes, we know but it shows you if you choose it in an intelligent way and you are careful you can at least outperform our big proprietary models. And this is here an absolutely fascinating insight. Imagine if we would be now constructing a discrete topological graph structure. This would be a mathematical procedure

### side B: HcZ2QKgFWPI  claim `HcZ2QKgFWPI#c021`  (support=YES)
**claim:** Dream to Chat's dynamics learning part uses past experiences, such as pre-programmed theoretical car-user interactions, and trains the world model using an objective function based on an evidence lower bound with KL divergence regularization.
**claim source chunks:** HcZ2QKgFWPI:00570, HcZ2QKgFWPI:00600
**grounder chunks:** HcZ2QKgFWPI:00570, HcZ2QKgFWPI:00600, HcZ2QKgFWPI:01860
**union chunk text:**
- `HcZ2QKgFWPI:00570` [claim+grounder]  past experiences. No, we have to have something. So either we have a theoretical interaction or conversation of a car with a user and this is pre-programmed somewhere in the factory you know so you have classical communication patterns no beautiful train you have your world model you have an objective function you see here the formula for the objective function you have an evidence lower bound a classic technique from variational inference and as you see we have here KL divergence and this is simply a regularizing you
- `HcZ2QKgFWPI:00600` [claim+grounder]  know that is to not to stray too far away here from the model dynamics from the previous step. And if you're not really familiar here, I have a particular video here, 52 minutes only on the new mathematics for AI and I explain every symbol, every notation, everything for you and then you are an expert. Part two, the behavior. Now once this if you want world model here in our conversation pattern is trained to a certain extent it becomes now yeah now
- `HcZ2QKgFWPI:01860` [grounder]  beautiful paper. You have then additional geometry grounded losses that add add a regularization loss here that is real similar to a Kullback-Leibler but different for the diffusion. And then you also can ensure or this here ensures with some other methodology and technique that the surface normals no and the depth maps here of the geometry scene stay if you want faithful to the underlying geometry. No, it means simply keeps the wall of the buildings flat and

**verdict:** 
**notes:** 

---

## cc-0034
**question id:** cc-0034
**question:** How does the approach of evaluating SoT by comparing its results against traditional chain-of-thought prompting differ from SwarmAgentic's use of a deterministic rule-based Python script as judge for the travel planner task?
**comparison axis:** evaluation methodology used to assess system outputs  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.3  final_status=pass

### side A: -JiUyJVPM3Q  claim `-JiUyJVPM3Q#c033`  (support=YES)
**claim:** The results of SoT were compared against traditional chain-of-thought prompting.
**claim source chunks:** -JiUyJVPM3Q:00780
**grounder chunks:** -JiUyJVPM3Q:00780
**union chunk text:**
- `-JiUyJVPM3Q:00780` [claim+grounder]  just check for self-consistency you know what self-consistency is we have some cases we want to do this three different reasoning paths for generated multiple polls for generating and then we let the AI system itself vote we have different voting systems let's go with the easiest one a majority voting system to say hey of those multiple answers what do you think AI is the best answer given then we have the final answer and then the results are compared simply against a traditional chain of Thought prompting and

### side B: 3tiAvRcviiY  claim `3tiAvRcviiY#c066`  (support=YES)
**claim:** For the travel planner task, SwarmAgentic uses a deterministic rule-based Python script as judge, checking outputs against explicit rules like city stopovers, timing, and budget constraints.
**claim source chunks:** 3tiAvRcviiY:02310, 3tiAvRcviiY:02340
**grounder chunks:** 3tiAvRcviiY:02310, 3tiAvRcviiY:02340
**union chunk text:**
- `3tiAvRcviiY:02310` [claim+grounder]  Yeah, this is open to interpretation. No, no, no. We have an objective function. we evaluate the result. So we have different task but let's go with a travel planner that's easy no with a judge is a deterministic rule-based Python script and it simply checks against the list of my rules and if I define my query I say hey on Monday I want to start in San Francisco on Tuesday I want to be in New York for a stepover I want to be there for I don't
- `3tiAvRcviiY:02340` [claim+grounder]  know 18 hours I have a budget for a hotel of $20 and then I want to go three days to I don't know Madrid and then I want to go 4 days and visit my aunt in Rome and then I want to take the boat to go back to I don't know rules simple rules budget check Monday in San Francisco check Tuesday in New York check simple you have scores you can go with a scale one to five you can aggregate the scores

**verdict:** 
**notes:** 

---

## cc-0001
**question id:** cc-0001
**question:** How does CMU's framework's relationship to reinforcement learning differ from that of AdaptThink?
**comparison axis:** relationship to/use of reinforcement learning in each framework  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/Y  both_side_grounded=True  leak=0.0  final_status=subject_unnameable

### side A: 14yPeonB2P4  claim `14yPeonB2P4#c030`  (support=YES)
**claim:** The creator notes that CMU's framework is not reinforcement learning; it is a separate training-time optimization process combined with a test-time reward system, where the reward model is an independent model rather than part of an RL loop.
**claim source chunks:** 14yPeonB2P4:00810, 14yPeonB2P4:00840, 14yPeonB2P4:00900, 14yPeonB2P4:00930, 14yPeonB2P4:01080, 14yPeonB2P4:01110
**grounder chunks:** 14yPeonB2P4:00810, 14yPeonB2P4:00840, 14yPeonB2P4:00870, 14yPeonB2P4:00900, 14yPeonB2P4:00930, 14yPeonB2P4:01080, 14yPeonB2P4:01110, 14yPeonB2P4:01410
**union chunk text:**
- `14yPeonB2P4:00810` [claim+grounder]  classical term high-level pipeline that integrates the post training here from the training time with an inference time rewarding system and this careful new marketing term enables now an Adaptive topology selection process and you are absolutely amazed by us marketing Geniuses and I have to tell you yes but did you notice something we are not here in reinforcement learning we are here just into separate process here in the training time
- `14yPeonB2P4:00840` [claim+grounder]  optimization and then we have a test time reward so careful the reward system is now not doing reinforcement learning but is an independent model that is now a pure reward model in the test time compute carefully just to make this clear remember test-time compute scaling we had our CoT and go and I told you hey this is quite heavy if we do this here really at inference test-time compute
- `14yPeonB2P4:00870` [grounder]  scaling so it's a good idea to prepare in the training-time compute like in the good old models here the non reasoning models yeah so what they did here both their models and you know we are talking here about the policy model that generates here the candidate response and defines the action to be taken under a reward model this is not a topological reward model so we have trm and this evaluates and scores now these candidates that were generated with a policy model based on a specific
- `14yPeonB2P4:00900` [claim+grounder]  range of quality metrics that it has been fine tuned on great but you remember those models have the same backbone but they have a different objective here and they have different output layers talking about objectives just to make it clear the reward model is not used to then optimize the policy model like in a reinforcement learning but the reward model is then transferred here to our test-time scaling here in in inference time
- `14yPeonB2P4:00930` [claim+grounder]  and it provides here the selection of the optimal response without a separate reinforcement learning training phase so careful they invented here something different what is the core idea well that's easy the topological reward model now this is now something interesting and you might say why do we need this so let's have a closer look it learns to predict aggregated this is the solution aggregated reward score by minimizing your particular loss
- `14yPeonB2P4:01080` [claim+grounder]  factors if you want so this is now depending on the quality of your llm that you use to get for example a right score for the clarity of the response or was it really concisely deduced was it logically perfect so you see ah this could be a little bit difficult just to make this clear again you typically we have a reward model might be used to refine policy model via reinforcement learning but in this
- `14yPeonB2P4:01110` [claim+grounder]  particular framework CMU decided no we use the TRM just applied as a selection mechanism that we activate in the inference computation in test time compute scaling careful and the training of the TRM is a supervised finetuning on a high quality data set that's also used here for the other one so it doesn't have to explore here the complete exploration space or the solution space via a reinforcement learning methodology and they argue we
- `14yPeonB2P4:01410` [grounder]  multitask evaluation structure for their topological reward model now this is kind of a challenge no this is kind of interesting because instead of having for reinforcement learning for a real important separate reward models like you go for factual correctness or you go for correctness or you go for whatever you like putting all all the factors into a general multitask trm a unified

### side B: 1igqokIKJvg  claim `1igqokIKJvg#c007`  (support=YES)
**claim:** AdaptThink is a novel reinforcement learning algorithm designed to teach reasoning models (R1 models or distilled models) when to switch on complex thinking mode versus answering without reasoning.
**claim source chunks:** 1igqokIKJvg:00090, 1igqokIKJvg:00120
**grounder chunks:** 1igqokIKJvg:00090, 1igqokIKJvg:00120, 1igqokIKJvg:00180, 1igqokIKJvg:00720, 1igqokIKJvg:00750, 1igqokIKJvg:01680, 1igqokIKJvg:01710, 1igqokIKJvg:01740, 1igqokIKJvg:01770
**union chunk text:**
- `1igqokIKJvg:00090` [claim+grounder]  from a particular benchmark and then you have here the deepseek R1 and we go with But it's still Qwen 7B and you see it takes 3,300 tokens because we switched on here the thinking mode complex thinking it's beautiful yes it's gorgeous it explains everything but do we need this if we just want to have the result so and the or tell us now hey we propose now a new methodology called AdaptThink Adapt think this is a novel reinforcement
- `1igqokIKJvg:00120` [claim+grounder]  learning algorithm we have a look at detail about this to teach you the reasoning models or R1 models or a distilled model here when really to switch on here the complex thinking mode but maybe the system is able to do it without here reasoning because look if you take here this AdaptThink 7B this is the model that they built it's available for you free of charge no problem they only give also here 2,222 tokens isn't this nice so what is
- `1igqokIKJvg:00180` [grounder]  here with a particular hyperparameter delta And now it turns out if you adopt a non-thinking mode more frequently if the delta is increased because you say hey end of thinking that's it. So we go here and this is so simple. We go with the classical openi PPO style. We even say hey without the callback library penality and we have a very simple formula here and yes of course a little bit of clipping but this is our PPO
- `1igqokIKJvg:00720` [grounder]  reasoning. Plus, it is based on the task complexity and the model's ability. I love this. Let's have a closer look. So, also important to see it's also reinforcement learning paradigm. And now what it does, it employs now two control tokens. Please remember control tokens. They will become important just in a minute. And we have one for the short concise response and one for the thinking for the detailed
- `1igqokIKJvg:00750` [grounder]  reasoning. Now it turns out and this is really important they cannot go with the regular GRPO because we have that the system collapses and now to understand why is important. So they tell us now here the core of our method is now a new GRPO a decoupled group relative policy optimization which decomposes the learning objective of a hybrid reasoning
- `1igqokIKJvg:01680` [grounder]  and the hyperparameter and exactly reinforcement learning and you say okay let's compare them now in their most effective way here we have the second paper and then adapt think here is the first paper now let's compare them efficient mode definition we just went through the short token distilled from a specialized short answer the control mechanism mechanism either to generate here the sync code to short as the first output token we have a two-stage mechanism
- `1igqokIKJvg:01710` [grounder]  supervised finetuning distillation and then a GPO and DGRPO modifies here the GPO objective to rebalance the gradient signals especially for the control tokens the key hyperparameters alpha and DGRPO and mitigation of mode collapse here with DGRPO and we have a beautiful learning core for the mode preference The first paper AdaptThink we have a pure no thinking which would be a no
- `1igqokIKJvg:01740` [grounder]  reasoning mode induced by an empty thinking segment. First generated token is end of thinking learns when to allow here the forced start of no thinking versus the standard thinking start. We work here with reasoning models relys on a base model being a thinking model. a reasoning model would be more correct and the no thinking behavior is bootstrapped during the reinforcement learning via as I told you specific prompting specific importance sampling and specific definition of the
- `1igqokIKJvg:01770` [grounder]  objective. We go here with the classical PPO style. So a much simpler way with value function and so on with constrained optimization and importance sampling we have the hyperparameter delta. Importance sampling ensures that a no thinking mode is also explored. Delta is here. We have to choose delta carefully. Key hyperparameter is here in the advantage function here. This delta directly bias towards no thinking if the

**verdict:** 
**notes:** 

---

## cc-0003
**question id:** cc-0003
**question:** When you look at how Claude Opus 4.6 in non-thinking mode worked through the elevator puzzle versus how GLM-5 arrived at its candidate solution, what does that reveal about their respective problem-solving approaches and the quality of the answers each one landed on?
**comparison axis:** problem-solving approach and solution quality on the elevator puzzle task  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.0  final_status=gold_insufficient

### side A: -0xKV2i6M4U  claim `-0xKV2i6M4U#c004`  (support=NO)
**claim:** Claude Opus 4.6 non-thinking exhibited trial-and-error behavior and clean restarts during the elevator puzzle, which the creator says is expected for a non-reasoning model.
**claim source chunks:** -0xKV2i6M4U:00030, -0xKV2i6M4U:00060
**grounder chunks:** (none)
**union chunk text:**
- `-0xKV2i6M4U:00030` [claim]  elevator test. It is only going deep inside. Oh, revise the deterministic path. Okay, press one. Press two. Press three. And on the thinking side, you see we have some deep thinking process. Just preparing here a strategy to come up here with an action plan. The left side clean restart. We restart here to Opus 4.6. Okay, this breaks the requirement. We need to go back. So you see trial and error, trial and error here on 4.6. This
- `-0xKV2i6M4U:00060` [claim]  is okay. This is a non-reasoning model. This is exactly what we expect. Okay. Press seven. You know, eight is excellent. Nine is very good. 10 button presses is still good. So let's see. We have a revised strategy. Okay. Yeah. Emergency exit. This is the right way to go. Beautiful. Press seven. Yes. Oh, good. Okay. Press eight. Press nine. What happens if I go above 50? Press

### side B: 0ao20vRWgis  claim `0ao20vRWgis#c019`  (support=YES)
**claim:** At one point during the test, GLM-5 produced a candidate solution using 11 steps, which the creator judged as maybe not the best result yet.
**claim source chunks:** 0ao20vRWgis:00330
**grounder chunks:** 0ao20vRWgis:00300, 0ao20vRWgis:00330, 0ao20vRWgis:00390, 0ao20vRWgis:00420, 0ao20vRWgis:00450, 0ao20vRWgis:00540, 0ao20vRWgis:00630, 0ao20vRWgis:00660, 0ao20vRWgis:00810, 0ao20vRWgis:00840, 0ao20vRWgis:00870, 0ao20vRWgis:00900, 0ao20vRWgis:00930, 0ao20vRWgis:00960, 0ao20vRWgis:00990, 0ao20vRWgis:01020, 0ao20vRWgis:01050, 0ao20vRWgis:01080, 0ao20vRWgis:01110, 0ao20vRWgis:01140
**union chunk text:**
- `0ao20vRWgis:00300` [grounder]  MiniMax does a very nice job here of giving us an idea what it could be working on. Here we have a revised plan now with GLM5. Okay, you see one MiniMax decided to go here real human sentences. GLM5 here is more or less here strictly focus here on the sequence of operation and the constraint.
- `0ao20vRWgis:00330` [claim+grounder]  As you can see both systems have a different strategy. Okay, we have here a win with GLM-5. This is interesting. Detailed run simulation. Okay, this looks good. How many steps do we have here? Oh, 11. Okay, maybe not the best yet, but we are still in the reasoning process. You see, MiniMax-2.5. Okay, we are not testing here as you can see the agentic
- `0ao20vRWgis:00390` [grounder]  Let us use here night shift. Maybe not such a great idea by GLM-5, but they're trying out. Okay. Invokes the emergency exit. MiniMax. Interesting. We have floor 29. This looks good. MiniMax looks real nice right now. Oh, what's going to happen now? Hey, final path construction here also in GM5. Nice.
- `0ao20vRWgis:00420` [grounder]  Really interested if the system will come up with a valid solution. Of course, we will run here validation because otherwise who knows if this is indeed here a valid solution to our task. I shift this on. Just figuring out if there are other ways to go there. I land on 27. Oh wow. Really goes iteratively now down here the
- `0ao20vRWgis:00450` [grounder]  floors from the end. Interesting strategy. Oh, we have a fail. Yeah, there's an energy limitation. So, GLM-5 decided to have now an optimization run. Beautiful. MiniMax is also thinking here. There seems to be a problem also with MiniMax currently.
- `0ao20vRWgis:00540` [grounder]  But yeah, there seems to be a problem with MiniMax. Has not yet found here the correct path. GLM-5 rather short in the answer. Just trying out different sequences of button presses, but token optimization. Okay, brute force. Oh, wow. This is quite a long run. Okay, I think both models have
- `0ao20vRWgis:00630` [grounder]  So many options, so many possibilities. You would not assume if you have here buttons A to H and a simple task to go from floor zero to floor 50. There are so many open possibility and you have to find you have to come up with a strategy understanding here the constraint of this puzzle and then find a valid path forward. Insert a break. Okay, GLM-5 is active
- `0ao20vRWgis:00660` [grounder]  again. This looks solid. Okay, let's move so far. Oh, this does not look good. 14. Currently GLM-5 has a solution with 14 button presses. This is not really an outstanding solution but we are happy if we find any valid solution at all and then we can have the validation run and then we can have another optimizer. MiniMax 2.5 we're still waiting.
- `0ao20vRWgis:00810` [grounder]  little bit thinking here in a little bit slower way. Never mind. This is what you see here. 500%. Because now we are just interested in the result. I think you see the reasoning traces are more or less identical which is not a good indication. But anyway, let's see what the system come up with. Now I want to have a real solution and I would be interested if it is GLM5 or MiniMax 2.5 who comes up first with a real solution
- `0ao20vRWgis:00840` [grounder]  and then of course we have to have the validation run of all of those systems. Oh we have it GLM 5 8 minutes 9 seconds the sort process and we have an official final answer. Beautiful. Look at this. So we have nine steps and plus emergency exit. So in total 10 presses. Okay. Final resources efficiency. Okay. This looks good.
- `0ao20vRWgis:00870` [grounder]  Positioned emergency exit. Here's the 10th one. Yes. Absolutely. Beautiful. Okay. So this tells us, hey, this run satisfies all objectives. legally and structurally impossible to shorten without violating the code collection constraints. Okay, I say validate if your solution is indeed a valid solution respect. Oh, MiniMax crashed. MiniMax 2.5 crashed. And now I can say validate if your solution
- `0ao20vRWgis:00900` [grounder]  is indeed a valid solution. And as you see, we accelerate again 500% because we don't want to wait for this. We just want to have here a final result. Interesting that MiniMax is trying here again now for the third time to start to solve this after it crashed two times. But GLM5 should be now really in the validation run of its 10 button press solution. So let's see if it comes up here with a validation that tells us the
- `0ao20vRWgis:00930` [grounder]  solution is invalid. 2 minutes 10 seconds. What? Green green. The proposed solution is invalid on technicality regarding the button press definition if the emergency exit is a button or not. Okay, forget about it. Validation report floor 50 reached presses. Yeah. Okay, we have here beautiful but the button press. Yeah, the emergency exit is not defined as a button but as a special something. Okay,
- `0ao20vRWgis:00960` [grounder]  forget about this. The definition of a button is not what should concern us. We go for the logical verification. Logically it satisfies all resource and state constraints output for clarity. Beautiful. This is it. We just copy it and you know exactly what is the next step. Yep. Energy. Okay. Invoke trigger. GLM5 has a solution. Not the best solution yet, but we have nine button presses plus the
- `0ao20vRWgis:00990` [grounder]  emergency exit. Okay, so let's see if this sequence is really a valid sequence. So again, both systems go off now on a very particular defined sequence. There's no freedom to do anything. Just want to see if MiniMax is now able to validate this is a valid solution or not. And GLM5 is now on the second validation run if you want. But
- `0ao20vRWgis:01020` [grounder]  let's see if there's a discrep answer between MiniMax and GLM5. And yes, as you can see. Okay, beautiful. So, let's just let them finish. Okay, GLM5 tells us there's a failure point. Okay, MiniMax tells us it's legally compliant. It's it's valid. So, GLM5 tells us now in the second validation incorrect. And MiniMax tells us it is correct. So GLM5 has not produced a
- `0ao20vRWgis:01050` [grounder]  single valid solution. Okay. At least it tells us yes here at step 8 it fails. We have a constraint violation. We have a definite failure point here because these present at least three presses here. Button C is disabled and therefore you cannot do this move and this is invalidated. So although we got here at first a valid now at the second validation GLM-5 tells us it is invalid.
- `0ao20vRWgis:01080` [grounder]  But why does MiniMax tell us here it's legally a legal fully compliant solution? So you can't have both systems here disagreeing on a single sequence. Come on. This is not to find something. This is just to validate here a sequence of nine letters. Look at this. MiniMax now changes its opinion. MiniMax says now, hey, you are absolutely correct. I made an error in
- `0ao20vRWgis:01110` [grounder]  my validation. So I give it now the reason why it is wrong. And MiniMax 2.5 comes up and says, oh yeah, I was wrong. Because yeah, button C is disabled at this point. So it simply ignored one of my instruction. It just ignored it. It is not a valid solution. Yes, thank you for catching this oversight. The validation should have flagged this rule. But MiniMax 2.5 why you have not done it in a correct way. You just skipped one of the constraint here which
- `0ao20vRWgis:01140` [grounder]  is not good. Look here it tells us legally fully compliant and then just give you the reason and says hey you are correct. I made a mistake. MiniMax 2.5 not the optimal answer I was looking for. GLM-5 failed.

**verdict:** 
**notes:** 

---

## cc-0013
**question id:** cc-0013
**question:** MiroFlow and the Salesforce AI Research work on deep research both target the same task, but how does MiroFlow's overall structure as an agent framework compare to the way the Salesforce approach relies on a single reasoning agent to get the job done?
**comparison axis:** architectural approach to deep research (framework vs single agent)  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=gold_insufficient

### side A: 4jwLkVMrdhQ  claim `4jwLkVMrdhQ#c011`  (support=YES)
**claim:** MiroFlow is an open-source agent framework focused on the deep research task, and the current version is version three, built over more than a year of development.
**claim source chunks:** 4jwLkVMrdhQ:00240
**grounder chunks:** 4jwLkVMrdhQ:00240, 4jwLkVMrdhQ:00540, 4jwLkVMrdhQ:00570, 4jwLkVMrdhQ:00660, 4jwLkVMrdhQ:00870, 4jwLkVMrdhQ:00900
**union chunk text:**
- `4jwLkVMrdhQ:00240` [claim+grounder]  itself as a node in a graph and there's some absolute fascinating new developments happening. This is now the second paper by Tsinghua University and they go for open source agent framework for particular task a deep research task here you have of course all the GitHub please notice yeah by the way this is here they have other mods so this is really something that's going on for more than a year so this is version three if I'm correct so if you
- `4jwLkVMrdhQ:00540` [grounder]  structures now the agent themselves and now as I told you you can see an agent as a fluent agent graph. What does it mean? The main agent is the root node and it can dynamically spawn specialized sub agent. What else we know about leaf nodes to investigate here specific clues in a story or the main agent can design to loop back to verify some finding. we have cyclic edges and it can pull
- `4jwLkVMrdhQ:00570` [grounder]  resources or all nodes together when certain conditions apply. So you see we've built a single agent graph structure that can expand and contract given the entropy and the complexity of the task. If you want it in one sentence, omni represent here the world as a graph and mirror flow represent here the logic as a graph. Why is it possible that graphs are the
- `4jwLkVMrdhQ:00660` [grounder]  answer. So the graph transversal guarantees here a logical solvability if you want using here an infinite generative high quality a dpo ppo subo whatever you have MiroFlow highlights also a critical failure mode in multi-agent system so when an agent delegates to a sub agent linearly the high fidelity context is lost but if you define the workflow as a programmable topology you can isolate
- `4jwLkVMrdhQ:00870` [grounder]  We have also our node but please note the nodes are now self-contained models of decision processes and our edges represent now the message passing interfaces. Okay, what I told you what is really interesting the metamorphosis we see in a graph because MiroFlow bypasses you the limit of a static architecture and we have now an execution policy that can alter the topology of our graph at runtime based on the uncertainty of the
- `4jwLkVMrdhQ:00900` [grounder]  task. So this means if an intermediate node calculates a high uncertainty the control tier triggers the a topological expansion of your graph. Let's say an ensemble expansion. So a particular vertex here K forks into a parallel subgraph executing multiple parallel rollouts. Maybe a tool calling maybe any other solver. The edges route back to a quality-aware aggregation node.

### side B: SovT1iKHkaU  claim `SovT1iKHkaU#c015`  (support=NO)
**claim:** A second paper discussed is from Salesforce AI Research, focused on deep research using a single autonomously reasoning agent, published September 8, 2025.
**claim source chunks:** SovT1iKHkaU:00240, SovT1iKHkaU:00270
**grounder chunks:** (none)
**union chunk text:**
- `SovT1iKHkaU:00240` [claim]  in total at the end of the discussion they switched from a correct to an incorrect answer. I'm loving this study. Have a look at this study. But of course I told you there's a second study Salesforce AI research. So Salesforce research and they focus now on deep research. Now yes absolutely deep research is the topic and they say you know what if those multi-agent is not so really perfect now let's look at single agent
- `SovT1iKHkaU:00270` [claim]  and you know what we need an autonomously reasoning single agent. So great. This is now September 8, 2025. And I selected this paper here as a counterpoint to the first paper. It is beautiful. So deep research, you're familiar with this wherever you go. It's a free or your paid service. And this requires an extensive internet search or database search or search whatever you have. And you have a reasoning over many sources. And hopefully you have a synthesis over many replies. Now George

**verdict:** 
**notes:** 

---

## cc-0024
**question id:** cc-0024
**question:** Compared to how LiveCodeBench Pro evaluates a model's reasoning process during code generation, what method did the researchers use to have GPT-4 Omni generate quiz-style prompts from full arXiv paper text?
**comparison axis:** methodology for evaluating/generating model reasoning or content (LiveCodeBench Pro's diagnostic approach vs GPT-4 Omni's quiz-generation approach)  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.042  final_status=leak

### side A: 3fNUh39h7EI  claim `3fNUh39h7EI#c006`  (support=NO)
**claim:** LiveCodeBench Pro asks not just whether a model can solve a problem but how it solves it and where its reasoning fails during code generation.
**claim source chunks:** 3fNUh39h7EI:00060, 3fNUh39h7EI:00090
**grounder chunks:** (none)
**union chunk text:**
- `3fNUh39h7EI:00060` [claim]  exceptional and let's see if the AI models are able to catch up the code and everything and the programs are available live code git live codebench pro GitHub repo here for you everything is there and you know what they are asking is not can it solve a particular problem but they ask hey how does it solve the problem how does it code this and where does its reasoning fail in the code generation part so absolutely fascinating to see in our large language
- `3fNUh39h7EI:00090` [claim]  model the text generation reasoning failures and now we look here at our code AIs and we ask where does the reasoning fail for the code generation is there anything similar let's look at the results I give you the results right away. And here you have it here, the live results. You can also have it from 2024, the first quarter of 2025. And you see in the hard category of this live codebench pro, none. Absolutely nobody, no model is able to achieve at least

### side B: 6Prpuc5W5gw  claim `6Prpuc5W5gw#c009`  (support=YES)
**claim:** The authors fed the full text of each arXiv paper (including diagrams) to GPT-4 Omni and had it act like a quiz show host, generating a question (prompt) that the paper perfectly answers.
**claim source chunks:** 6Prpuc5W5gw:00180, 6Prpuc5W5gw:00210
**grounder chunks:** 6Prpuc5W5gw:00180, 6Prpuc5W5gw:00210
**union chunk text:**
- `6Prpuc5W5gw:00180` [claim+grounder]  Great. Just think about the amount of corpus you have in those papers. Now the if you want genius new idea what they had is to reverse prompt engineer from this point. So the owner said, "You know what? We give you the full text of the arXiv paper everything and and and diagram and everything to a powerful LLM like they decided for a GPT-4 Omni and the LM task is not to reproduce the paper but to act like a quiz show host and
- `6Prpuc5W5gw:00210` [claim+grounder]  write here the question that this single particular arXiv paper perfectly answers. So the question is of course a prompt. So you see you have a detailed scientific explanation written by human authors and then you just ask here an LLM at GPT-4 omni hey now write questions where you are sure that in this single arXiv paper there's a perfect answer for this particular question now you understand that there are different

**verdict:** 
**notes:** 

---

## cc-0005
**question id:** cc-0005
**question:** CMU's method and the UT Dallas paper both invoke supervised fine-tuning, but what do they each claim it actually teaches a model about how to reason?
**comparison axis:** what supervised fine-tuning teaches a model about reasoning  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.059  final_status=pass

### side A: 14yPeonB2P4  claim `14yPeonB2P4#c018`  (support=NO)
**claim:** CMU's approach involves supervised fine-tuning of a base language model on reasoning training data so that the model learns to generate an optimal reasoning topology policy.
**claim source chunks:** 14yPeonB2P4:00480
**grounder chunks:** (none)
**union chunk text:**
- `14yPeonB2P4:00480` [claim]  a look what Carnegie Mellon University came up with so training data we need training data we have some reasoning data somewhere yeah beautifully and then we have a supervised finetuning of a base language model and now the task is a little bit different because now we train this llm to generate here an optimal reasoning topology policy so the reasoning we choose chain of thought or tree of thought or graph of Thought is reasoning topology is now

### side B: 78vn6XWvtzI  claim `78vn6XWvtzI#c012`  (support=YES)
**claim:** The University of Texas at Dallas paper's two main statements were that supervised fine-tuning helps models learn reasoning formats but often locks aligned models into an imitative, rigid reasoning mode that impedes further learning, and that their reinforcement learning approach fosters more genuine adaptive reasoning behavior.
**claim source chunks:** 78vn6XWvtzI:00270, 78vn6XWvtzI:00300
**grounder chunks:** 78vn6XWvtzI:00270, 78vn6XWvtzI:00360, 78vn6XWvtzI:00390, 78vn6XWvtzI:00420, 78vn6XWvtzI:01380, 78vn6XWvtzI:01410, 78vn6XWvtzI:01590, 78vn6XWvtzI:01620
**union chunk text:**
- `78vn6XWvtzI:00270` [claim+grounder]  convinced strong evidence but you are right if you say hey let's have a look let's have a look at this so two main statements you see it here I just put it out here supervised fine-tuning helps our models to learn reasoning formats it often locks aligned models into an imitative rigid reasoning mode that impedes further learning. So supervised finetuning is not great at all to help here the model in its reasoning process.
- `78vn6XWvtzI:00300` [claim]  And regarding reinforcement learning, they looked here at GRPO with a they developed here a novel mixed reward model with four or five additional components here from format and whatever reward structure integrating now both the perception and the cognition signals and everything. and they say, "Hey, our reinforcement learning approach here fosters here more genuine adaptive reasoning behavior." Hm. Let's have a look at
- `78vn6XWvtzI:00360` [grounder]  the floodgates, the complexity might really increase and might not be that easy. But so let's come here and the first is to summarize here the authors tell us here from the University of Texas at Dallas while supervised fine-tuning helps unaligned models so not reinforcement learning at all not aligned models follow here the instruction set it limits the exploration during reinforcement learning by promoting imitative reasoning. So they tell us hey
- `78vn6XWvtzI:00390` [grounder]  supervised fine-tuning it limits the exploration during the reinforcement learning and you know we always have this delicate balance between exploration and exploitation. Can we have a flashlight and we have a dark room and we look in the room with the flashlight at different spots in this dark room. We explore every corner or exploitation. We have already found one interesting object in the depth of the room. So we have now to
- `78vn6XWvtzI:00420` [grounder]  focus our light beam here on this object from different angles. Exploration exploitation and they tell us supervised fine-tuning is not that good and they say while prior works suggested supervised fine-tuned followed by reinforcement learning. So the classical SFT plus RL it offers you the best of both worlds. We find that applying supervised fine-tuning before GRPO you know the group relative policy optimization hurts
- `78vn6XWvtzI:01380` [grounder]  to follow the instruction of this model? So this is what I felt at the time reading this. So let's go back now to this original study and this is a beautiful study don't get me wrong and they tell us these findings highlight the limitation of supervised fine-tuning as a tool for enhancing the multimodal reasoning and somehow at the time I did not really agree with this I felt different it's a feeling you know and then they say
- `78vn6XWvtzI:01410` [grounder]  rather than simply scaling supervision our results suggest a shift towards more advanced training methods like reinforcement learning You remember 10 days ago everybody thought about hey yeah supervised fine-tuning plus reinforcement learning and we all read the paper here from DeepSeek where said hey only reinforcement learning for the big model and supervised finetuning and reinforcement learning for the smaller models. So 10 11 days ago this was the
- `78vn6XWvtzI:01590` [grounder]  that I did not really felt at the time. The first one, distilling reasoning data and performance supervised fine-tuning is a deficient way to transfer reasoning abilities. And I thought I don't think so. And I know for sure that in the if you want language model, this is not the case. You know why? Because 10 days later we got the this data experiment.
- `78vn6XWvtzI:01620` [grounder]  Here look black are the distilled version. They outperform the reinforcement learning base and the instruction tuned version. So saying that distilled reasoning data and performance supervised fine tuning is a deficient way. 10 days later it was clear. No this is this is not the correct statement. Now if you say a cross modality with a frozen vision encoder this would be a very interesting discussion if you do not do this anymore

**verdict:** 
**notes:** 

---

## cc-0007
**question id:** cc-0007
**question:** DeepSeek's R1 paper documents GRPO as part of the model's design, while a 14B model's RPT setup also relies on GRPO to update weights every cycle—how does the way GRPO is presented in DeepSeek's writeup differ from its actual role in driving those continuous weight updates during RPT training?
**comparison axis:** how GRPO is described in DeepSeek R1's paper versus how GRPO actually functions in the RPT training loop's weight updates  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.0  final_status=pass

### side A: 2ENvGkkK36E  claim `2ENvGkkK36E#c002`  (support=NO)
**claim:** DeepSeek published a research paper explaining R1 in detail, including the Group Relative Policy Optimization (GRPO) reinforcement learning algorithm.
**claim source chunks:** 2ENvGkkK36E:00000, 2ENvGkkK36E:00030
**grounder chunks:** (none)
**union chunk text:**
- `2ENvGkkK36E:00000` [claim]  hello Community open R1 what is it how can we use it now you know we have DeepSeek R1 download close to 200,000 downloads here for in the last days from Hugging Face we have it available we can use it and you might say what is open R1 now let's open up this video and let's have a deeper look now you know there's a beautiful research paper by DeepSeek explaining here R1 in
- `2ENvGkkK36E:00030` [claim]  detail and we have here the reinforcement learning algorithm we have here the group relative policy optimization described in detail and everything is beautiful but you know then there was this particular spark and in my video that I showed you here and I was talking here about R1 distilled version smaller version not the original huge r one but we have a 32 billion version we have even a 1.5 billion version that is distilled from

### side B: 7ec_0NPxmnA  claim `7ec_0NPxmnA#c035`  (support=YES)
**claim:** The creator argues that the 14B model does learn continuously throughout the RPT optimization process, based on the training loop where a forward pass generates reasoning traces, an automatic verifier compares outputs to ground truth, rewards are assigned, and weights are updated via GRPO (policy gradient algorithm) using backpropagation and an Adam optimizer.
**claim source chunks:** 7ec_0NPxmnA:01620, 7ec_0NPxmnA:01650, 7ec_0NPxmnA:01680, 7ec_0NPxmnA:01710, 7ec_0NPxmnA:01740, 7ec_0NPxmnA:01770, 7ec_0NPxmnA:01800
**grounder chunks:** 7ec_0NPxmnA:01710, 7ec_0NPxmnA:01740, 7ec_0NPxmnA:01770
**union chunk text:**
- `7ec_0NPxmnA:01620` [claim]  I showed you continuous learning is currently not possible this would be a way out of the dilemma. So you can ask hey how did this 14B model learn continuously or did it just apply its static knowledge to do here this new reinforcement pre-training learning and the answer is I think the model learns really continuously throughout the entire opt process why I would argue
- `7ec_0NPxmnA:01650` [claim]  in the following way given we have a specific textual context now this ex up less than t. So our model llm the policy pi data generates now its reasoning pool of g different responses and each each output is now a reasoning trace and a prediction. So this is the pure forward pass through our neural network. At this point no
- `7ec_0NPxmnA:01680` [claim]  learning is happening yet the model is just performing based on what it currently knows. And now the automatic verifier compares now each of the G predictions as I just showed you five minutes ago to the ground truth answer A from the data set from the training data set and if the completion is correct then it's an easy solution because then each of the G reasoning paths is assigned a reward function a reward R as scalar
- `7ec_0NPxmnA:01710` [claim+grounder]  reward in the simplest case it's one for correct and zero for incorrect And using now what we know as a GRPO a policy gradient algorithm our nabla theta theta on j the system calculates how to change the model parameter data our what we are 14 billion free trainable parameter for example and the algorithm's core logic is for the reasoning path that led to a high reward
- `7ec_0NPxmnA:01740` [claim+grounder]  in our reinforcement learning for the pre-training we just adjust here millions of weights it's indicator to make those specific path more likely to happen again in the future because this was a successful path. I want to have this in my memory. I want to have this representation encoded here in my weights and my biases and for all those path here in our J predictions with a chain of sort and a prediction that led to a low reward that was simply incorrect to the golden
- `7ec_0NPxmnA:01770` [claim+grounder]  ground truth by the internet. adjust the weights in data to make this path less likely. We do not want to see this anymore in our neural network. So this adjustment is done using here the standard mechanism of a backprop and a gradient based optimizer like an Adam optimizer. And we achieved what we wanted. We wanted to modify here the tensor weight structure data of our LLM. And now we physically change them. So we did create a new slightly slightly
- `7ec_0NPxmnA:01800` [claim]  smarter model task and the loop starts again with the next one. This is now a complete new view how to do pre-training given the experience we have with reinforcement learning. And I think the question is how far can you go with this? Can you really go infinitely continuous learning with this opt process? I think this is fascinating. Yeah, of course the others

**verdict:** 
**notes:** 

---

## cc-0008
**question id:** cc-0008
**question:** How does Claude 3.7 Sonnet's thinking tool relate to in-context learning compared to how learning happens within CORAL's architecture?
**comparison axis:** how each system's learning mechanism relates to in-context learning (thinking tool vs CORAL's in-context memory accumulation)  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.0  final_status=pass

### side A: 4QnDrX6c96E  claim `4QnDrX6c96E#c008`  (support=NO)
**claim:** In a previous video, the creator showed an optimized prompt example for Claude 3.7 Sonnet and suggested that Anthropic's 'thinking tool' resembles in-context learning.
**claim source chunks:** 4QnDrX6c96E:00150, 4QnDrX6c96E:00180
**grounder chunks:** (none)
**union chunk text:**
- `4QnDrX6c96E:00150` [claim]  particular system message tells me Open AI you highly capable beautiful yes think step by step through complex problems provide clear and accurate answer anticipate helpful followup information and beautiful and I said this does not explain anything of this so what do we have here I have a video on Claude 3.7 Sonnet the sonnet model and I show you here the example of the optimized prompt and I told you that looking here at the
- `4QnDrX6c96E:00180` [claim]  thinking tool example to this looks like an In-context learning now this is just days ago and I told you this I put it here said this is strange that this brings here this massive performance boost that goes beyond 100% Beyond Claude 3.7 extended thinking that I pay more than double so we need a SP of Genius so short question is you shot examples back

### side B: 7n5EVMtYA4I  claim `7n5EVMtYA4I#c022`  (support=YES)
**claim:** Learning in CORAL is entirely contextualized through in-context memory accumulation rather than weight updates.
**claim source chunks:** 7n5EVMtYA4I:00510
**grounder chunks:** 7n5EVMtYA4I:00480, 7n5EVMtYA4I:00510, 7n5EVMtYA4I:01860, 7n5EVMtYA4I:01920
**union chunk text:**
- `7n5EVMtYA4I:00480` [grounder]  artifacts. So again, we are back to a natural human language text-based artifacts. And as I showed you, we have three elements, the attempts, the notes, and the skills. Attempts, hopefully we write in JSON logs, the notes in markdown files, and the skills in reusable code functions with some metadata. data. Just to make sure there's no gradient-based training or fine-tuning in this methodology, eh? And the whole framework operates dynamically, if you
- `7n5EVMtYA4I:00510` [claim+grounder]  want, at test time, not at training time. So, it works at inference. And this is here a gradient-free search algorithm, if you take a step back and say, "What is the main cause of learning?" The learning is entirely contextualized through an in-context memory accumulation. So, around your LLM you have now this hopefully more intelligent file system, where all the multiple agents, four, five, eight agents, write into this file
- `7n5EVMtYA4I:01860` [grounder]  your domain and your complexity level. So there are so many ways to further optimize this. But anyway, I just wanted to show you AI's developing sideways, no? We are not trying to integrate right now our insights then and train our LLM with all this new knowledge. We say, "No. We want to be deterministic. We want to be file based. We want to be easy to debug. We want that everybody can read here our markdown files, our JSON files and
- `7n5EVMtYA4I:01920` [grounder]  institutions globally from Asia to US are now focusing here not to touch the LLM at all, not to modify here the weight tensor structure, not to learn the LLM anything new. Everything is outsourced, but we heavily depend on the syntactic and semantic understanding of AI system to perform this outsourced task to the file system. But hey, this was just my opinion and my

**verdict:** 
**notes:** 

---

## cc-0011
**question id:** cc-0011
**question:** Between the finance study's approach to specializing Seed-OSS 36B and the way DSPy is framed relative to fine-tuning, how does each one's method of customizing model behavior—altering weights versus working through prompts and context—actually play out?
**comparison axis:** how model specialization is achieved (weight modification vs. context/prompt engineering)  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.0  final_status=pass

### side A: -HjPWrKavyA  claim `-HjPWrKavyA#c020`  (support=NO)
**claim:** The authors of the finance study took the Seed-OSS 36B base model and applied fine-tuning and reinforcement learning to create a finance-specialized model.
**claim source chunks:** -HjPWrKavyA:00480, -HjPWrKavyA:00510
**grounder chunks:** (none)
**union chunk text:**
- `-HjPWrKavyA:00480` [claim]  published here you see Apache 2.0 zero on hugging face and they released here a particular model they call it a seed OSS 36B base model and they released this here 2025 here in August 20th and the authors of today's paper took this particular model and said let's do some fine-tuning and reinforcement learning and let's make this open-source model a financial genius interested let's go on
- `-HjPWrKavyA:00510` [claim]  so they built here yuan 4.0 here if I'm not pronouncing this in the correct way I'm sorry and this is the latest flagship here for the financial sector 36 billion dense model initialized from the coss 36B base model but they had a very very specific training exercise so let's have a look this is the main study for today February 25th for financial intelligence and

### side B: 1067jj67toY  claim `1067jj67toY#c057`  (support=YES)
**claim:** The creator positions DSPy as a middle ground between manual prompting and fine-tuning: manual prompting changes only the prompt text; DSPy modifies prompt text via new instructions and few-shot examples through context engineering; fine-tuning modifies the model's weights.
**claim source chunks:** 1067jj67toY:01560, 1067jj67toY:01590
**grounder chunks:** 1067jj67toY:01560, 1067jj67toY:01590, 1067jj67toY:01620, 1067jj67toY:01650
**union chunk text:**
- `1067jj67toY:01560` [claim+grounder]  There other optimizing algorithms that are coordinate prompt optimization. This is all simpler. You just can have a look at it. DSPy is in a beautiful in between of fine-tuning and manual prompting and in context learning. Let's have a look at this. So first line is manual prompting. Second line is DSPy and then we have fine-tuning. So you see with manual prompting what changes here is simply the prompt. No,
- `1067jj67toY:01590` [claim+grounder]  the text of the prompt string itself. Yeah. With DSPy you have context engineering. The text of the prompt is now modified. You get new instruction and few short examples. Just do this here with a JSON format in the output for in the output and few short example that are really specific to your task. No. Or you say refine tuning. You know, I really want that the model learns this and really modifies here its weight so that it's really a
- `1067jj67toY:01620` [grounder]  permanent experience that the model learned. You modify the weights in the language model itself if you do a fine tuning cost and speed for the manual prompting but a human fast to iterate brittle and labor intensive to get it right even if you're an expert you have to try it out simple or you have the experience the knowledge no DSPy optimization it's a low cost I don't know if you have a few hundred LLM calls only if you have open source no if you go with the real proprietary model like o3 pro it can become
- `1067jj67toY:01650` [grounder]  expensive real fast. So it's fast. Yeah. But machine optimized. No. And you just need here a small labeled data set depending on the complexity of your task between one 10 or 200 examples that you where you define this is what I want the machine does. Yeah. And for fine-tuning you need thousands of examples. Now it's really much more detailed. We have beautiful documentation. Stanford NLP DSPy version three. Here I

**verdict:** 
**notes:** 

---

## cc-0012
**question id:** cc-0012
**question:** How does MiroFlow's design as a dedicated open-source agent framework for deep research compare to OpenAI's o3-full model's approach when used directly to carry out a deep research task?
**comparison axis:** design/approach to performing deep research tasks (dedicated agent framework vs. direct model use)  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.136  final_status=pass

### side A: 4jwLkVMrdhQ  claim `4jwLkVMrdhQ#c011`  (support=YES)
**claim:** MiroFlow is an open-source agent framework focused on the deep research task, and the current version is version three, built over more than a year of development.
**claim source chunks:** 4jwLkVMrdhQ:00240
**grounder chunks:** 4jwLkVMrdhQ:00240, 4jwLkVMrdhQ:00270
**union chunk text:**
- `4jwLkVMrdhQ:00240` [claim+grounder]  itself as a node in a graph and there's some absolute fascinating new developments happening. This is now the second paper by Tsinghua University and they go for open source agent framework for particular task a deep research task here you have of course all the GitHub please notice yeah by the way this is here they have other mods so this is really something that's going on for more than a year so this is version three if I'm correct so if you
- `4jwLkVMrdhQ:00270` [grounder]  want to read the other paper you find it of course here in the references you see does it really work. Absolutely. They have here this MiroFlow now compared for the GAIA validation benchmark. They compared with Manus with OpenAI deep research and you see here this solid dark blue is really outperforming everything else in deep research task. Great. You find here a complete um description here in the paper. But I want to focus here today with you only

### side B: NaeeCTutYEY  claim `NaeeCTutYEY#c003`  (support=NO)
**claim:** The creator used OpenAI's o3-full model to perform a deep research task on reinforcement fine-tuning, which took 17 minutes and consulted 28 internet sources.
**claim source chunks:** NaeeCTutYEY:00120, NaeeCTutYEY:00150
**grounder chunks:** (none)
**union chunk text:**
- `NaeeCTutYEY:00120` [claim]  pay. So, I didn't have access to the reinforcement fine-tuning. And I understand that this is here a proprietary a a closed thing here from OpenAI but now today today was the time I said hey now I'm going to break free I open this box of Pandora I want to know what is reinforcement fine-tuning so I went to OpenAI to GPT-03 the full one and I did a deep research and after 17 minutes and after having access to 28
- `NaeeCTutYEY:00150` [claim]  sources you know and I want to stress as 28 internet sources 03 came back with a beautiful deep research and look here at all their explanation. This is a screenshot here and you know what there's hardly any information because it is often used as a reward model but instead of seeing the correct answer the model only gets a score or reward and must adjust its policy but give me

**verdict:** 
**notes:** 

---

## cc-0014
**question id:** cc-0014
**question:** For a 235-billion-parameter mixture-of-experts model that exposes a thinking-mode slider for capping reasoning length, how does that reasoning-control mechanism stack up against how Self-MoE reorganizes a single monolithic LLM into a set of specialized expert sub-models?
**comparison axis:** how thinking-mode/reasoning-control design compares to Self-MoE's expert-composition approach  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=pass

### side A: 1igqokIKJvg  claim `1igqokIKJvg#c045`  (support=YES)
**claim:** The creator references a mixture-of-experts model with 235 billion total parameters and 22 billion active parameters that has a thinking mode with a slider to control maximum thinking length, shown in a previous video about the o3 model.
**claim source chunks:** 1igqokIKJvg:00900, 1igqokIKJvg:00930
**grounder chunks:** 1igqokIKJvg:00900, 1igqokIKJvg:00930
**union chunk text:**
- `1igqokIKJvg:00900` [claim+grounder]  is here o3 achieves here a 3% success rate. So I think yeah, beautiful. We have a new hard benchmark. So this will be amazing. So we will see now here have a look at this publication. I cannot go into the details but have a look at it. I love it. But we know this I showed you in my video about the new o3 model. Now if we had a look at the mixture of expert model with 235 billion free trainable parameter with active 22
- `1igqokIKJvg:00930` [claim+grounder]  billion free trainable parameter. I told you we have this thinking mode and here we have a slider and we can control the maximum length of thinking. This is more or less if you want our token length that we want to pay for. So you have a thinking budget and you have this entity and it's in US dollars and you see you can move it around and I have for example 21K token thinking is really great. So if you want a budget and you want to say

### side B: 9NcVpt5tpxs  claim `9NcVpt5tpxs#c003`  (support=NO)
**claim:** Self-MoE transforms a monolithic LLM into a compositional system of specialized expert models.
**claim source chunks:** 9NcVpt5tpxs:00030, 9NcVpt5tpxs:00060
**grounder chunks:** (none)
**union chunk text:**
- `9NcVpt5tpxs:00030` [claim]  and let's have a look that you have to read this paper first because I was stuck with the original paper so I went here and remember here from Georgia Tech MIT IBM MIT October 7 2024 self mixture of expert system two words here a compositional large language model with some selfs specialized expert system so we transform now a monolitic llm into a compositional model system of experts
- `9NcVpt5tpxs:00060` [claim]  specialized experts and you might ask why well this is the beauty because then we will pick some of those experts specialized expert from our llm and we will magnify them we will give them more power so we will have a different specialization pattern emerging in our monolithic llm so if you have read the two paper great let's define what is a self adaptive llm meaning this is even more

**verdict:** 
**notes:** 

---

## cc-0015
**question id:** cc-0015
**question:** For controlling and customizing behavior in a mixture-of-experts setup, how does the approach used by that 235B/22B-parameter thinking-mode model—with its slider for capping reasoning length—compare to what's being proposed for Llama 4 Maverick's 128 experts in terms of tailoring critique sets to each expert?
**comparison axis:** approach to controlling/customizing behavior in a mixture-of-experts model  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.033  final_status=pass

### side A: 1igqokIKJvg  claim `1igqokIKJvg#c045`  (support=NO)
**claim:** The creator references a mixture-of-experts model with 235 billion total parameters and 22 billion active parameters that has a thinking mode with a slider to control maximum thinking length, shown in a previous video about the o3 model.
**claim source chunks:** 1igqokIKJvg:00900, 1igqokIKJvg:00930
**grounder chunks:** (none)
**union chunk text:**
- `1igqokIKJvg:00900` [claim]  is here o3 achieves here a 3% success rate. So I think yeah, beautiful. We have a new hard benchmark. So this will be amazing. So we will see now here have a look at this publication. I cannot go into the details but have a look at it. I love it. But we know this I showed you in my video about the new o3 model. Now if we had a look at the mixture of expert model with 235 billion free trainable parameter with active 22
- `1igqokIKJvg:00930` [claim]  billion free trainable parameter. I told you we have this thinking mode and here we have a slider and we can control the maximum length of thinking. This is more or less if you want our token length that we want to pay for. So you have a thinking budget and you have this entity and it's in US dollars and you see you can move it around and I have for example 21K token thinking is really great. So if you want a budget and you want to say

### side B: 9KMxNZ2CvUg  claim `9KMxNZ2CvUg#c039`  (support=YES)
**claim:** The creator speculates that Llama 4 Maverick, a 400 billion parameter mixture-of-experts model with 128 experts, could benefit from a similar approach of handcrafted principled critique sets tailored to each of its 128 experts.
**claim source chunks:** 9KMxNZ2CvUg:00750, 9KMxNZ2CvUg:00780, 9KMxNZ2CvUg:00810, 9KMxNZ2CvUg:00840
**grounder chunks:** 9KMxNZ2CvUg:00750, 9KMxNZ2CvUg:00780, 9KMxNZ2CvUg:00810
**union chunk text:**
- `9KMxNZ2CvUg:00750` [claim+grounder]  space and the critique has now this opportunity to search in all the gradients of this search space and not lose some of these spaces. Now you know I thought when I did my video on Llama 4 the Maverick the 400 billion model and especially it's a mixture of expert and we have 128 experts and I thought you know this would be an opportunity for Llama I didn't know if they would take here this
- `9KMxNZ2CvUg:00780` [claim+grounder]  new idea from DeepSeek that was just published two days ago by DeepSeek this golden set this this perfect set of principled critique and they are now handcrafted that hand-designed for each of those 128 experts in their specific expert domain. This would really provide here I think a reason a performance jump because now let's say one of those 128
- `9KMxNZ2CvUg:00810` [claim+grounder]  experts is an expert in mathematics. One expert is an expert in financial mathematics and financial the next one is an expert in physics in medicine and biopharma. You get the idea. If you would provide them a starting set with the best principles and the best critique behavior for those principles, I think you could really make sense that you have so many experts here in this new Llama for Maverick. It's a 400 billion
- `9KMxNZ2CvUg:00840` [claim]  free trainable parameter model. So here you really would have the opportunity to further optimize or at least optimize the initial condition for the inference time scaling. Okay, let's come here to the core element. This shift now enables here the principle to be generated based on the input of the user query. So if I have a mathematical query here, the principles will be based here on

**verdict:** 
**notes:** 

---

## cc-0018
**question id:** cc-0018
**question:** For someone comparing reasoning transparency across models, how does Claude 3.7 Sonnet's handling of chain-of-thought visibility to the end user stack up against what QwQ 32B does when it comes to exposing its own reasoning trace?
**comparison axis:** visibility/transparency of chain-of-thought reasoning to users  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.083  final_status=pass

### side A: 12lAM-xPvu8  claim `12lAM-xPvu8#c005`  (support=YES)
**claim:** The creator states that with Claude 3.7 Sonnet, users are not allowed to see the real thinking process or chain of thought.
**claim source chunks:** 12lAM-xPvu8:00060
**grounder chunks:** 12lAM-xPvu8:00060
**union chunk text:**
- `12lAM-xPvu8:00060` [claim+grounder]  yes Claude 3.7 Sonnet. Now we know with sonnet we are not allowed to see the real thinking process the chain of thought thinking. So therefore, as I showed you in my last video, we do not miss a lot of, but as I showed you here by the latest publication on Anthropic, the chain of thought reasoning that Claude 3.7 shows us is not the real thing, is not a real thinking process and can be very easily disturbed

### side B: 14yPeonB2P4  claim `14yPeonB2P4#c001`  (support=NO)
**claim:** QwQ 32B is a reasoning system that prints out each and every single thought of the machine explicitly.
**claim source chunks:** 14yPeonB2P4:00000
**grounder chunks:** (none)
**union chunk text:**
- `14yPeonB2P4:00000` [claim]  [Music] hello Community hello hello Community great that you are back and you might ask hey are you sure topological AI systems are we ready for that yes we are so let's start and if you are subscribe of this channel you know that in my last video where we looked at the explicit reasoning process and qwq 32B is a beautiful system because it really prints out each and every single thought of the machine

**verdict:** 
**notes:** 

---

## cc-0019
**question id:** cc-0019
**question:** When people talk about visibility into a model's reasoning, how does the restriction on seeing Claude 3.7 Sonnet's actual chain of thought compare to the kinds of structural patterns—like chain of thought, tree of thought, and graph of thought—that researchers have identified within o1 and o3's reasoning traces?
**comparison axis:** visibility/accessibility of reasoning process vs. structural patterns of reasoning  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.059  final_status=pass

### side A: 12lAM-xPvu8  claim `12lAM-xPvu8#c005`  (support=YES)
**claim:** The creator states that with Claude 3.7 Sonnet, users are not allowed to see the real thinking process or chain of thought.
**claim source chunks:** 12lAM-xPvu8:00060
**grounder chunks:** 12lAM-xPvu8:00060
**union chunk text:**
- `12lAM-xPvu8:00060` [claim+grounder]  yes Claude 3.7 Sonnet. Now we know with sonnet we are not allowed to see the real thinking process the chain of thought thinking. So therefore, as I showed you in my last video, we do not miss a lot of, but as I showed you here by the latest publication on Anthropic, the chain of thought reasoning that Claude 3.7 shows us is not the real thing, is not a real thinking process and can be very easily disturbed

### side B: 14yPeonB2P4  claim `14yPeonB2P4#c004`  (support=NO)
**claim:** Chain of thought, tree of thought, and graph of thought structures were discovered in the reasoning process/answer structure of o1 and o3 models.
**claim source chunks:** 14yPeonB2P4:00090
**grounder chunks:** (none)
**union chunk text:**
- `14yPeonB2P4:00090` [claim]  topology for the right task so easiest way is now we have the chain of thought the tree of thought and the graph of thought that we discovered here in the answer structure here in the reasoning process of o1 o3 B so instead of relying on simple linear chain of thought you know from the very old models o1 or o3 let's have a look at the latest reasoning models and in this video I told you here by Princeton University if we go beyond chain of thought

**verdict:** 
**notes:** 

---

## cc-0021
**question id:** cc-0021
**question:** When you look at the Xiaomi research's dual-adapter setup for its world model versus how the web world model paper structures its own architecture, how does each one divide up the functional pieces handling physics versus the other components?
**comparison axis:** how each world model architecture divides functional components (e.g., geometry/imagination) from physics handling  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=pass

### side A: -hFJe5hXWps  claim `-hFJe5hXWps#c012`  (support=YES)
**claim:** In that Xiaomi research, two dynamic adapters were used: one adapter for geometry and one adapter for the world model handling physics.
**claim source chunks:** -hFJe5hXWps:00151
**grounder chunks:** -hFJe5hXWps:00151, -hFJe5hXWps:00181, -hFJe5hXWps:00211
**union chunk text:**
- `-hFJe5hXWps:00151` [claim+grounder]  was new self-driving AI explained here a vision language action model on the Plus integrating a world model here for Xiaomi electric vehicles. They used in their latest research here as I told you two dynamic adapters. One adapter was here for the geometry and one adapter was for the world model for the physics. And now for the geometry adapter. And you remember they also used here V GGGD but this changes today because now we
- `-hFJe5hXWps:00181` [grounder]  don't have to go quadratic complexity. Now we have a new option and you remember in this video I showed you a study published by Google and Purdue University on March 1st 2026 and they characterized the vision language action models here on edge AI architecture like in cars and they said you know we look at Nvidia Orin and to this is our Blackwell and they said hm we have a bottleneck it is not fast enough because 75% of end to end latency
- `-hFJe5hXWps:00211` [grounder]  is consumed by action generation phase So if they run here a 7B model and this is I mean Google so they do have the computer resources they have not the best model because they say for a general purpose utility in a complex real world environment our models should have 10 to 100 billion free trainable parameter but this is not working here on the current Nvidia infrastructure Nvidia is too slow. So

### side B: 388I4ugcf-0  claim `388I4ugcf-0#c001`  (support=NO)
**claim:** The paper introduces a 'web world model' that separates physics from imagination/generation.
**claim source chunks:** 388I4ugcf-0:00000, 388I4ugcf-0:00120, 388I4ugcf-0:00150, 388I4ugcf-0:00180
**grounder chunks:** (none)
**union chunk text:**
- `388I4ugcf-0:00000` [claim]  Hello communities, so great that you are back. Yes, today we talk about a new form of world model, the web world model. And as you can see, we will separate here the physics from the imagination. Welcome to my channel Discovery. We have a look at the latest AI research paper. And yeah, they built here a galaxy travel atlas. This is here sci-fi simulation where we do have real physics algorithm that dictate here the layout of galaxies of stars, planetary clusters. And then the LLM textures here this geometry with mission
- `388I4ugcf-0:00120` [claim]  this the next day. So tomorrow maybe you already have all the information. Now what is the idea? The idea is we have a web framework. Yeah, where we have text code based environment controllability beautiful and on the other side we have the full defined world model with an almost unlimited context and now they say let's build something in the middle let's build something where the framework set the rules and the LLMs just fill in the content so you see the LLM is not the mastermind it's not this
- `388I4ugcf-0:00150` [claim]  AGI but we have a framework physics if you want state transition between physical systems that set the rules that set the dynamic what is possible what moves you can do in this environment and then the LLM is just giving you the story the narration and this is here a much more powerful model because the AI does not have to do all the syncing so we have here with this web world model unlimited context text code based environment controllability beautiful
- `388I4ugcf-0:00180` [claim]  the best of both worlds this is yet a publication as I already showed here published December 29, 2025. A new web world model, a middle ground world of world state and the physics are implemented in ordinary web code to ensure a logical consistency of both worlds if you want while the LLMs generate only quotation mark the context, the narratives and the high-level decision on top of this structured

**verdict:** 
**notes:** 

---

## cc-0031
**question id:** cc-0031
**question:** How does Yuan 4.0's continual pre-training strategy for absorbing new financial knowledge without losing its reasoning ability compare to the training-loop technique DEEPSEARCH uses to broaden the range of reasoning paths it explores?
**comparison axis:** training-loop techniques for managing knowledge/reasoning during training (KL divergence self-regularization vs MCTS injection)  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=pass

### side A: -HjPWrKavyA  claim `-HjPWrKavyA#c036`  (support=YES)
**claim:** Yuan 4.0's training used continual pre-training (CPT) with a Kullback-Leibler divergence self-regularization objective against a reference model to prevent catastrophic forgetting of base mathematical reasoning while infusing new financial data.
**claim source chunks:** -HjPWrKavyA:00870, -HjPWrKavyA:00900
**grounder chunks:** -HjPWrKavyA:00900, -HjPWrKavyA:01410, -HjPWrKavyA:01650, -HjPWrKavyA:01890
**union chunk text:**
- `-HjPWrKavyA:00870` [claim]  decided now to develop now their own finance agent. Yeah. And they called it 4.0. You have guessed there are some other models before and this is just a 36 billion free trainable parameter model. So this you can run locally if you invest some thousands here for a unified memory for Mac or whatever. Now this model they trained in a very particular way that seems similar. Yeah, we have a continual pre-training of GPT.
- `-HjPWrKavyA:00900` [claim+grounder]  They use our classical Kullback-Leibler divergence for the self-regularization objective against a reference model during CPT and this limits the gradient updates to prevent catastrophic forgetting of everything that we learn from base mathematical reasoning while infusing here this new dense financial data. You notice here we have a reference model our cookbook library and then we have reinforcement learning here with DPO and I say this is great fine
- `-HjPWrKavyA:01410` [grounder]  the conclusion from the finish creating a dense multi-step trajectory from end to start. If we have this now after supervised fine tuning they now apply reinforcement learning but they could not go with a standard DPO because this would penalize the model for straying too far from supervised fine tuning policy and often include length penalties. No, now this is not what we want. Remember I also told you we want to have um escape here from the outcome reward functions
- `-HjPWrKavyA:01650` [grounder]  highly professional absolutely convincing but lead to complete nonsense. So therefore now the second step here of this if you want 32 billion model that um kind of simulates you the human reasoning aspect here we have to have a modified dapo and the modified dapo is simple the order remove the KL divergences and the length penalty and if you think
- `-HjPWrKavyA:01890` [grounder]  risks here the severe overoptimization and a model stripped of a Kullback-Leibler regularization is prone to catastrophic exploitation of its own reward function. Yes, we know but it shows you if you choose it in an intelligent way and you are careful you can at least outperform our big proprietary models. And this is here an absolutely fascinating insight. Imagine if we would be now constructing a discrete topological graph structure. This would be a mathematical procedure

### side B: ARst0nlEgO4  claim `ARst0nlEgO4#c014`  (support=NO)
**claim:** DEEPSEARCH's solution is to directly inject Monte Carlo tree search into the training loop, forcing the model to systematically map out a wider portion of the solution space via branching, exposing it to correct, incorrect, and partial reasoning paths.
**claim source chunks:** ARst0nlEgO4:00300, ARst0nlEgO4:00330
**grounder chunks:** (none)
**union chunk text:**
- `ARst0nlEgO4:00300` [claim]  problem but it fails to master the complete long horizon decision-making so let's solve this now and the idea here by Stanford is okay we take our good friend Monte Carlo search and directly inject it into the training loop and we just force the model to systematically map out a wider portion of the solution space because yes we have a tree and the tree is branching out so we don't collapse automatically here to an entropy trace exposes the model to a vast array of
- `ARst0nlEgO4:00330` [claim]  correct and also we have to learn also the incorrect one and partial reasoning but everything we want to discover the whole solution space we want to learn this is the main topic here no mic reward back propagation provides you the fine grade credit assignments we have a dozen videos on this and yes what a coincidence and here we have the direct connection to my last video directly rewarded with a higher Q value you remember in my last video we are talking about the solution to the plateauing is exactly here the Q

**verdict:** 
**notes:** 

---

## cc-0032
**question id:** cc-0032
**question:** How does the benchmark score gap between the Llama 13B teacher and its distilled Llama 7B student on ALFWorld and Hotpot compare to the score gap between the Light-R1 32B model and the official DeepSeek R1 distilled 32B model?
**comparison axis:** performance gap between teacher/larger model and distilled/smaller student model  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=pass

### side A: -OzH4buQzTM  claim `-OzH4buQzTM#c021`  (support=YES)
**claim:** With a Llama 13B model as the teacher, the teacher achieved a task success score of 75 on one benchmark and 71 on another, while a distilled Llama 7B student achieved 68 and 61 respectively on those benchmarks (ALFWorld and Hotpot).
**claim source chunks:** -OzH4buQzTM:00450, -OzH4buQzTM:00480
**grounder chunks:** -OzH4buQzTM:00480, -OzH4buQzTM:00510, -OzH4buQzTM:00540
**union chunk text:**
- `-OzH4buQzTM:00450` [claim]  style. Great. If you want to see a detailed explanation here of the definition of those parameters here it is. But I'll say we go now and we have a look at the results. So here we are. Now let's look here at the last one. When the teacher model is here a llama model a 13 billion free trainable parameter model. And here you have this one two three benchmarks. And here in this benchmark you see now here from ALFWorld and Hotpot you see now the
- `-OzH4buQzTM:00480` [claim+grounder]  parameter the task success the reasoning length the chain of sort matching and the latency as I told you so let's have a look so here's our teacher beautiful so we have I don't know 75 and then say if we do now a llama 7B and we do all the specific imitation learning from this teacher from 13b the student the 7B now comes is close to the teacher. Teacher has 75 and the student has 68. Teacher has 71. The student has 61. And yes, you can
- `-OzH4buQzTM:00510` [grounder]  see it especially the chain of thought matching quality. Of course, the teacher is defined here as 100%. But I would say 77% is not that famous. 72%. Okay. And yeah, and I mean their main argument is not about how close can the student become the teacher, but their main argument, hey, what about we take here a vanilla llama 7B? We do not
- `-OzH4buQzTM:00540` [grounder]  optimize it for imitation learning. Well, yes, of course. Then instead of 68, we only have a 64% performance here on AlfWorld, for example. But yeah, so they argue now as you see here in Boldface that if you take only the Llama 7B and now compared to their Llama 7B distilled version that it is better overall. Okay, beautiful. But maybe a little tiny bit

### side B: FAg4v2xaLYc  claim `FAg4v2xaLYc#c026`  (support=NO)
**claim:** The new Light-R1 32B model, released beginning of March 2025, achieved a performance score of 76.6, surpassing the official DeepSeek R1 distilled 32B's 72.6.
**claim source chunks:** FAg4v2xaLYc:00540
**grounder chunks:** (none)
**union chunk text:**
- `FAg4v2xaLYc:00540` [claim]  Light-R1 32B but I'm going to show you in a minute this is now here the beginning of March 2025 has a performance of 76.6 so we not even come close but we so Close here to official DeepSeek variant is still from January so with less than two months we have now that we can build something that is even better than the original DeepSeek R1 32B isn't this

**verdict:** 
**notes:** 

---

## cc-0033
**question id:** cc-0033
**question:** How does the performance gap between the Llama 13B teacher and its distilled Llama 7B student on ALFWorld and Hotpot compare to the performance jump observed between the Light-R1 14B and 32B models?
**comparison axis:** performance gap/jump from model size scaling (teacher-student distillation vs model size increase)  (both_sides_required=True)
**advisory:** side_support(A/B)=Y/N  both_side_grounded=False  leak=0.0  final_status=pass

### side A: -OzH4buQzTM  claim `-OzH4buQzTM#c021`  (support=YES)
**claim:** With a Llama 13B model as the teacher, the teacher achieved a task success score of 75 on one benchmark and 71 on another, while a distilled Llama 7B student achieved 68 and 61 respectively on those benchmarks (ALFWorld and Hotpot).
**claim source chunks:** -OzH4buQzTM:00450, -OzH4buQzTM:00480
**grounder chunks:** -OzH4buQzTM:00480, -OzH4buQzTM:00510
**union chunk text:**
- `-OzH4buQzTM:00450` [claim]  style. Great. If you want to see a detailed explanation here of the definition of those parameters here it is. But I'll say we go now and we have a look at the results. So here we are. Now let's look here at the last one. When the teacher model is here a llama model a 13 billion free trainable parameter model. And here you have this one two three benchmarks. And here in this benchmark you see now here from ALFWorld and Hotpot you see now the
- `-OzH4buQzTM:00480` [claim+grounder]  parameter the task success the reasoning length the chain of sort matching and the latency as I told you so let's have a look so here's our teacher beautiful so we have I don't know 75 and then say if we do now a llama 7B and we do all the specific imitation learning from this teacher from 13b the student the 7B now comes is close to the teacher. Teacher has 75 and the student has 68. Teacher has 71. The student has 61. And yes, you can
- `-OzH4buQzTM:00510` [grounder]  see it especially the chain of thought matching quality. Of course, the teacher is defined here as 100%. But I would say 77% is not that famous. 72%. Okay. And yeah, and I mean their main argument is not about how close can the student become the teacher, but their main argument, hey, what about we take here a vanilla llama 7B? We do not

### side B: FAg4v2xaLYc  claim `FAg4v2xaLYc#c035`  (support=NO)
**claim:** Comparing the 14B and 32B Light-R1 models, performance goes from 60% to 64.6%, a smaller jump than the previous size increase, indicating room for improvement.
**claim source chunks:** FAg4v2xaLYc:00750
**grounder chunks:** (none)
**union chunk text:**
- `FAg4v2xaLYc:00750` [claim]  and if you want to compare the 14B to the 32B you see yeah it's it's not that it again doubles into performance in the next jump but it goes from 60 to 64.6% so interesting there's room for improvement but let's stay with this particular study today so they say here hey our little Light-R1 becomes really a mathematical wizard even outperforming some of the giant AI models and especially here the smaller 14B model

**verdict:** 
**notes:** 

---

## cc-0035
**question id:** cc-0035
**question:** When judging output quality, how does the way SoT's results get benchmarked against traditional chain-of-thought prompting differ from the approach of using GPT-4 as a stand-in judge to score creative writing on coherence, creativity, and adherence to source terms?
**comparison axis:** methods used to evaluate SoT outputs (direct comparison vs. LLM-as-judge)  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.074  final_status=pass

### side A: -JiUyJVPM3Q  claim `-JiUyJVPM3Q#c033`  (support=NO)
**claim:** The results of SoT were compared against traditional chain-of-thought prompting.
**claim source chunks:** -JiUyJVPM3Q:00780
**grounder chunks:** (none)
**union chunk text:**
- `-JiUyJVPM3Q:00780` [claim]  just check for self-consistency you know what self-consistency is we have some cases we want to do this three different reasoning paths for generated multiple polls for generating and then we let the AI system itself vote we have different voting systems let's go with the easiest one a majority voting system to say hey of those multiple answers what do you think AI is the best answer given then we have the final answer and then the results are compared simply against a traditional chain of Thought prompting and

### side B: 3tiAvRcviiY  claim `3tiAvRcviiY#c067`  (support=YES)
**claim:** For creative writing tasks, evaluation becomes more subjective, requiring a strong LLM like GPT-4 to act as a proxy for human critique, rating coherence, creativity, and adherence to source terms on a scale of 1 to 10.
**claim source chunks:** 3tiAvRcviiY:02340, 3tiAvRcviiY:02370, 3tiAvRcviiY:02400
**grounder chunks:** 3tiAvRcviiY:02310, 3tiAvRcviiY:02340, 3tiAvRcviiY:02370, 3tiAvRcviiY:02400
**union chunk text:**
- `3tiAvRcviiY:02310` [grounder]  Yeah, this is open to interpretation. No, no, no. We have an objective function. we evaluate the result. So we have different task but let's go with a travel planner that's easy no with a judge is a deterministic rule-based Python script and it simply checks against the list of my rules and if I define my query I say hey on Monday I want to start in San Francisco on Tuesday I want to be in New York for a stepover I want to be there for I don't
- `3tiAvRcviiY:02340` [claim+grounder]  know 18 hours I have a budget for a hotel of $20 and then I want to go three days to I don't know Madrid and then I want to go 4 days and visit my aunt in Rome and then I want to take the boat to go back to I don't know rules simple rules budget check Monday in San Francisco check Tuesday in New York check simple you have scores you can go with a scale one to five you can aggregate the scores
- `3tiAvRcviiY:02370` [claim+grounder]  beautiful or other constraint super for some creative writing task it becomes much more wobbling. No. So what do you need? You need a better AI system like GPT-4. This acts like a proxy for a human critique. No, this will understand if I'm here very emotional maybe or creative writing or whatever. But it's also depending here on the pre-training data. No. And
- `3tiAvRcviiY:02400` [claim+grounder]  then for me it's easy. say to the LLM, hey, please write or rate the story's coherence, the story creativity and the adherence to the source terms on a scale of 1 to 10. So this is easy, no, but this is highly subjective here to the quality and the experience and the training and the domain specificity of the LLM. If it's all language-based, language is not like a theoretical physics

**verdict:** 
**notes:** 

---

## cc-0038
**question id:** cc-0038
**question:** How does the approach of converting natural language premises into first-order logic notation compare to the hierarchical reasoning model's (HRM) use of structured latent-space operations for handling multi-step reasoning tasks?
**comparison axis:** how each approach handles multi-step reasoning (symbolic FOL conversion vs. structured latent-space operations)  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.045  final_status=pass

### side A: -JiUyJVPM3Q  claim `-JiUyJVPM3Q#c014`  (support=NO)
**claim:** The creator references another prior video called 'The AI Reasoning Lie' in which natural language premises were converted into first-order logic notation.
**claim source chunks:** -JiUyJVPM3Q:00270
**grounder chunks:** (none)
**union chunk text:**
- `-JiUyJVPM3Q:00270` [claim]  as I instructed them so we went from a human task description to a mathematical logic notation and you know mathematics is code and then this mathematical logic was coded in Python also another video here the video was called the AI reasoning lie where I showed you here if you have premises that are formulated in our natural human English then we have here and I showed you exactly how to do this here first

### side B: N_MhjTkWg54  claim `N_MhjTkWg54#c036`  (support=YES)
**claim:** The creator previously covered a hierarchical reasoning model (HRM) video two days earlier, in which the model authors claimed spectacular performance on tasks requiring multi-step reasoning via powerful, structured, algorithmically effective latent-space operations.
**claim source chunks:** N_MhjTkWg54:01140, N_MhjTkWg54:01170
**grounder chunks:** N_MhjTkWg54:01140, N_MhjTkWg54:01170, N_MhjTkWg54:01200, N_MhjTkWg54:01230, N_MhjTkWg54:01260, N_MhjTkWg54:01290, N_MhjTkWg54:01320, N_MhjTkWg54:01350, N_MhjTkWg54:01380, N_MhjTkWg54:01410
**union chunk text:**
- `N_MhjTkWg54:01140` [claim+grounder]  anything that comes close to a logical chain. And you might say, "But wait, wait a minute. No, two days ago you showed us here a new AI model about hierarchical reasoning. And there we also used here a recurrent model." And you were absolutely right if you are a subscriber of my channel. And at that time I told you here that the authors said our model achieves a spectacular performance on tasks that require multi-step reasoning. The operation happening in its latent space. So we are
- `N_MhjTkWg54:01170` [claim+grounder]  again operating here in the vector space must be powerful structured and algorithmically effective. And in this video I showed you a result that was just amazing. And now now we have nothing. So what is the difference? Have you spotted it already? Do you know it? Well, it's very easy. Remember that here in this particular case of hierarchical reasoning models, we were operating in
- `N_MhjTkWg54:01200` [grounder]  transformer blocks that were encoder only blocks like using here bidirectional self attention. So each token can look at all the other tokens in the sequence before and after itself. Great for understanding here the full context today in the Huginn-3.5B in the depth recurrent transformer. So both are recurrent systems just to be clear. But today we looked at the decoder only blocks like in GPT or llama that use your causal self attention or masked self attention and each token can only look
- `N_MhjTkWg54:01230` [grounder]  at itself and the token that came before it. So this is an autoregressive text generation that we know from GPT. And this is the first of the differences. We have not a transformer block because a transformer block if you have the encoder block is totally different in its operation to the decoder block. Remember this is BERT and this is GPT. So careful if you read transformer block you have to specify which kind of it is it
- `N_MhjTkWg54:01260` [grounder]  and because we have bidirectional attention these HRM encoder blocks are perfectly suited for all at once reasoning. Remember we were doing here what was it Sudoku and chess. So we have complete configuration with one view. We see the here the complete chess board and we have a complete understanding of the system here on hugging decoder blocks. We only have a left to right generation. We have an autoregressive token generation.
- `N_MhjTkWg54:01290` [grounder]  Yeah. So extremely limited. But I want to be clear. The hugging paper does not invalidate the HRM paper. Well, it's quite the opposite. No, it provides you a beautiful piece of context that makes the result of HRM even more impressive. But if you go back to my video, you see they built a much more complicated architecture because the hugging paper just shows
- `N_MhjTkWg54:01320` [grounder]  that simple generic recurrence is not enough. There's nothing on space spatial separation or temporal separation. This is just looping over transformer layers over and over again. You just get messy states and a weak performance if you just do the trivial the the of course we do this thing. But where on the other hand HRM succeeds is it has special features. And remember three points I told you we have
- `N_MhjTkWg54:01350` [grounder]  with a high and a low system operating within HRM. We have a hierarchical separation plus we have a temporal separation like this slow fast update like this syncing one and syncing two for the humans. And then I specified here the deep supervision training strategy for this particular configuration. So it really pays if you are both on a recurrent system but you really think
- `N_MhjTkWg54:01380` [grounder]  about how the learning process should happen, how the reasoning process should happen and how you build your training strategy. If you just take here a transformer block or transformer layers here and you just have a recurrency that you run over it without anything else, weak performance. But I think together and this is why I show you this study today. Together those two papers tell a complete
- `N_MhjTkWg54:01410` [grounder]  story. Huh? Because achieving here a powerful latent reasoning in calculated in our mathematical vector space here after transformer blocks is not easy and it requires here highly specialized sophisticated architecture like I've shown you in my HRM video and not just the simple application of recurrence like we saw on today's paper. So this Huginn paper provides you the baseline if you want to demonstrate what is not

**verdict:** 
**notes:** 

---

## cc-0022
**question id:** cc-0022
**question:** What's the reasoning behind calling something 'context engineering' as opposed to prior terminology, and how does that compare to the logic that led to naming a training process rejective fine-tuning (RFT) rather than reinforcement fine-tuning?
**comparison axis:** reasoning behind terminology choices (naming rationale) for two unrelated terms  (both_sides_required=True)
**advisory:** side_support(A/B)=N/Y  both_side_grounded=False  leak=0.091  final_status=two_factuals

### side A: 1067jj67toY  claim `1067jj67toY#c002`  (support=NO)
**claim:** The creator characterizes 'context engineering' as marketing slang for what was previously called prompt engineering.
**claim source chunks:** 1067jj67toY:00030
**grounder chunks:** (none)
**union chunk text:**
- `1067jj67toY:00030` [claim]  context engineering if you prefer here the more marketing slang. So let's have a look context engineering with DSPy. You have more or less just two things that you do. You have DSP programming. What does it mean? It simply means you write a high-level pipeline in Python using here specific modules in DSPy that are given to you. And then you have an optimizer. This is a compiler. That's all you do. It's an optimizer that runs on your high

### side B: 9KMxNZ2CvUg  claim `9KMxNZ2CvUg#c029`  (support=YES)
**claim:** During the critique step in training, votes are extracted and incorrect or too-easy answers are rejected, which is why the process is called rejective fine-tuning (RFT), not reinforcement fine-tuning.
**claim source chunks:** 9KMxNZ2CvUg:00480, 9KMxNZ2CvUg:00960
**grounder chunks:** 9KMxNZ2CvUg:00480
**union chunk text:**
- `9KMxNZ2CvUg:00480` [claim+grounder]  do this those are your principle that I wanted you have in your evaluation report then here the critique is here okay given the principle I vote here for this and this and this then you extract the votes what is incorrect or what is too easy you just forget about it you reject it this is why it's called rejective fine-tuning so RF is not reinforcement fine-tuning but rejective finetuning and then you build your data set for the
- `9KMxNZ2CvUg:00960` [claim]  domain, let's say this is an AI for a hospital, you don't need to train it on I don't know English poetry or how to cook a salad. No, you are only in medicine. So this reward model just focusing on medicine can have so much more deeper understanding than a general model. Yeah, just rejective fine tuning. We talked about it. Here we have a GRM to generate principle and critique in the

**verdict:** 
**notes:** 

---
