import copy
import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from main import collect, parse_profile
from publish import refresh


PROFILE = '''<div id="gsc_prf_in">Yu Mao</div><table id="gsc_rsb_st"><tr>
<td class="gsc_rsb_std">295</td><td class="gsc_rsb_std">295</td>
<td class="gsc_rsb_std">9</td><td class="gsc_rsb_std">9</td>
<td class="gsc_rsb_std">8</td><td class="gsc_rsb_std">8</td></tr></table>
<table><tr class="gsc_a_tr"><td><a class="gsc_a_at"
href="/citations?citation_for_view=Iw3bTCAAAAAJ:paper">Paper &amp; Systems</a></td>
<td><a class="gsc_a_ac gs_ibl" href="/scholar?cites=123">1,234</a></td>
<td class="gsc_a_y"><span>2022</span></td></tr></table>
<span class="gsc_g_t">2026</span><span class="gsc_g_al">292</span>
<button id="gsc_bpf_more" disabled>Show more</button>'''
PREVIOUS = {"scholar_id": "Iw3bTCAAAAAJ", "affiliation": "ByteDance", "citedby": 284,
            "publications": {"Iw3bTCAAAAAJ:paper": {"bib": {"journal": "Existing venue"}}}}


class ScholarTests(unittest.TestCase):
    def parse(self, page=PROFILE, previous=PREVIOUS):
        return parse_profile(page, 'Iw3bTCAAAAAJ', previous)

    def test_official_metrics_are_independent_of_chart_and_paper_sums(self):
        previous = copy.deepcopy(PREVIOUS)
        author = self.parse(previous=previous)
        self.assertEqual(author['citedby'], 295)
        self.assertEqual(author['cites_per_year'], {'2026': 292})
        self.assertEqual(author['affiliation'], 'ByteDance')
        paper = author['publications']['Iw3bTCAAAAAJ:paper']
        self.assertEqual(paper['num_citations'], 1234)
        self.assertEqual(paper['bib'], {'title': 'Paper & Systems', 'journal': 'Existing venue', 'pub_year': '2022'})
        self.assertEqual(paper['cites_id'], ['123'])
        self.assertEqual(previous, PREVIOUS)

    def test_uncited_paper_and_missing_year(self):
        author = self.parse(PROFILE.replace('>1,234</a>', '></a>').replace('<span>2022</span>', ''))
        self.assertEqual(author['publications']['Iw3bTCAAAAAJ:paper']['num_citations'], 0)

    def test_reject_blocked_incomplete_duplicate_or_wrong_profile(self):
        start = PROFILE.index('<tr class="gsc_a_tr"')
        row = PROFILE[start:PROFILE.index('</tr>', start) + 5]
        for page in ['<html>Sorry, unusual traffic</html>',
                     PROFILE.replace(' disabled', ''),
                     PROFILE.replace('<td class="gsc_rsb_std">8</td>', '', 1),
                     PROFILE.replace('</table>\n<span', row + '</table>\n<span'),
                     PROFILE.replace('citation_for_view=Iw3bTCAAAAAJ:', 'citation_for_view=other:'),
                     PROFILE.replace('<span class="gsc_g_al">292</span>', '')]:
            with self.subTest(page=page), self.assertRaises((ValueError, KeyError)):
                self.parse(page)
        with self.assertRaises(ValueError):
            self.parse(previous=dict(PREVIOUS, scholar_id='other'))

    def test_403_and_timeout_preserve_existing_files(self):
        for error in [HTTPError('https://scholar.google.com', 403, 'Forbidden', {}, None),
                      TimeoutError('timed out')]:
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'gs_data.json'
                path.write_text(json.dumps(PREVIOUS))
                before = path.read_bytes()
                with patch('main.urlopen', side_effect=error), self.assertRaises(type(error)):
                    collect('Iw3bTCAAAAAJ', path, folder)
                self.assertEqual(path.read_bytes(), before)
                self.assertFalse((Path(folder) / 'gs_data_shieldsio.json').exists())

    def test_invalid_success_response_preserves_data(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'gs_data.json'
            path.write_text(json.dumps(PREVIOUS))
            before = path.read_bytes()
            with patch('main.urlopen') as request:
                response = request.return_value.__enter__.return_value
                response.read.return_value = b'<html>Consent or CAPTCHA</html>'
                response.headers.get_content_charset.return_value = 'utf-8'
                with self.assertRaises(ValueError):
                    collect('Iw3bTCAAAAAJ', path, folder)
            self.assertEqual(path.read_bytes(), before)

    def test_publication_stops_before_any_write_when_collection_fails(self):
        responses = [{'object': {'sha': 'old'}}, {'tree': {'sha': 'tree'}},
                     {'content': base64.b64encode(json.dumps(PREVIOUS).encode()).decode()}]
        with patch('publish.api', side_effect=responses) as api, \
                patch('publish.collect', side_effect=TimeoutError), self.assertRaises(TimeoutError):
            refresh()
        self.assertEqual(api.call_count, 3)

    def test_publishes_two_files_atomically_without_force(self):
        data = json.dumps({'citedby': 295}).encode()
        responses = [{'object': {'sha': 'old'}}, {'tree': {'sha': 'tree'}},
                     {'content': base64.b64encode(json.dumps(PREVIOUS).encode()).decode()},
                     {'sha': 'newtree'}, {'sha': 'newcommit'}, {},
                     {'content': base64.b64encode(data).decode()}]

        def collected(scholar_id, previous, folder):
            (folder / 'gs_data.json').write_bytes(data)
            (folder / 'gs_data_shieldsio.json').write_text('{"message":"295"}')

        with patch('publish.api', side_effect=responses) as api, \
                patch('publish.collect', side_effect=collected):
            self.assertEqual(refresh(), 'newcommit')
        calls = api.call_args_list
        self.assertEqual(len(calls[3].args[2]['tree']), 2)
        self.assertEqual(calls[4].args[2]['parents'], ['old'])
        self.assertEqual(calls[5].args[2], {'sha': 'newcommit', 'force': False})


if __name__ == '__main__':
    unittest.main()
