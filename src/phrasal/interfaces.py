"""
This module defines interfaces for each tool or decision maker used in the scraping process.
This makes it easy to test new ways or to tune one aspect of the scraper while keeping most of the code unchanged.

See the :py:mod:`swisstext.cmd.scraping.tools` module for implementations.
"""
from typing import List


class CrawlError(Exception):
    """This wrapper should be used for any exception that arise during scraping."""

    def __init__(self, name='CrawlError', message=''):
        super().__init__(f'{name}: {message}')
        self.name = name
        self.message = message

    @classmethod
    def from_ex(cls, e: Exception):
        """Create an exception using the original exception name and repr"""
        return cls(name=e.__class__.__name__, message=str(e))


class CrawlResults:
    """Holds the results of a page crawl."""

    def __init__(self, text: str, links: List[str]):
        self.text: str = text
        """the clean text found in the page, free of any structural marker such as HTML tags, etc."""
        self.links: List[str] = links
        """A list of interesting links found in the page. By interesting, we mean:
        * no duplicates
        * different from the current page URL (no anchors !)
        * if possible, no link pointing to unparseable resources (zip files, images, etc.)
        The method :py:meth:`swisstext.cmd.link_utils.filter_links` is available to do the filtering. 
        """

    @classmethod
    def empty(cls):
        return cls(text='', links=[])


class ICrawler:
    """
    [ABSTRACT] This tool is in charge of crawling a page. More specifically, it should be able to:
    1. extract the text of the page (stripped of any HTML or other structural clue),
    2. extract links pointing to other pages
    """

    def crawl(self, url: str, ignore_links=False) -> CrawlResults:
        """[ABSTRACT]
        Should crawl the page and extract the text and the links into a :py:class:`ICrawler.CrawlResults` instance."""
        return CrawlResults.empty()


class INormalizer:
    """
    A normalizer should take a [long] text (extracted from a web page) and clean it in a consistant way.
    For example: uncurling quotes, normalizing punctuation, fix unicode, etc.
    The default implementation just return the text as-is.
    """

    def normalize(self, text: str) -> str:
        """This should be overriden. The default implementation just returns the text as-is."""
        return text

    def normalize_all(self, texts: List[str]) -> List[str]:
        """Calls normalize on each element of text."""
        return [self.normalize(t) for t in texts]


class ISplitter:
    """
    A splitter should take a [long] text (extracted from a web page) and split it into well-formed sentences.
    The default implementation just splits on the newline character.
    """

    def split(self, text: str) -> List[str]:
        """This should be overriden. The default implementation just splits on newlines."""
        return text.splitlines()

    def split_all(self, texts: List[str]) -> List[str]:
        """Takes a list of texts and returns a list of sentences (see :py:meth:`split`)."""
        return [splitted for t in texts for splitted in self.split(t)]


class IFilterer:
    """
    A sentence filter should be able to tell if a given sentence is well-formed (i.e. valid) or not.
    """

    def is_valid(self, sentence: str) -> bool:
        """This should be overriden. The default implementation just returns true."""
        return True

    def filter(self, sentences: List[str]) -> List[str]:
        """Filter a list of sentences by calling :py:meth:`ISentenceFilter.is_valid` on each element."""
        return [s for s in sentences if self.is_valid(s)]
