from phrasal import link_utils
import pytest


@pytest.mark.parametrize(
    'link,expected',
    [('#hello', 'http://example.ch/page/1'),
     ('2', 'http://example.ch/page/2'),
     ('../other', 'http://example.ch/other'),
     ('/', 'http://example.ch/'),
     ('?q=1#something', 'http://example.ch/page/1?q=1'),
     ('https://other.com', 'https://other.com')]
)
def test_relative_urls(link, expected):
    base_url = 'http://example.ch/page/1'
    fixed, _ = link_utils.fix_url(link, base_url=base_url)
    assert fixed == expected
    fixed, _ = link_utils.fix_url(link, base_url=base_url + '/')
    assert fixed == expected


@pytest.mark.parametrize(
    'link',
    [
        # non-HTTP(s)
        'mailto:lala@example.com',
        'ftp://123.32.23.0/resources',
        # js
        'javascript: return false',
        # relative URLs and anchors
        '../hello',
        '#x',

    ]
)
def test_excluded(link):
    fixed, ok = link_utils.fix_url(link)
    assert not ok


def test_duplicates():
    results = list(link_utils.process_links(base_url='http://example.ch/page/1', links=[
        # same page/1 => ignored
        'http://example.ch/page/1',
        'http://example.ch/page/1?#hello',
        '1',
        '../page/1',
        '#',
        '1/#',
        # page/2 => added
        '2',
        'http://example.ch/page/2',
        'http://example.ch/page/2/',
    ]))

    assert len(results) == 1
    assert results[0] == 'http://example.ch/page/2'
