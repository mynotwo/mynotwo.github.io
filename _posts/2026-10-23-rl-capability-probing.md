---
title: "What can training unlock? Using RL as a capability probe"
date: 2026-10-23
lang: en
permalink: /blog/rl-capability-probing/
excerpt: "Why equal accuracy can hide very different responses to training, and what random rewards let us measure."
tags: [RL, capability, evaluation]
---

Two models can answer the same fraction of questions correctly and still respond very differently to further training. That makes current accuracy an incomplete answer to a practical question: which checkpoint is worth post-training, and what kind of supervision will help it?

In our paper, [Probe with Participation Trophies](https://arxiv.org/abs/2610.01066), I study training itself as a probe. We call the object of measurement **reachability**: what a model can attain from its current state under specified training procedures, information and budgets. It is a property of a model *under an intervention*, rather than a single score attached to the model forever.

![A checkpoint branches into correctness-reward RL, random-reward RL and masked SFT before held-out evaluation.](/images/current-work-rl.svg)

*Method schematic. The branches represent different interventions, not measured improvements of equal size.*

## Why remove correctness from the reward?

A supervised probe has a familiar ambiguity: if it succeeds, did it expose something the model already represented, or learn the task from the labels supplied to the probe? Training with correctness rewards introduces a related ambiguity. The reward tells the learner which responses to reinforce.

Random rewards remove that information from the reward channel. The model still receives prompts, produces responses and undergoes optimization; those are substantial sources of structure. What disappears is the reward's ability to identify correct answers. This makes random-reward RL useful for a narrower question: **how does this starting model respond to training when the reward does not tell it what is right?**

That is why I treat it as an evaluation instrument. A high-scoring random-reward run does not establish that random rewards are a generally good training recipe, or prove that a complete solution was already present in the original model.

## Hold the training signal fixed, change the learner

One of our most informative controls uses cached rollouts. We take checkpoints from the end of OLMo-2 pre-training and the beginning of mid-training, and train both learners on the same responses with the same random rewards. Within each rollout source, the learners start with identical LoRA weights. This separates the learner's response from differences in the sampled training material.

In [Table 1 of the paper](https://arxiv.org/html/2610.01066#S3), each condition has 16 runs and a terminal evaluation at 500 updates. Using pre-training rollouts, the mean accuracy gain is 0.6 percentage points for the earlier learner and 4.5 for the later learner. Using mid-training rollouts, the corresponding gains are 2.9 and 13.7 percentage points.

The best run is a different statistic from the mean. The later learner's best endpoint reaches 80.0% with pre-training rollouts, but that is not its expected performance. The distinction matters when evaluating an intervention with large seed-to-seed variation.

The controlled comparison supports a specific conclusion: rollout quality alone does not explain the difference. The state of the learner also changes what the same training signal can do.

## The prompt remains part of the experiment

Removing correctness feedback does not remove task information. We therefore also compare random-token inputs with and without retained math instructions. The model responds differently to these conditions, even though neither supplies an ordinary, valid math question.

Across OLMo checkpoints, we observe an ordering: early checkpoints improve little under either reward; later checkpoints benefit from correctness rewards while random rewards remain weak; some mid-training checkpoints respond strongly even to random rewards. Number-masked SFT provides a further comparison outside the RL mechanism.

These are observed regimes in the studied settings. They are not universal developmental stages that every model must follow.

## Turning the experiment into a reusable tool

I am building a capability evaluation framework around this idea. Its unit of comparison is a fully specified intervention: checkpoint, prompt distribution, reward information, optimizer, update budget and evaluation protocol. Repeated runs are necessary to distinguish a reachable high endpoint from a reliable training response.

The systems work is part of the measurement. Changing serving behavior, silently replacing rollouts or mixing evaluation checkpoints changes the question being asked. A useful framework must retain those identities alongside results, so another experiment can challenge the finding under the same conditions.

The paper and its experiments are available; the reusable framework is ongoing work. For the full experimental setup, formal definition and controls, see the [paper](https://arxiv.org/abs/2610.01066) and [code](https://github.com/mynotwo/rl-random-prob).
