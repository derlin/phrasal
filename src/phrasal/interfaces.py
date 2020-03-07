"""
This module defines interfaces for each tool or decision maker used in the scraping process.
This makes it easy to test new ways or to tune one aspect of the scraper while keeping most of the code unchanged.

See the :py:mod:`swisstext.cmd.scraping.tools` module for implementations.
"""
from typing import List, Union


class IHtmlConverter:
    """
    [ABSTRACT] This tool is in charge of extracting text from HTML.
    """

    def to_text(self, html: Union[str, bytes], encoding=None, **kwargs) -> str:
        """[ABSTRACT] Should extract the text from HTML."""
        return ''


class INormalizer:
    """
    A normalizer should take a [long] text (extracted from a web page) and clean it in a consistant way.
    For example: uncurling quotes, normalizing punctuation, fix unicode, etc.
    The default implementation just return the text as-is.
    """

    def normalize(self, text: str, **kwargs) -> str:
        """This should be overriden. The default implementation just returns the text as-is."""
        return text

    def normalize_all(self, texts: List[str], **kwargs) -> List[str]:
        """Calls normalize on each element of text."""
        return [self.normalize(t, **kwargs) for t in texts]


class ISplitter:
    """
    A splitter should take a [long] text (extracted from a web page) and split it into well-formed sentences.
    The default implementation just splits on the newline character.
    """

    def split(self, text: str, **kwargs) -> List[str]:
        """This should be overriden. The default implementation just splits on newlines."""
        return text.splitlines()

    def split_all(self, texts: List[str], **kwargs) -> List[str]:
        """Takes a list of texts and returns a list of sentences (see :py:meth:`split`)."""
        return [splitted for t in texts for splitted in self.split(t, **kwargs)]


class IFilterer:
    """
    A sentence filter should be able to tell if a given sentence is well-formed (i.e. valid) or not.
    """

    def is_valid(self, sentence: str, **kwargs) -> bool:
        """This should be overriden. The default implementation just returns true."""
        return True

    def filter(self, sentences: List[str], **kwargs) -> List[str]:
        """Filter a list of sentences by calling :py:meth:`ISentenceFilter.is_valid` on each element."""
        return [s for s in sentences if self.is_valid(s, **kwargs)]
