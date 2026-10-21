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

<div class="current-work-list">
<article class="current-work-item" aria-labelledby="work-kv">
<h3 id="work-kv">KV Cache &amp; Inference State Compression</h3>
<p>KV cache is structured state, not a homogeneous byte stream. I study how representation and layout affect its compressibility, and when memory or transfer savings justify codec cost on a serving path.</p>
<p><strong>AIBrix Hybrid KV Cache:</strong> an experimental integration for hybrid-model prefix-cache offloading and compression profiling. Whole-model output equivalence remains under investigation.</p>
<div class="current-work-links"><a href="{{ '/kvcache-bench/' | relative_url }}">Benchmark</a><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache">Code</a><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache/releases/tag/hybrid-v0.1.1-experimental">Source preview</a><a href="https://github.com/vllm-project/aibrix/issues/3220">RFC</a><a href="https://github.com/vllm-project/aibrix/pull/3221">MEMORY backend PR (draft)</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-agent">
<h3 id="work-agent">Agent Reliability &amp; LLM Capability</h3>
<p>A model can demonstrate the right capability when prompted directly and still fail to invoke it during natural execution. I study this gap through controlled capability probes and agent evaluations.</p>
<div class="current-work-links"><a href="{{ '/agent-reliability/' | relative_url }}">Project</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-capacity">
<h3 id="work-capacity">Production Inference Capacity</h3>
<p>Offline throughput is not production capacity. I study how workload shape, cache behavior, hardware, and latency constraints determine sustainable serving capacity in real deployments.</p>
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

# 📝 Publications

{% assign themes = "LLM Capability & Agents|Compression & Representation|AI Systems & Inference" | split: "|" %}
{% for theme in themes %}
<h3 class="pub-theme">{{ theme }}</h3>
{% for pub in site.data.publications %}{% if pub.theme == theme %}{% include publication-card.html pub=pub %}{% endif %}{% endfor %}
{% endfor %}

# 🎖 Honors and Awards
{% for a in site.data.awards %}- *{{ a.date }}* {{ a.content }}
{% endfor %}

# 🤝 Services
- **ML conference referee:** NeurIPS 24/25/26, ACM MM 23/24, ICLR 25/26, ICML 25/26, CVPR 25/26, AAAI 26, ARR
- **System TPC:** USENIX ATC 25, GLSVLSI, RTCSA
- **Journal referee:** ACM TECS, TMLR, IEEE TKDE

# 👩‍🏫 Supervision
- Shashwat Jaiswal, summer intern (Ph.D. student at UIUC), 2026
- Yusheng Zheng, summer intern (Ph.D. student at UCSC), 2026
- Jun Wang, Ph.D. student with Prof. Jason Xue (2024–2025)
- Weilan Wang, Ph.D. student with Prof. Jason Xue (2024–2025)
- Dongdong Tang, Ph.D. student with Prof. Jason Xue (2024–2025)
