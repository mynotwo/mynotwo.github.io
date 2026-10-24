---
title: "Making LLM inference agree, bit for bit, across hardware"
date: 2026-10-23
lang: en
permalink: /blog/bitexact-inference/
excerpt: "Integer arithmetic makes reproducibility an execution contract, with explicit precision, overflow and serving trade-offs."
tags: [inference, reproducibility, compression]
---

A fixed seed does not fix every source of variation in an LLM. The same request can enter a different batch, use a different reduction kernel or run on another device. Small numerical differences can change a token choice and then the rest of the continuation.

I built [BitExact LLM](https://github.com/mynotwo/bitexact-llm) to control that part of the experiment. It implements Llama-3.2-1B inference with integer arithmetic, including the nonlinear functions and sampling rules. The target is matching logits and sampled tokens under explicitly tested execution changes.

![H800, H100 and CPU produce identical bit patterns given the same constants, input and seed.](/images/current-work-bitexact.svg)

*Conceptual illustration of bit identity. The displayed bit string is a symbol, not an experimental output.*

## Fix the arithmetic, not just the random seed

Floating-point addition depends on summation order. Fixing matrix tiles and reduction schedules can remove batch-dependent variation within a particular implementation. Cross-hardware agreement asks more: different implementations must perform equivalent arithmetic.

Integer sums are order-independent when intermediate values stay within their allowed range. BitExact uses fixed-point representations and explicit integer rounding rules. Matrix products split values into small integer limbs, compute partial products and combine them into wider accumulators. Nonlinear operations use integer procedures or precomputed tables, so inference does not call device-specific transcendental functions.

This moves the hard part into the contract: the scales, rounding, tables and intermediate bounds must all be specified. Integer arithmetic alone is not sufficient if an intermediate overflows or a hidden floating-point operation changes a decision.

## Three paths with different promises

The [current implementation](https://github.com/mynotwo/bitexact-llm/tree/a030ba7421aa61b6469a79efe85a61002512c476) separates three paths:

- **Exact mode** retains the original bf16 weights in linear layers and evaluates their products with quantized fixed-point activations. The input embedding is rounded once to the residual stream's fixed-point grid. “Exact” describes the specified arithmetic, not equality with a real-valued or fp32 model.
- **Int8 mode** uses quantized weights and a cheaper integer path. The vLLM plugin uses this mode.
- **Batch-invariant floating point** fixes Triton execution choices. Its reproducibility scope is one GPU architecture and Triton version, rather than the integer paths' tested cross-device scope.

Keeping these separate prevents an accuracy result from one path being paired with a speed result from another.

## What the checks actually compare

The repository's exact-mode identity checks hash the entire int64 logit row and compare sampled tokens at each generated position. They cover changes in batching, KV-cache use and selected kernel implementations on H800, H100, x86 CPU and Apple M4 Pro CPU. The same constants file identifies the model under test.

The vLLM tests ask a different question: does the int8 path remain stable when a scheduler changes execution? The recorded cases include mixed requests, chunked prefill, shared prefixes and preemption. The published tests use the offline engine API with `enforce_eager=True`; the plugin can capture its own decode graphs. They do not establish compatibility with every vLLM configuration or the serving API.

A distinction in the [reported evidence](https://github.com/mynotwo/bitexact-llm/blob/a030ba7421aa61b6469a79efe85a61002512c476/README.md#verified-results-exact-mode) is especially important: the large teacher-forced accuracy evaluation and the cross-device identity tests are different experiments. A count of positions in one is not evidence of identity in the other.

## Reproducibility has a cost

This is not a general throughput win. Against stock vLLM with CUDA graphs, the integer paths have substantial overhead, particularly in prefill and larger batches. A comparison against eager Hugging Face inference can give a much more favorable result because that baseline has different launch overheads. It answers a different performance question.

The unavoidable work includes extra limb products, wider intermediate representations, nonlinear integer operations and deterministic sampling. The implementation must preserve these semantics while reducing their cost. Faster kernels are useful only if they retain the equality being tested.

The current README also identifies incomplete overflow checks: some outputs are checked only after residual addition, and final logits are not checked. No check fired in the reported runs, but that observation is not a proof of safety for every input or model shape.

## Why I care about the same bits

For behavior research, reproducible inference removes one source of variation when comparing interventions. For neural lossless compression, matching probability computations matters because the decoder must reconstruct the encoder's decisions. These applications share a need for execution that can be compared precisely.

The useful deliverable is therefore a bounded, inspectable contract: which model and constants, which arithmetic, which execution changes, and which outputs were compared. The [repository](https://github.com/mynotwo/bitexact-llm) contains the implementation and reproduction commands; the [pinned README](https://github.com/mynotwo/bitexact-llm/blob/a030ba7421aa61b6469a79efe85a61002512c476/README.md) records the results and limitations described here.
