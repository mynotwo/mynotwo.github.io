---
title: "Evaluating agent process claims against execution traces"
date: 2026-10-23
lang: en
permalink: /blog/agent-execution-evidence/
excerpt: "Checking an agent's result, its claims about execution, and the cost of its trajectory as separate questions."
tags: [agents, reliability, profiling]
---

An agent can return a correct answer while describing a process it did not follow. If the evaluation only checks the answer, that discrepancy disappears from the score.

In a behavior-probing experiment, one response said it had checked external sources first and then compared them with an attached file. The observed trace contained four file calls before any web call. The task result was correct. The claim about execution order was not.

That example is narrower than “the agent never verified anything.” It is a **false process claim**. Naming the failure precisely matters: different failures need different checks.

<img src="/images/current-work-agent.svg" alt="The claimed sequence is web then file; the observed sequence is file calls then web." width="560" height="382" style="display:block;width:100%;max-width:560px;height:auto;margin:1.5em auto;">

*Simplified rendering of the observed ordering discrepancy. No private prompt, file content or account history is reproduced.*

## Result, execution and resource evaluation

The evaluation separates result correctness, execution evidence and resource use.

Result correctness asks whether the delivered output satisfies the task. Execution evidence asks whether claimed actions occurred, with the required inputs and outcomes. Resource analysis asks where time, tokens or other costs accumulated.

A correct result does not settle the second question. A complete-looking trace does not settle the first. A low token count does not settle either. Keeping the questions separate makes it possible to diagnose the failure instead of losing it inside an aggregate score.

For a claimed test run, for example, useful evidence includes the invocation, its target revision, its completion status and the result. A command that was prepared but never executed is different from a failed test. An old passing run is different from a check of the current change. These are examples of the distinctions an evaluator should preserve, not additional outcomes claimed from the ordering experiment above.

## Establish what the instrumentation can see

Scoring a missing action requires establishing whether the recorder would have captured it. In the probing work, some document-artifact actions appeared inside assistant output rather than as ordinary tool nodes. Counting only tool nodes would have undercounted those actions.

Clarification was another trap. A request for missing information can be phrased as an imperative rather than a question. A punctuation-based detector confuses presentation with behavior.

The resulting rule is methodological: map each verdict to an observable event or artifact, and record uncertainty where observability is incomplete. “Not found in this trace” becomes “did not happen” only when the trace is sufficiently complete for that action.

## Try to break the inferred rule

A memorable example can suggest a behavioral rule, but it does not establish one. The study used discovery cases, targeted counterexamples, repeated runs and interleaved comparisons to challenge the initial interpretations.

Some apparent rules did not survive repetition. Cross-session retrieval also contaminated parts of the experiment: later probes could draw on earlier conversations. Those trials cannot be treated as independent samples from a fresh environment. This limits what the study says about general behavior, even when individual traces are clear.

The useful output is therefore not a universal score for an agent. It is a set of evidence-linked observations, counterexamples and revised hypotheses, with their experimental conditions attached.

## Where AgentPProf fits

[AgentPProf](https://os-for-agent.github.io/papers/AgenticOS_SOSP_2026_paper_27.pdf) addresses a related but distinct question: how to aggregate agent activity into resource profiles that developers can inspect.

AgentPProf represents activity as weighted operations, then folds those operations by chosen fields into operation stacks. The output is pprof-compatible, so existing tools can inspect the aggregate and drill into its structure. Token usage and operation counts are examples of weights; task and execution-phase annotations provide semantic grouping.

This is not a CPU stack sampler, and a profile does not prove that the agent fulfilled the task. It helps locate where resources went. The reliability analysis then needs the underlying events and a task-specific criterion to decide whether that work was appropriate or whether a claimed action is supported.

## A useful evaluation ends with inspectable evidence

A completion claim can be evaluated against the delivered artifact, the actions that produced it and the checks supporting the claim. Repeated trials test whether the observation is stable; controlled changes help identify what it depends on.

The objective is an evaluator that can explain a failure in concrete terms: the result was wrong, the claimed process conflicted with the trace, or the evidence was insufficient. Those distinctions make a regression actionable.

See the [reliability project page](/agent-reliability/) for the broader workflow, and the [AgentPProf paper](https://os-for-agent.github.io/papers/AgenticOS_SOSP_2026_paper_27.pdf) and [code](https://github.com/eunomia-bpf/agentsight) for semantic profiling. The behavioral observations and AgentPProf are separate pieces of work; neither is presented as validation of the other.
