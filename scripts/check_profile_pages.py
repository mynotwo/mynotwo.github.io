"""Smoke-check built profile pages: python3 scripts/check_profile_pages.py _site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
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
    # A publication without a paper URL must keep a readable, non-empty title.
    fallback = next(c for c in pubs if "Parallel-SA:" in c.text())
    assert not list(next(fallback.find(cls="paper-title")).find("a"))
    print("PASS publication links and missing-URL fallback")

    home = docs["index.html"]
    ids = [n.attrs["id"] for n in home.find() if "id" in n.attrs]
    assert len(ids) == len(set(ids)), "Duplicate homepage IDs"
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


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
