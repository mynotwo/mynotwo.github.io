---
title: "Why Learned Compression Is Hard to Beat — and Hard to Ship"
date: 2026-06-05
lang: en
tags: [compression, notes]
excerpt: "A few notes on the gap between rate-distortion wins on paper and the realities of deploying neural codecs at scale."
---

Learned (neural) compression has, on paper, comfortably overtaken classical codecs on rate-distortion curves. Yet production pipelines still lean on JPEG, H.265, and zstd. Why the gap?

## Three frictions

1. **Decode latency.** A learned codec that beats H.266 by 15% BD-rate but needs a GPU to decode is a non-starter for most edge scenarios.
2. **Determinism across hardware.** Floating-point entropy coding that isn't bit-exact across devices breaks the round-trip. This is the quiet killer.
3. **Tail behavior.** Classical codecs degrade gracefully on out-of-distribution inputs; neural ones can fall off a cliff.

The interesting research frontier isn't another 2% on Kodak — it's making these systems *boring*: deterministic, cheap to decode, and predictable on the tail.

More to come.
