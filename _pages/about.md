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
.current-work-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin: 24px 0 36px; }
.current-work-list .current-work-item { min-width: 0; padding: 24px; display: flex; flex-direction: column; background: rgba(255,255,255,.93); border: 1px solid #e0e6ef; border-top: 3px solid #788fc0; border-radius: 14px; box-shadow: 0 4px 16px rgba(35,55,90,.04); }
.current-work-list .current-work-item:first-child { grid-column: 1 / -1; border-top-color: #367d83; }
.current-work-list .current-work-item:nth-child(2) { border-top-color: #8371b1; }
.current-work-list .current-work-item:nth-child(4) { border-top-color: #367d83; }
.current-work-list .current-work-item h3 { margin: 0 0 14px; font-size: 1.12em; line-height: 1.4; letter-spacing: -.015em; color: #243955; }
.current-work-list .current-work-item p { margin: 0 0 14px; font-size: .92em; line-height: 1.75; color: #465369; }
.current-work-list .current-work-item p:last-child { margin-bottom: 0; }
.current-work-list .current-work-links { display: flex; flex-wrap: wrap; gap: 8px; margin-top: auto; padding-top: 6px; font-size: .8em; }
.current-work-list .current-work-links a { display: inline-flex; align-items: center; min-height: 34px; padding: 5px 11px; border: 1px solid #dce4ef; border-radius: 7px; background: #f5f8fc; color: #294f7c; font-weight: 600; line-height: 1.4; text-decoration: none; box-shadow: none; }
.current-work-list .current-work-links a:hover { background: #eaf0f8; border-color: #b8c9de; text-decoration: none; }
.current-work-list .current-work-links a:focus-visible { outline: 2px solid #294f7c; outline-offset: 3px; }
@media (max-width: 760px) {
  .current-work-list { grid-template-columns: minmax(0, 1fr); gap: 14px; }
  .current-work-list .current-work-item { padding: 20px; }
  .current-work-list .current-work-links a { min-height: 40px; }
}
</style>

<div class="current-work-list">
<article class="current-work-item" aria-labelledby="work-kv">
<h3 id="work-kv">AIBrix Hybrid KV Cache</h3>
<p>Built and open-sourced hybrid KV offloading with bounded storage, now used by TikTok Infra, with an upstream AIBrix PR. CPU byte-store round trips are verified; whole-model output equivalence remains open.</p>
<div class="current-work-links"><a href="https://github.com/mynotwo/aibrix-hybrid-kvcache">Code</a><a href="https://github.com/vllm-project/aibrix/pull/3221">Upstream PR #3221</a><a href="{{ '/blog/hybrid-kv-cache-storage-contract/' | relative_url }}">Technical article</a><a href="{{ '/kvcache-bench/' | relative_url }}">Benchmark</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-rl">
<h3 id="work-rl">RL as a Probe of LLM Capability</h3>
<p>My first-author paper uses random-reward RL to probe what further training can unlock beyond current accuracy. I am turning these controlled interventions into a capability evaluation framework.</p>
<div class="current-work-links"><a href="https://arxiv.org/abs/2610.01066">Paper</a><a href="https://github.com/mynotwo/rl-random-prob">Code</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-bitexact">
<h3 id="work-bitexact">Bitwise-Reproducible LLM Inference Across Hardware</h3>
<p>Built integer-exact and batch-invariant LLM engines with vLLM integration. The integer engine reproduced 95K tokens bitwise across tested H800, H100, and x86 CPU configurations, supporting reproducible inference and lossless compression.</p>
<div class="current-work-links"><a href="https://github.com/mynotwo/bitexact-llm">Project repository</a></div>
</article>
<article class="current-work-item" aria-labelledby="work-capacity">
<h3 id="work-capacity">Omni Profiler: Continuous Profiling for RL Training</h3>
<p>Co-developed a continuous profiler that traces CPU/GPU memory and compute back to Python and native code. Now used by Seed RL to investigate training bottlenecks and memory growth.</p>
</article>
<article class="current-work-item" aria-labelledby="work-agent">
<h3 id="work-agent">Agent Reliability &amp; Semantic Profiling</h3>
<p>I test whether agents actually execute the actions they claim. I also coauthored AgentPProf for semantic resource profiling, winner of the AgenticOS @ SOSP 2026 Best Paper Award.</p>
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
