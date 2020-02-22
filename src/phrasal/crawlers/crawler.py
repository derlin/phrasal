"""
A crawler that uses BeautifulSoup to extract text and links.
"""
import logging
from typing import Generator, Tuple, List

import requests
from bs4 import BeautifulSoup

from .link_utils import process_links
from ..interfaces import ICrawler, CrawlError, CrawlResults

# suppress warning for invalid SSL certificates
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#: Headers passed with each request
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'}

#: Timeout used in requests.get
GET_TIMEOUT = 60

logger = logging.getLogger(__name__)


class Crawler(ICrawler):
    """
    A basic crawler implemented using `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_.

    Text is extracted by concatenating all pieces of text (except CSS and script)
    into one string using a space separator (no newlines).


    .. warning::

        This crawler implementation will return the page's textual content in one bulk, with no newlines characters.
        Consequently, results won't be exploitable without a clever
        :py:class:`~swisstext.cmd.scraping.interfaces.ISplitter` (recall that the default implementation split text
        based on newlines...) such as the :py:class:`~swisstext.cmd.scraping.punkt_splitter.PunktSplitter`.

    .. todo::

        Try using just the response.text from requests to get a proper encoding ?
    """

    def __init__(self, joiner=' '):
        self.joiner = joiner  # used to join text chunks

    def crawl(self, url: str, ignore_links=False, **kwargs) -> CrawlResults:
        """Extract links and text from a URL."""
        soup, content = self.get_soup(url)
        # get links first, as extract_text_blocks is destructive
        links = None if ignore_links else self.extract_links(url, soup)
        text_blocks = self.extract_text_blocks(soup)
        return CrawlResults(
            text=self.joiner.join(text_blocks),
            links=links)

    @classmethod
    def get_content(cls, url) -> Tuple[bytes, str]:
        """
        Get the raw content from a URL (as a string), with the response encoding as reported by the requests module.
        Exceptions may be raised if:
        * an error occurs during the GET request (timeout, decoding issue, too many redirects, etc.)
        * the content-type is not of a supported type (namely html or text)
        * the response body is empty
        """
        try:
            # ignore SSL certificates
            resp = requests.get(url, verify=False, stream=True, headers=DEFAULT_HEADERS, timeout=GET_TIMEOUT)
            content = resp.content  # trigger content decoding to catch ContentDecodingError as well
        except Exception as e:
            # here, don't use from_ex so we can trim the error message
            raise CrawlError(name=e.__class__.__name__, message=str(e)[:50])

        # try to avoid encoding issues
        # see https://stackoverflow.com/a/45643551/2667536
        # Note: the encoding might be wrong if the content-type is declaring a charset with
        # uppercase, for example 'text/html; Charset=xxx'. I posted an issue, see
        # https://github.com/requests/requests/issues/4748
        ctype = resp.headers.get('content-type', '').lower()
        if not ('html' in ctype or 'text/plain' in ctype):
            raise CrawlError(name='CtypeError', message=f'{url} not HTML (ctype={ctype})')

        # also test the .text, so that we avoid returning content with only unprintable chars, e.g. b'\xef\xbb\xbf'
        if len(content) == 0 or len(resp.text.strip()) == 0:
            raise CrawlError(name=f'EmptyDocumentError', message='Content is empty.')

        # the resp.encoding is an educated guess about the encoding of the response based on the HTTP headers
        return content, resp.encoding

    @classmethod
    def get_soup(cls, url) -> Tuple[BeautifulSoup, bytes]:
        """Get a :py:class:`~bs4.BeautifulSoup` object from a URL (HTML)."""
        content, _ = cls.get_content(url)
        # here, the encoding should be ok, since bs4 uses the decode/replace strategy by default
        return BeautifulSoup(content, 'html.parser'), content

    @classmethod
    def extract_text_blocks(cls, soup) -> Generator[str, None, None]:
        """
        Get text blocks from a :py:class:`~bs4.BeautifulSoup` object.

        .. warning::

            This method is destructive, as it will first remove script, style and forms
            from the HTML/soup object !

        .. todo::

            Find a way to avoid altering the soup object.. ?
        """
        # see https://stackoverflow.com/a/22800287/2667536
        # kill all script and style elements
        for script in soup(['script', 'style', 'form']):
            script.decompose()  # rip it out

        return soup.stripped_strings

    @classmethod
    def extract_links(cls, url, soup) -> List[str]:
        """
        Get all links from a soup (a href only).
        Note that links will be resolved (relative to absolute) and filtered (non-HTML removed).
        """
        links = (a.get('href') for a in soup.find_all('a', href=True))
        return [l for l in process_links(url, links)]

def main():
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='+')
    parser.add_argument('-j', '--joiner', default=' ')
    parser.add_argument('-l', '--links', default=False, action='store_true',
                        help='If set, outputs links instead of the text.')
    args = parser.parse_args()

    crawler = Crawler(joiner=args.joiner)

    for url in args.url:
        try:
            res = crawler.crawl(url)
            print(f'=== from URL {url}', file=sys.stderr)
            if args.links:
                print('\n'.join(res.links))
            else:
                print(res.text)
        except Exception as e:
            print(e)