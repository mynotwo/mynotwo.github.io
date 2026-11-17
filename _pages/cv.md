---
layout: default
permalink: /cv/
title: "CV"
excerpt: "Curriculum vitae of Yu Mao: experience, education, publications, honors and service."
author_profile: true
---

# Curriculum Vitae

**{{ site.author.name }}** (Audrey) · {{ site.author.bio }} · {{ site.author.location }} · [{{ site.author.email }}](mailto:{{ site.author.email }})

{% assign sections = "experience|education|internships" | split: "|" %}
{% for section in sections %}
## {{ section | capitalize }}

{% for item in site.data.cv[section] %}- **{{ item.title }}**, {{ item.org }}{% if item.place %}, {{ item.place }}{% endif %}{% if item.period %} ({{ item.period }}){% endif %}{% if item.detail %}<br>{{ item.detail }}{% endif %}
{% endfor %}
{% endfor %}

## Publications

{% assign themes = "LLM Capability & Agents|Compression & Representation|AI Systems & Inference|Applied ML" | split: "|" %}
{% for theme in themes %}
**{{ theme }}**

{% for pub in site.data.publications %}{% if pub.theme == theme %}{% unless pub.case_study %}{% assign paper_url = pub.arxiv | default: pub.pdf | default: pub.doi %}- {{ pub.authors }}. {% if paper_url %}[{{ pub.title }}]({{ paper_url }}){% else %}{{ pub.title }}{% endif %}. *{{ pub.venue }}*.
{% endunless %}{% endif %}{% endfor %}
{% endfor %}

## Honors and Awards

{% for a in site.data.awards %}- *{{ a.date }}* {{ a.content }}
{% endfor %}

## Services

{% for s in site.data.services %}- **{{ s.role }}:** {{ s.venues }}
{% endfor %}

## Supervision

{% for s in site.data.supervision %}- {{ s.name }}, {{ s.detail }}
{% endfor %}
