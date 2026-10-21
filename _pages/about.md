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

My current work studies production inference, especially capacity and KV/cache behavior, and how reliably LLM capabilities are invoked in agent settings. Compression remains a long-term part of my work, with a recent focus on how inference state is represented and moved through serving systems.

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
<h3 id="work-kv">KV Cache &amp; Inference State Compression</h3>
<p>Inference leaves behind state worth keeping, and KV cache is the largest part of it. This work looks at how that state is represented, compressed, and moved, so that structure in the data becomes real savings in memory and transfer time.</p>
<p><strong>AIBrix Hybrid KV Cache</strong> brings these ideas into an experimental offloading workflow for hybrid models, with tools for compression profiling. Whole-model output equivalence remains an open question.</p>
<div class="current-work-links"><a href="{{ '/kvcache-bench/' | relative_url }}">Benchmark</a><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache">Code</a><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache/releases/tag/hybrid-v0.1.1-experimental">Source preview</a><a href="https://github.com/vllm-project/aibrix/issues/3220">RFC</a><a href="https://github.com/vllm-project/aibrix/pull/3221">MEMORY backend PR (draft)</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-agent">
<h3 id="work-agent">Agent Reliability &amp; LLM Capability</h3>
<p>What a model can do and what an agent actually does are often far apart. Controlled probes and agent evaluations show how capabilities surface during a task, where they go unused, and what helps an agent carry its understanding through to action.</p>
<p><strong>AgentSight</strong> is an eBPF-based profiler for AI agents. It traces processes, files, network traffic, and LLM calls at the system level and links each action back to the prompt and tool decision behind it, with no SDK or code changes in the agent.</p>
<div class="current-work-links"><a href="{{ '/agent-reliability/' | relative_url }}">Project</a><a href="https://github.com/eunomia-bpf/agentsight">AgentSight code</a><a href="https://arxiv.org/abs/2508.02736">AgentSight paper</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-capacity">
<h3 id="work-capacity">Production Inference Capacity</h3>
<p>Performance numbers only mean something inside the serving system that produces them. This work examines how workloads, cache behavior, hardware, and latency requirements together set inference capacity, and how to keep that capacity stable under real deployment pressure.</p>
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
