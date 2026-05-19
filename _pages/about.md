---
permalink: /
title: "Yu Mao"
excerpt: "Research Scientist at ByteDance, AI infrastructure and neural compression."
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

Hi there! I’m a Research Scientist at ByteDance (San Jose), focusing on AI infrastructure and system efficiency at scale. I received my Ph.D. in Computer Science from City University of Hong Kong. My work centers on designing next-generation data compression techniques (including neural approaches) and building high-performance systems for neural network acceleration and edge computing.

**Research interests**
- Neural and learned data compression
- System efficiency at scale (memory, storage, edge)
- Hardware-aware acceleration for ML workloads

# 🔥 News
{% for item in site.data.news %}- *{{ item.date }}*: &nbsp; {{ item.content }}
{% endfor %}

# 📝 Publications

{% assign themes = "Compression · LLM Efficiency|Whole-Slide-Image · Medical Imaging|Systems · Edge AI|ML · Theory" | split: "|" %}
{% for theme in themes %}
<h3 class="pub-theme">{{ theme }}</h3>
{% for pub in site.data.publications %}{% if pub.theme == theme %}{% include publication-card.html pub=pub %}{% endif %}{% endfor %}
{% endfor %}

# 🎖 Honors and Awards
{% for a in site.data.awards %}- *{{ a.date }}* {{ a.content }}
{% endfor %}

# 💬 Invited Talks
- *2023.10* — "Efficient Large Language Models", Institute of Microelectronics of the Chinese Academy of Sciences

# Services
- **ML conference referee:** NeurIPS 24/25/26, ACM MM 23/24, ICLR 25/26, ICML 25/26, CVPR 25/26, AAAI 26, ARR
- **System TPC:** USENIX ATC 25, GLSVLSI, RTCSA
- **Journal referee:** ACM TECS, TMLR, IEEE TKDE

# 🎓 Teaching
- CS3103 Operating Systems (TA) — 2020 Fall, 2021/22/23 Spring
- CS2115 Computer Organization (TA) — 2021/22/23 Fall
- CS1302 Introduction to Computer Programming (TA) — 2020 Spring

# 👩‍🏫 Supervision
- Jun Wang, Ph.D. student with Prof. Jason Xue (2024–present)
- Weilan Wang, Ph.D. student with Prof. Jason Xue (2024–present)
- Dongdong Tang, Ph.D. student with Prof. Jason Xue (2024–2025)
