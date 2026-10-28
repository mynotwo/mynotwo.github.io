---
title: "Random-reward RL for capability probing"
date: 2026-10-23
lang: en
permalink: /blog/rl-capability-probing/
excerpt: "Training response can reveal capability that a checkpoint's current accuracy does not show."
tags: [RL, capability, evaluation]
---

Current accuracy tells us what a checkpoint can do now. It does not tell us what that checkpoint can reach with more training. This distinction matters when choosing a checkpoint to post-train—and when asking whether an evaluation method exposed an ability or taught the model the answer.

[Probe with Participation Trophies](https://arxiv.org/abs/2610.01066) uses reinforcement learning (RL) as a probe of **capability reachability**: what a model can attain from its current state under specified training procedures, information and budgets. The key idea is to measure the model's response to training, not treat its frozen score as the full measure of its capability.

For example, two OLMo checkpoints both start at **3.5%** accuracy on synthetic arithmetic. Under the same correctness-rewarded RL, their best runs reach **8.5%** and **55%**. The best-run figures are maxima across runs, not average outcomes.

<figure>
  <img src="/images/papers/random-reward-rl.png" alt="Three OLMo-2 capability reachability regimes: early pretraining checkpoints barely improve, later pretraining checkpoints respond to correctness rewards, and some mid-training checkpoints also reach high accuracy with random rewards." width="1340" height="590" style="display:block;width:100%;height:auto;margin:1.5em auto;">
  <figcaption>Training response separates three observed reachability regimes. Lines show individual seeds; bars show the best endpoint, not the mean (4 correctness-reward seeds, 8 random-reward seeds). These regimes describe the studied OLMo-2 checkpoints, not a universal training trajectory.</figcaption>
</figure>

## Why use random rewards to probe capability?

A supervised probe has a familiar ambiguity: if it succeeds, did it expose something the model already represented, or learn the task from the labels supplied to the probe? Training with correctness rewards introduces a related ambiguity. The reward tells the learner which responses to reinforce.

Random rewards remove that information from the reward channel. The model still receives prompts, produces responses and undergoes optimization; those are substantial sources of structure. What disappears is the reward's ability to identify correct answers. This makes random-reward RL useful for a narrower question: **how does this starting model respond to training when the reward does not tell it what is right?**

Random-reward RL serves here as an evaluation instrument. A high-scoring random-reward run does not establish that random rewards are a generally good training recipe, or prove that a complete solution was already present in the original model.

## How the probe compares interventions

The study compares correctness-reward RL, random-reward RL and number-masked supervised fine-tuning (SFT), then evaluates held-out behavior. The branches are different interventions; the schematic describes the experiment and does not imply equal-sized gains.

<img src="/images/current-work-rl.svg" alt="A checkpoint branches into correctness-reward RL, random-reward RL and masked SFT before held-out evaluation." width="560" height="382" loading="lazy" style="display:block;width:100%;max-width:560px;height:auto;margin:1.5em auto;">

*Intervention schematic. Each branch asks what the same starting checkpoint can reach under a different training signal.*

## Hold the training signal fixed, change the learner

A cached-rollout control compares checkpoints from the end of OLMo-2 pre-training and the beginning of mid-training. Both learners train on the same responses with the same random rewards. Within each rollout source, the learners start with identical LoRA weights. This separates the learner's response from differences in the sampled training material.

In [Table 1 of the paper](https://arxiv.org/html/2610.01066#S3), each condition has 16 runs and a terminal evaluation at 500 updates. Using pre-training rollouts, the mean accuracy gain is 0.6 percentage points for the earlier learner and 4.5 for the later learner. Using mid-training rollouts, the corresponding gains are 2.9 and 13.7 percentage points.

The best run is a different statistic from the mean. The later learner's best endpoint reaches 80.0% with pre-training rollouts, but that is not its expected performance. The distinction matters when evaluating an intervention with large seed-to-seed variation.

The controlled comparison supports a specific conclusion: rollout quality alone does not explain the difference. The state of the learner also changes what the same training signal can do.

## The prompt remains part of the experiment

Removing correctness feedback does not remove task information. An additional control compares random-token inputs with and without retained math instructions. The model responds differently to these conditions, even though neither supplies an ordinary, valid math question.

Across the studied OLMo checkpoints, the experiments show an ordering: early checkpoints improve little under either reward; later checkpoints benefit from correctness rewards while random rewards remain weak; some mid-training checkpoints respond strongly even to random rewards. Number-masked SFT provides a further comparison outside the RL mechanism.

These are observed regimes in the studied settings. They are not universal developmental stages that every model must follow.

## Turning the experiment into a reusable tool

A capability evaluation framework based on these interventions is under development. Its unit of comparison is a fully specified intervention: checkpoint, prompt distribution, reward information, optimizer, update budget and evaluation protocol. Repeated runs are necessary to distinguish a reachable high endpoint from a reliable training response.

The systems work is part of the measurement. Changing serving behavior, silently replacing rollouts or mixing evaluation checkpoints changes the question being asked. A useful framework must retain those identities alongside results, so another experiment can challenge the finding under the same conditions.

The paper and its experiments are available; the reusable framework is ongoing work. For the full experimental setup, formal definition and controls, see the [paper](https://arxiv.org/abs/2610.01066) and [code](https://github.com/mynotwo/rl-random-prob).
