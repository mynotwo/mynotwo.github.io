---
permalink: /
title: "Yu Mao"
excerpt: "Research Scientist at ByteDance working on AI infrastructure, inference systems, compression, and LLM reliability."
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I study how LLM capabilities emerge through training and build systems that make training and inference measurable, reproducible, and efficient.

I’m Yu Mao (Audrey), a Research Scientist at ByteDance in San Jose. My recent work uses random-reward RL to probe model capabilities, connects training resource use to code with Omni Profiler, and builds bounded storage for hybrid KV caches.

I received my Ph.D. in Computer Science from City University of Hong Kong, working on compression and computer systems.

**Research interests**

<span class="interest-pill">Inference Systems</span>
<span class="interest-pill">Compression &amp; Representation</span>
<span class="interest-pill">LLM Capability &amp; Agent Reliability</span>

# 🔬 Current Work

<style>
body.homepage { background-image: none !important; }
body.homepage .interest-pill { background: #edf2f7; color: #334155; }
@media (max-width: 600px) {
  body.homepage .profile_box { display: grid; grid-template-columns: 75px minmax(0, 1fr); gap: 12px; align-items: center; }
  body.homepage .author__content { min-width: 0; padding-left: 0; }
  body.homepage .author__urls-wrapper { grid-column: 1 / -1; margin-left: 0; }
  body.homepage .author__urls_sm { display: flex; flex-wrap: wrap; gap: 8px; padding: 0; }
  body.homepage .author__urls_sm a { display: inline-flex; align-items: center; justify-content: center; min-width: 40px; min-height: 44px; }
}
.current-work-list { margin: 22px 0 36px; max-width: 850px; }
.current-work-list .current-work-item { display: grid; grid-template-columns: 300px minmax(0, 1fr); column-gap: 24px; align-items: start; padding: 22px 0; border-bottom: 1px solid #e1e5eb; }
.current-work-list .current-work-figure { display: block; width: 100%; height: auto; margin: 0; }
.current-work-list .current-work-copy { min-width: 0; }
.current-work-list figure { margin: 0; }
.current-work-list figcaption { margin-top: 12px; font-size: 14px; font-family: inherit; line-height: 1.6; color: #465369; }
.current-work-list .current-work-copy p + p { margin-top: 8px; }
.current-work-list .current-work-more { margin: 32px 0 0; font-size: 1.05em; }
.current-work-list .current-work-item--related { grid-template-columns: 160px minmax(0, 1fr); }
.current-work-list .current-work-item:first-child { padding-top: 0; }
.current-work-list .current-work-item:last-child { padding-bottom: 0; border-bottom: 0; }
.current-work-list .current-work-item h3 { margin: 0 0 8px; font-size: 1.08em; line-height: 1.4; letter-spacing: -.015em; color: #243955; }
.current-work-list .current-work-item p { margin: 0; font-size: .92em; line-height: 1.65; color: #465369; }
.current-work-list .current-work-links { display: flex; flex-wrap: wrap; column-gap: 18px; row-gap: 4px; margin-top: 8px; font-size: .82em; }
.current-work-list .current-work-links a { display: inline-block; padding: 3px 0; color: #295d8a; font-weight: 500; line-height: 1.5; text-decoration: none; box-shadow: none; }
.current-work-list .current-work-links a:hover { text-decoration: underline; text-underline-offset: 3px; }
.current-work-list .current-work-links a:focus-visible { outline: 2px solid #295d8a; outline-offset: 3px; }
@media (max-width: 760px) {
  .current-work-list .current-work-item, .current-work-list .current-work-item--related { grid-template-columns: minmax(0, 1fr); row-gap: 16px; padding: 20px 0; }
  .current-work-list .current-work-copy { grid-row: 1; }
  .current-work-list figure, .current-work-list .current-work-figure { max-width: 320px; }
  .current-work-list .current-work-item--related .current-work-figure { max-width: 160px; }
  .current-work-list .current-work-links { column-gap: 20px; }
  .current-work-list .current-work-links a { padding: 8px 0; }
}
</style>

<div class="current-work-list">
<article class="current-work-item" aria-labelledby="work-rl">
<figure>
<img class="current-work-figure" src="{{ '/images/current-work-rl-v2.svg' | relative_url }}?v=research" width="440" height="300" loading="lazy" alt="Reported best terminal GSM accuracy at three selected OLMo-2-7B checkpoints; GT reward has 4 seeds and random reward has 8.">
<figcaption>GSM accuracy at three selected OLMo-2-7B checkpoints. Bars show the best terminal result across seeds, not the mean: correctness reward uses 4 seeds; random reward uses 8. Different seed counts limit direct comparison of maxima.</figcaption>
</figure>
<div class="current-work-copy">
<h3 id="work-rl">RL as a Probe of LLM Capability</h3>
<p>Current accuracy does not tell us how a model will respond to further training. My first-author paper uses random-reward RL to probe that response without correctness information in the reward.</p>
<p>Controlled comparisons show that the learner’s starting state changes what the same training signal can unlock. The paper and code are available; a reusable capability evaluation framework is in development.</p>
<div class="current-work-links"><a href="{{ '/blog/rl-capability-probing/' | relative_url }}">Blog</a><a href="https://arxiv.org/abs/2610.01066">Paper</a><a href="https://github.com/mynotwo/rl-random-prob">Code</a></div>
</div>
</article>
<article class="current-work-item" aria-labelledby="work-capacity">
<figure>
<img class="current-work-figure" src="{{ '/images/current-work-omni-v2.svg' | relative_url }}?v=research" width="440" height="300" loading="lazy" alt="Technical schematic separating CPU time, GPU duration and live-memory weights and attribution; no measured profile values.">
<figcaption>Resource-attribution schematic. CPU time, GPU duration and live memory are distinct measurements; this is not a measured performance result.</figcaption>
</figure>
<div class="current-work-copy">
<h3 id="work-capacity">Omni Profiler: Continuous Profiling for RL Training</h3>
<p>High utilization or growing memory alone does not identify the responsible code. I co-developed Omni Profiler to connect CPU/GPU memory and compute to Python and native stacks.</p>
<p>Seed RL uses the profiler to investigate training bottlenecks and memory growth, connecting resource measurements to code that engineers can inspect.</p>

<div class="current-work-links"><a href="{{ '/blog/omni-profiler/' | relative_url }}">Blog</a></div>
</div>
</article>
<article class="current-work-item" aria-labelledby="work-kv">
<figure>
<img class="current-work-figure" src="{{ '/images/current-work-kv.svg' | relative_url }}" width="440" height="300" loading="lazy" alt="Hybrid state and KV spans are encoded, stored, then decoded and checked byte for byte.">
<figcaption>Storage mechanism: encode hybrid state and KV spans, then restore and check the bytes. This does not establish whole-model output equivalence.</figcaption>
</figure>
<div class="current-work-copy">
<h3 id="work-kv">AIBrix Hybrid KV Cache</h3>
<p>Hybrid-model prefixes need recurrent state and attention history to survive offloading together. I built and open-sourced hybrid KV offloading with bounded storage and reader-safe eviction, now used by TikTok Infra.</p>
<p>The upstream AIBrix PR contributes the byte-store contract. CPU byte-store round trips are verified; whole-model output equivalence remains open.</p>
<div class="current-work-links"><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache">Code</a><a href="https://github.com/vllm-project/aibrix/pull/3221">Upstream PR #3221</a><a href="{{ '/blog/hybrid-kv-cache-storage-contract/' | relative_url }}">Blog</a><a href="{{ '/kvcache-bench/' | relative_url }}">Benchmark</a></div>
</div>
</article>
<h2 class="current-work-more">More research</h2>
<article class="current-work-item current-work-item--related" aria-labelledby="work-bitexact">
<img class="current-work-figure" src="{{ '/images/current-work-bitexact-v2.svg' | relative_url }}?v=research" width="440" height="300" loading="lazy" alt="Historical exact-mode report: zero logits and token differences against H800 over 3,696 generated positions on selected devices.">
<div class="current-work-copy">
<h3 id="work-bitexact">Bitwise-Reproducible LLM Inference Across Hardware</h3>
<p>Built integer LLM inference with matching logits and tokens across tested GPU and CPU configurations. An int8 vLLM plugin preserves reproducibility under tested batching and cache changes.</p>
<div class="current-work-links"><a href="{{ '/blog/bitexact-inference/' | relative_url }}">Blog</a><a href="https://github.com/mynotwo/bitexact-llm">Project repository</a></div>
</div>
</article>
<article class="current-work-item current-work-item--related" aria-labelledby="work-agent">
<img class="current-work-figure" src="{{ '/images/current-work-agent-v2.svg' | relative_url }}?v=research" width="440" height="300" loading="lazy" alt="Observed case: four file calls preceded the first web call despite a web-before-file claim; call order is not elapsed time.">
<div class="current-work-copy">
<h3 id="work-agent">Agent Reliability &amp; Semantic Profiling</h3>
<p>I test whether agents actually execute the actions they claim. I also coauthored AgentPProf for semantic resource profiling, winner of the AgenticOS @ SOSP 2026 Best Paper Award.</p>
<div class="current-work-links"><a href="{{ '/blog/agent-execution-evidence/' | relative_url }}">Blog</a><a href="{{ '/agent-reliability/' | relative_url }}">Reliability project</a><a href="https://os-for-agent.github.io/papers/AgenticOS_SOSP_2026_paper_27.pdf">AgentPProf paper</a><a href="https://github.com/eunomia-bpf/agentsight">AgentPProf code</a></div>
</div>
</article>
</div>

# 🔥 News
<div class="news-timeline" markdown="1">
{% for item in site.data.news limit:4 %}- *{{ item.date }}*: &nbsp; {{ item.content }}
{% endfor %}
</div>

<details markdown="1">
<summary>Earlier news</summary>

{% for item in site.data.news offset:4 %}- *{{ item.date }}*: &nbsp; {{ item.content }}
{% endfor %}
</details>

<span id="-publications"></span>

# 📝 Selected Publications

{% assign selected = site.data.publications | where_exp: "pub", "pub.selected_order" | sort: "selected_order" %}
{% for pub in selected %}{% include publication-card.html pub=pub %}{% endfor %}

[View all publications →]({{ '/publications/' | relative_url }})

# 🎖 Honors and Awards
{% for a in site.data.awards %}- *{{ a.date }}* {{ a.content }}
{% endfor %}

# 🤝 Services
- **Conference reviewing:** NeurIPS 2024–2026; ICLR 2025–2026; ICML 2025; CVPR 2024–2026; ICCV 2025; BMVC 2026; ACM MM 2023–2024; ARR
- **Program committees:** AAAI 2026; DAC 2026; GLSVLSI 2025–2026; RTCSA 2025
- **External review committee:** USENIX ATC 2024
- **Artifact evaluation committees:** EuroSys 2025; DSN 2024
- **Journal reviewing:** ACM TECS; TMLR; IEEE TKDE

# 👩‍🏫 Supervision
- Shashwat Jaiswal, summer intern (Ph.D. student at UIUC), 2026
- Yusheng Zheng, summer intern (Ph.D. student at UCSC), 2026
- Jun Wang, Ph.D. student with Prof. Jason Xue (2024–2025)
- Weilan Wang, Ph.D. student with Prof. Jason Xue (2024–2025)
- Dongdong Tang, Ph.D. student with Prof. Jason Xue (2024–2025)
