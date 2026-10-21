---
layout: default
permalink: /publications/
title: "Publications"
author_profile: true
---

# Publications

[← Selected publications on the homepage]({{ '/#-publications' | relative_url }})

{% assign themes = "LLM Capability & Agents|Compression & Representation|AI Systems & Inference|Applied ML" | split: "|" %}
{% for theme in themes %}
<h2 class="pub-theme">{{ theme }}</h2>
{% for pub in site.data.publications %}{% if pub.theme == theme %}{% unless pub.case_study %}{% include publication-card.html pub=pub %}{% endunless %}{% endif %}{% endfor %}
{% endfor %}
