# Local check loop; .github/workflows/ci.yml runs `make check` on pull requests.
# Needs `bundle install` once (see README for the Ruby version).

.PHONY: build check

build:
	bundle exec jekyll build

check: build
	python3 scripts/check_profile_pages.py _site
	python3 -m unittest discover -s google_scholar_crawler -p test_main.py
