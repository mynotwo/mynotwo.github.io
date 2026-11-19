---
permalink: /
title: "Yu Mao"
excerpt: "Research Scientist at ByteDance working on AI infrastructure, inference systems, compression, and LLM reliability."
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<span class='anchor' id='about-me'></span>

Hi, I'm Yu Mao. Feel free to call me Audrey! I'm a Research Scientist at ByteDance working on AI infrastructure for LLMs. **I build LLM systems whose behavior can be checked, not just benchmarked**: byte-exact KV-cache compression, bitwise-reproducible inference, probes of what further training can unlock in a model, and tests of whether agents did what they claim. I received my Ph.D. in Computer Science from City University of Hong Kong, where I worked on compression and computer systems.

**Highlights**

- [Best Paper Award](https://os-for-agent.github.io/papers/AgenticOS_SOSP_2026_paper_27.pdf) at AgenticOS @ SOSP 2026 for AgentPProf, a semantic profiler for AI agents
- [Hybrid KV cache offloading](#work-kv){:target="_self"} that I built and open-sourced is in use at TikTok Infra
- <a href="{{ site.author.googlescholar }}">Google Scholar</a><span id="scholar-summary" hidden>: <span id="scholar_citedby"></span> citations, h-index <span id="scholar_hindex"></span> (as of <span id="scholar_updated"></span>)</span>

**Research interests**

<span class="interest-pill">Inference Systems</span>
<span class="interest-pill">Compression &amp; Representation</span>
<span class="interest-pill">LLM Capability &amp; Agent Reliability</span>

# 🔬 Current Work

<div class="current-work-list">
{% for work in site.data.current_work.featured %}{% include current-work-item.html work=work %}{% endfor -%}
<h2 class="current-work-more">More research</h2>
{% for work in site.data.current_work.more %}{% include current-work-item.html work=work related=true %}{% endfor -%}
</div>

{% include hushword-tool.html placement="mobile" %}

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
{% for s in site.data.services %}- **{{ s.role }}:** {{ s.venues }}
{% endfor %}

# 👩‍🏫 Supervision
{% for s in site.data.supervision %}- {{ s.name }}, {{ s.detail }}
{% endfor %}
