"""Collect the public Scholar profile with bounded requests and fail-closed parsing."""

import argparse
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children).strip()

    def find(self, *, id=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if ((id is not None and child.attrs.get("id") == id)
                        or (cls is not None and cls in child.attrs.get("class", "").split())):
                    found.append(child)
                found.extend(child.find(id=id, cls=cls))
        return found


class ProfileHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_profile(page, scholar_id, previous):
    parser = ProfileHTML()
    parser.feed(page)
    root = parser.root
    names = root.find(id="gsc_prf_in")
    tables = root.find(id="gsc_rsb_st")
    more = root.find(id="gsc_bpf_more")
    if len(names) != 1 or len(tables) != 1 or len(more) != 1:
        raise ValueError("Not a complete Scholar profile (blocked page or changed markup)")
    if "disabled" not in more[0].attrs:
        raise ValueError("Profile exceeds one page; refusing a partial publication snapshot")
    if previous.get("scholar_id") != scholar_id:
        raise ValueError("Previous snapshot belongs to a different Scholar profile")
    values = [int(n.text().replace(",", "")) for n in tables[0].find(cls="gsc_rsb_std")]
    if len(values) != 6:
        raise ValueError("Expected all six Scholar citation metrics")
    publications = {}
    for row in root.find(cls="gsc_a_tr"):
        title, = row.find(cls="gsc_a_at")
        citation, = row.find(cls="gsc_a_ac")
        year, = row.find(cls="gsc_a_y")
        key, = parse_qs(urlparse(title.attrs["href"]).query)["citation_for_view"]
        if not key.startswith(scholar_id + ":") or key in publications:
            raise ValueError("Unexpected or duplicate publication identifier")
        publication = dict(previous.get("publications", {}).get(key, {}))
        publication.update(author_pub_id=key, container_type="Publication",
                           source="AUTHOR_PUBLICATION_ENTRY", filled=False,
                           num_citations=int(citation.text().replace(",", "") or "0"))
        publication["bib"] = dict(publication.get("bib", {}), title=title.text())
        if year.text():
            publication["bib"]["pub_year"] = year.text()
        if citation.attrs.get("href"):
            href = urljoin("https://scholar.google.com", citation.attrs["href"])
            publication["citedby_url"] = href
            publication["cites_id"] = parse_qs(urlparse(href).query).get("cites", [""])[0].split(",")
        else:
            publication.pop("citedby_url", None)
            publication.pop("cites_id", None)
        publications[key] = publication
    if not publications:
        raise ValueError("No publications found; refusing to overwrite existing data")
    years = [n.text() for n in root.find(cls="gsc_g_t")]
    counts = [int(n.text().replace(",", "")) for n in root.find(cls="gsc_g_al")]
    if not years or len(years) != len(counts) or len(set(years)) != len(years):
        raise ValueError("Incomplete annual citation chart")
    author = dict(previous)
    author.update(zip(("citedby", "citedby5y", "hindex", "hindex5y", "i10index", "i10index5y"), values))
    author.update(name=names[0].text(), publications=publications,
                  cites_per_year=dict(zip(years, counts)),
                  updated=datetime.now(timezone.utc).isoformat())
    return author


def collect(scholar_id, previous_path, output_dir):
    url = "https://scholar.google.com/citations?" + urlencode(
        {"user": scholar_id, "hl": "en", "pagesize": 100})
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"})
    # HTTP errors and network timeouts propagate; never replace data with an error page.
    with urlopen(request, timeout=30) as response:
        page = response.read().decode(response.headers.get_content_charset() or "utf-8")
    previous = json.loads(Path(previous_path).read_text())
    author = parse_profile(page, scholar_id, previous)
    author["source_url"] = url
    shield = {"schemaVersion": 1, "label": "citations", "message": str(author["citedby"])}
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for name, data in (("gs_data.json", author), ("gs_data_shieldsio.json", shield)):
        temporary = output / (name + ".tmp")
        temporary.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        temporary.replace(output / name)
    print(f"Verified {author['name']}: {author['citedby']} citations, "
          f"{len(author['publications'])} publications, updated {author['updated']}")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--previous", required=True)
    cli.add_argument("--output", required=True)
    args = cli.parse_args()
    collect(os.environ["GOOGLE_SCHOLAR_ID"], args.previous, args.output)
