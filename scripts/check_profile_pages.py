"""Smoke-check built profile pages: python3 scripts/check_profile_pages.py _site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import mimetypes
import statistics
import sys


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def find(self, tag=None, cls=None):
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (
                    cls is None or cls in child.attrs.get("class", "").split()
                ):
                    yield child
                yield from child.find(tag, cls)

    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)


class Document(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def check(root):
    pages = {
        "index.html": ("Yu Mao — Research Scientist", "profile"),
        "publications/index.html": ("Publications — Yu Mao", "website"),
        "blog/index.html": ("Blog — Yu Mao", "website"),
        "photos/index.html": ("Photos — Yu Mao", "website"),
        "blog/bitexact-inference/index.html": (
            "Cross-hardware bitwise reproducibility in LLM inference — Yu Mao", "article"
        ),
    }
    docs = {}
    for path, (title, kind) in pages.items():
        doc = Document((root / path).read_text()).root
        docs[path] = doc
        assert next(doc.find("title")).text() == title, path
        meta = {n.attrs.get("property", n.attrs.get("name")): n.attrs.get("content")
                for n in doc.find("meta")}
        assert meta["og:title"] == meta["twitter:title"] == title, path
        assert meta["og:type"] == kind, path
        assert meta["description"] and "Do small things" not in meta["description"], path
        for a in doc.find("a"):
            href = a.attrs.get("href", "")
            if href.startswith("/") and not href.startswith("//"):
                target = root / unquote(urlsplit(href).path).lstrip("/")
                assert target.exists(), (path, href)
        print("PASS metadata and internal links:", path)

    pubs = list(docs["publications/index.html"].find(cls="paper-box"))
    code_projects = {
        "AgentPProf:": "https://github.com/eunomia-bpf/agentsight",
        "Trace:": "https://github.com/mynotwo/A-Fast-Transformer-based-General-Purpose-LosslessCompressor",
        "Faster and Stronger": "https://github.com/mynotwo/Faster-and-Stronger-Lossless-Compression-with-Optimized-Autoregressive-Framework",
    }
    for prefix, expected in code_projects.items():
        card = next(c for c in pubs if next(c.find(cls="paper-title")).text().startswith(prefix))
        links = {a.text(): a.attrs["href"] for a in card.find("a")}
        assert links["Code"] == expected, prefix
        assert list(next(card.find(cls="paper-title")).find("a")), prefix
    mm = next(c for c in pubs if c.text().strip().startswith("Accelerating General-purpose"))
    assert not any(a.text() == "Code" for a in mm.find("a"))
    publication_dois = {
        "Hitcher:": "https://doi.org/10.1145/3770854.3780212",
        "Parallel-SA:": "https://doi.org/10.23919/DATE69613.2026.11539197",
    }
    for prefix, expected in publication_dois.items():
        matches = [c for c in pubs if next(c.find(cls="paper-title")).text().startswith(prefix)]
        assert len(matches) == 1, (prefix, "missing or duplicate publication")
        card = matches[0]
        assert next(next(card.find(cls="paper-title")).find("a")).attrs["href"] == expected
        links = {a.text(): a.attrs["href"] for a in card.find("a")}
        assert links["DOI"] == expected, prefix
        assert "PDF" not in links, (prefix, "DOI must not be labeled as PDF")
    assert all(next(c.find(cls="paper-title")).text().strip() for c in pubs)
    print("PASS publication links, unique new entries and accurate DOI labels")

    home = docs["index.html"]
    ids = [n.attrs["id"] for n in home.find() if "id" in n.attrs]
    assert len(ids) == len(set(ids)), "Duplicate homepage IDs"
    assert ids.index("-current-work") < ids.index("-news") < ids.index("-selected-publications")
    assert len(list(home.find(cls="hushword-tool--sidebar"))) == 1
    assert len(list(home.find(cls="hushword-tool--mobile"))) == 1
    assert "Open draft PR #3221" in home.text()
    assert "has not been merged" in home.text()
    assert "do not revalidate" in home.text()
    assert "Do small things with great love!" in home.text()
    article = docs["blog/bitexact-inference/index.html"].text()
    assert "Version note" in article and "971a3e1" in article and "a030ba7" in article
    assert "The current README also identifies incomplete overflow checks" not in article
    print("PASS project scope, version boundaries, unique IDs and preserved personal content")

    # Resolve links from every rendered page, including fragments and metadata assets.
    all_docs = {p: Document(p.read_text()).root for p in root.rglob("*.html")}
    social_labels = {"Email", "LinkedIn", "DBLP", "GitHub", "Google Scholar", "ORCID"}
    for path, doc in all_docs.items():
        for social in doc.find(cls="author__urls_sm"):
            links = list(social.find("a"))
            assert len(links) == len(social_labels), (path, "mobile social links")
            assert {a.attrs.get("aria-label") for a in links} == social_labels, (path, "mobile link names")
            assert all(i.attrs.get("aria-hidden") == "true" for a in links for i in a.find("i")), path
        ids = [n.attrs["id"] for n in doc.find() if "id" in n.attrs]
        assert len(ids) == len(set(ids)), (path, "duplicate IDs")
        for node in doc.find():
            refs = [node.attrs.get(key, "") for key in ("href", "src", "data-full")]
            if node.tag == "meta" and node.attrs.get("name", node.attrs.get("property")) in {
                "msapplication-TileImage", "msapplication-config", "og:image", "twitter:image"
            }:
                refs.append(node.attrs.get("content", ""))
            for ref in filter(None, refs):
                url = urlsplit(ref)
                if url.netloc and url.netloc != "mynotwo.github.io":
                    continue
                if url.scheme and url.scheme not in {"http", "https"}:
                    continue
                target = (root / unquote(url.path).lstrip("/")) if url.path.startswith("/") else path.parent / unquote(url.path)
                if not url.path:
                    target = path
                if target.is_dir():
                    target /= "index.html"
                assert target.is_file(), (path, ref, "missing target")
                if url.fragment and target in all_docs:
                    target_ids = {n.attrs.get("id") for n in all_docs[target].find()}
                    assert unquote(url.fragment) in target_ids, (path, ref, "missing anchor")
        html = next(doc.find("html"))
        for article in doc.find("article"):
            if "lang" in article.attrs:
                assert html.attrs["lang"] == article.attrs["lang"], (path, "document language")
    print("PASS all", len(all_docs), "HTML pages: local targets, anchors, IDs, mobile link names and article language")

    manifest = json.loads((root / "images/site.webmanifest").read_text())
    assert manifest["name"] == manifest["short_name"] == "Yu Mao"
    for icon in manifest["icons"]:
        path = root / icon["src"].lstrip("/")
        assert path.is_file(), icon
        assert mimetypes.guess_type(path)[0] == icon["type"], icon
    for page in ("photos/index.html", "blog/index.html"):
        buttons = list(docs[page].find("button", "filter-btn"))
        assert sum(b.attrs.get("aria-pressed") == "true" for b in buttons) == 1
        assert all(b.attrs.get("aria-pressed") in {"true", "false"} for b in buttons)
    dialog = next(docs["photos/index.html"].find(cls="photo-lightbox"))
    assert dialog.attrs["aria-label"] and dialog.attrs["aria-describedby"]
    print("PASS manifest, filter selection states and named photo dialog")

    reliability = all_docs[root / "agent-reliability/index.html"]
    intentcap = next(n for n in reliability.find("article") if "IntentCap" in n.text())
    assert "Best Paper Award" not in intentcap.text()
    bench = all_docs[root / "kvcache-bench/index.html"]
    template = json.loads(next(n for n in bench.find("script") if n.attrs.get("type") == "__bundler/template").text())
    matrix = json.loads((root / "kvcache-bench/kv-matrix.json").read_text())
    values = [row["bf16"]["KV"] for row in matrix["data"].values()]
    methods = matrix["methods"]
    median = lambda name: statistics.median(row[methods.index(name)] for row in values)
    assert f"{len(values)}-point repeated-input BF16 matrix" in template
    assert f"{median('bytesplit+zstd-1'):.2f}× median ratio versus {median('raw_zstd-1'):.2f}×" in template
    best = lambda prefix: statistics.median(max(row[i] for i, m in enumerate(methods) if m.startswith(prefix)) for row in values)
    assert f"{best('raw_'):.2f}× for raw codecs and {best('pipeline_'):.2f}× for structure-aware methods" in template
    assert "All averages the five input types; selecting one shows that input." in template
    assert "Median compression ratio per method and context length." not in template
    print("PASS project award label and benchmark explanations against source matrix")


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
