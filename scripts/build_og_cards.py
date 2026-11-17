#!/usr/bin/env python3
"""Render the share cards in _data/og_cards.yml into images/og/<name>.png.

    make og-cards                                  # builds _site first
    python3 scripts/build_og_cards.py [name ...]   # only the named cards

Serves the built _site on a local port and screenshots
/tools/og-card.html?card=<name> at 1200x630 with headless Chrome. Set CHROME
to the browser binary when it is not at the macOS default path.
"""

import functools
import http.server
import json
import os
import re
import subprocess
import sys
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(REPO, "_site")
OUT = os.path.join(REPO, "images", "og")
CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def card_names():
    # The built template page carries the card list Jekyll read from the data file.
    page = open(os.path.join(SITE, "tools", "og-card.html"), encoding="utf-8").read()
    cards = json.loads(re.search(r"var cards = (\[.*\]);", page).group(1))
    return [card["name"] for card in cards]


def main(wanted):
    names = card_names()
    unknown = sorted(set(wanted) - set(names))
    if unknown:
        sys.exit(f"Not in _data/og_cards.yml: {', '.join(unknown)}")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Quiet, directory=SITE))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    os.makedirs(OUT, exist_ok=True)
    for name in wanted or names:
        target = os.path.join(OUT, name + ".png")
        subprocess.run(
            [CHROME, "--headless", "--hide-scrollbars", "--force-device-scale-factor=1",
             "--window-size=1200,630", "--virtual-time-budget=4000",
             "--screenshot=" + target,
             f"http://127.0.0.1:{server.server_port}/tools/og-card.html?card={name}"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("wrote", os.path.relpath(target, REPO))
    server.shutdown()


if __name__ == "__main__":
    main(sys.argv[1:])
