# Local check loop; .github/workflows/ci.yml runs `make check` on pull requests.
# Needs `bundle install` once (see README for the Ruby version).

.PHONY: build check og-cards

build:
	bundle exec jekyll build

check: build
	python3 scripts/check_profile_pages.py _site
	python3 -m unittest discover -s google_scholar_crawler -p test_main.py

# Share cards: _data/og_cards.yml -> images/og/*.png (needs Chrome, see the script).
og-cards: build
	python3 scripts/build_og_cards.py
