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

Hi, I’m Yu Mao. Feel free to call me Audrey! I’m a Research Scientist at ByteDance in San Jose, working on AI infrastructure and inference. I received my Ph.D. in Computer Science from City University of Hong Kong, where I worked on compression and computer systems.

My current work connects LLM capability research with the systems needed to run and understand training and inference. I study reinforcement learning as a probe of capability reachability, build profiling tools for RL workloads, and develop reproducible inference and KV-cache storage systems. Compression remains a long-term thread across this work.

**Research interests**

<span class="interest-pill" style="background: linear-gradient(135deg, #667eea, #764ba2);">Inference Systems</span>
<span class="interest-pill" style="background: linear-gradient(135deg, #f093fb, #ffd700);">Compression &amp; Representation</span>
<span class="interest-pill" style="background: linear-gradient(135deg, #38bdf8, #667eea);">LLM Capability &amp; Agent Reliability</span>

<span style="display:block; margin-top:8px; font-size:0.9em; color:#666;">
  Google Scholar: Cited by <span id='total_cit' style='font-weight:bold;color:#224b8d;'>...</span>
</span>

# 🔬 Current Work

<style>
.current-work-list .current-work-item { padding: 1.1em 0; border-bottom: 1px solid #dfe3e8; }
.current-work-list .current-work-item:first-child { padding-top: 0.4em; }
.current-work-list .current-work-item:last-child { border-bottom: 0; }
.current-work-list .current-work-item h3 { margin: 0 0 0.5em; font-size: 1.08em; color: #224b8d; }
.current-work-list .current-work-item p { margin: 0 0 0.65em; }
.current-work-list .current-work-links { display: flex; flex-wrap: wrap; gap: 0.4em 1.1em; font-size: 0.85em; }
.current-work-list .current-work-links a { text-underline-offset: 3px; }
.current-work-list .current-work-links a:focus-visible { outline: 2px solid #224b8d; outline-offset: 3px; }
</style>

<div class="current-work-list">
<article class="current-work-item" aria-labelledby="work-kv">
<h3 id="work-kv">AIBrix Hybrid KV Cache</h3>
<p>I built and open-sourced an experimental extension for hybrid-state offloading and variable-sized KV records, including bounded MEMORY storage, reader leases, and eviction constraints. The MEMORY backend was submitted upstream to AIBrix under the vLLM project. TikTok Infra has begun using the work.</p>
<p>A fixed-version CPU example verifies byte-store round trips and compression accounting. Whole-model output equivalence remains an open question.</p>
<div class="current-work-links"><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache">Code</a><a href="https://github.com/vllm-project/aibrix/pull/3221">Upstream PR #3221</a><a href="{{ '/blog/hybrid-kv-cache-storage-contract/' | relative_url }}">Technical article</a><a href="{{ '/kvcache-bench/' | relative_url }}">Benchmark</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-rl">
<h3 id="work-rl">RL as a Probe of LLM Capability</h3>
<p>My first-author paper uses random-reward RL and controlled training comparisons to study capability reachability: what further training can attain from a checkpoint under specified constraints, beyond its current accuracy. I am building an RL-based capability evaluation framework around these interventions.</p>
<div class="current-work-links"><a href="https://arxiv.org/abs/2610.01066">Paper</a><a href="https://github.com/mynotwo/rl-random-prob">Code</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-bitexact">
<h3 id="work-bitexact">Bitwise-Reproducible LLM Inference Across Hardware</h3>
<p>My personal project combines integer-exact Llama-3.2-1B inference, a batch-invariant Triton Llama-3.1-8B engine, and vLLM integration. The integer engine produced bitwise-identical outputs over 95K tokens across tested H800, H100, and x86 CPU configurations.</p>
<p>I also use deterministic inference for lossless compression, including agent trajectories, with GPU neural prediction and rANS coding.</p>
<div class="current-work-links"><a href="https://github.com/mynotwo/bitexact-llm">Project repository</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-capacity">
<h3 id="work-capacity">Omni Profiler: Continuous Profiling for RL Training</h3>
<p>I co-developed Omni Profiler, now in use by Seed RL, to investigate memory growth and performance bottlenecks in training workloads. It combines eBPF tracing, userspace allocation tracking, and GPU instrumentation to attribute CPU/GPU memory, CPU time, and GPU kernels to Python and native code.</p>
<p>Sampling, automatic process discovery, continuous collection, and interactive reports support analysis across distributed training workers.</p>
</article>
<article class="current-work-item" aria-labelledby="work-agent">
<h3 id="work-agent">Agent Reliability &amp; Semantic Profiling</h3>
<p>I study the gap between an agent's reported actions and observable execution through controlled probes, counterexamples, and repeated trials. I also coauthored AgentPProf, which aggregates agent trajectories into semantic profiles for resource attribution and received the AgenticOS @ SOSP 2026 Best Paper Award.</p>
<div class="current-work-links"><a href="{{ '/agent-reliability/' | relative_url }}">Reliability project</a><a href="https://os-for-agent.github.io/papers/AgenticOS_SOSP_2026_paper_27.pdf">AgentPProf paper</a><a href="https://github.com/eunomia-bpf/agentsight">AgentPProf code</a></div>
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
