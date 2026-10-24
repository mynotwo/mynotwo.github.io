---
title: "Where did the training time and memory go?"
date: 2026-10-23
lang: en
permalink: /blog/omni-profiler/
excerpt: "The problem behind Omni Profiler: connecting CPU/GPU resource use to the code responsible for it during RL training."
tags: [profiling, RL, infrastructure]
---

A training job can look busy without making useful progress. GPU utilization tells us that something ran; a rising memory curve tells us that something accumulated. Neither identifies the code responsible or explains whether it lies on the path delaying the next training step.

I co-developed **Omni Profiler**, a continuous profiler that connects CPU/GPU memory and compute to Python and native code. It is used by Seed RL to investigate training workloads. The central design question is how to turn resource observations into an attribution that an engineer can act on.

<img src="/images/current-work-omni.svg" alt="CPU time, memory and GPU kernel observations connect to Python and native stacks and a hotspot." width="560" height="382" style="display:block;width:100%;max-width:560px;height:auto;margin:1.5em auto;">

*Conceptual resource attribution. The boxes do not encode measured time, bytes or overhead.*

## A peak is a symptom; attribution makes it actionable

Consider a hypothetical job whose host memory grows across iterations. A process-level curve cannot distinguish live allocations retained by application code from memory reserved by an allocator. The two observations can require very different responses.

There are several questions to answer before changing code: what resource is being measured, which process owns it, which stack created it, and whether the allocation has been released. On the compute side, a kernel's duration and the host code that launched it provide another view. Together, these views help turn “memory is high” or “the GPU is busy” into an investigation that a developer can follow.

Omni combines eBPF tracing, userspace allocation tracking and GPU instrumentation to connect these observations to code. Continuous collection and process discovery support looking at behavior over time, rather than relying entirely on a manually captured interval.

## The units must survive the visualization

A profiler can show several resources in the same interface without making them interchangeable. CPU time, GPU kernel duration, live allocated bytes and allocation traffic answer different questions.

For example, live memory depends on allocation and release lifetimes. Adding every allocation observed over a run measures traffic, not the amount retained at its end. Similarly, a long GPU kernel is not automatically the reason the request or training step took longer. It may overlap other work.

These distinctions shape how I read a profile. I first ask what gives each sample its weight and what interval it covers. Only then do I interpret a wide stack as a candidate for investigation. A graph with the wrong denominator can look convincing while sending an engineer toward the wrong optimization.

## Continuous collection changes the trade-off

A detailed trace of every event is attractive until collection changes the workload being measured. Sampling reduces that cost, but introduces another question: which events and stacks are represented well enough to support the conclusion?

The goal is evidence that remains useful across a long-running workload. Collection overhead, missed observations and stack attribution all affect that evidence. A missing stack should not be interpreted as zero resource use, and an unobserved event should not silently become a confirmed absence.

This is why I treat the profiler as part of the system under investigation. Before trusting an attribution, compare it with an independent resource measurement and a controlled workload whose behavior is understood. Agreement on a synthetic case validates that case; it does not establish accuracy for every real job.

## A hotspot is a hypothesis about the bottleneck

Suppose a hypothetical profile attributes substantial time to a CPU function. Making that function faster will shorten the training iteration only if its work constrains progress. If it finishes while a longer GPU operation is still running, the local speedup may have little effect on elapsed time.

The practical loop is: identify a suspicious resource cost, inspect its code and lifecycle, locate it in the execution timeline, then measure the workload after a targeted change. The final comparison is step time, throughput or memory headroom under the same workload—not simply a smaller rectangle in the profile.

That distinction is particularly useful in RL infrastructure, where several kinds of work interact and a local measurement may not represent the entire iteration.

## The connection to my research work

My capability experiments ask how models respond to controlled training interventions. Profiling asks whether the infrastructure is running those interventions as intended and where their cost comes from. Both require a measurement whose meaning survives inspection.

Omni's role in that loop is resource attribution: connect observed cost to the responsible execution context, then use that evidence to guide and validate an engineering change. My separate work on [agent execution evidence](/blog/agent-execution-evidence/) applies a related discipline at the task and tool-call level; it does not replace CPU/GPU profiling.

The project description on my [homepage](/#-current-work) summarizes my contribution and its use by Seed RL. The examples in this article are explanatory scenarios, not production incident reports.
