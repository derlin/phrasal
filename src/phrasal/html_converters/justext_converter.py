"""
This module relies on `JusText <https://github.com/miso-belica/jusText>`_ for text extraction.

To get a feel, try the `online demo of the original JustText <http://nlp.fi.muni.cz/projects/justext/>`_.

.. note::

    * usually, jusText uses ``''`` (empty string) to join text nodes inside a paragraph, thus making things like
      "*One sentence.Second sentence*" likely. Here, we always use a space to join, then normalize the spaces.
    * justext will throw an error on an empty document content.

"""
import logging
import re
from typing import Union

from bs4 import UnicodeDammit
import justext
from ..interfaces import IHtmlConverter

logger = logging.getLogger(__name__)


class JustextConverter(IHtmlConverter):
    """
    An HTML converter that relies on
    `JusText <https://github.com/miso-belica/jusText>`_ to cleverly extract meaningful text from webpages.
    """

    def __init__(self, joiner='\n',
                 keep_bad=True,
                 stoplist=None,
                 stopwords_low=justext.core.STOPWORDS_LOW_DEFAULT,
                 stopwords_high=justext.core.STOPWORDS_HIGH_DEFAULT,
                 **kwargs):
        """
        Create a crawler instance.
        :param joiner: character used to join paragraphs;
        :param keep_bad: if set, keep everything.
        If unset, keep only paragraphs with a context-free class of "neargood" or "good".
        :param stoplist: see the `justText doc <https://github.com/miso-belica/jusText/blob/dev/doc/algorithm.rst>`_
        :param stopwords_low: idem
        :param stopwords_high: idem
        :param kwargs: unused
        """
        self.joiner = joiner

        if stoplist is not None:
            with open(stoplist) as f:
                self.kwargs = dict(
                    stoplist=set(l.strip() for l in f if len(l)),
                    stopwords_low=stopwords_low,
                    stopwords_high=stopwords_high)
        else:
            self.kwargs = dict(stoplist=set(), stopwords_low=0, stopwords_high=0)

        self.kwargs.update(kwargs)
        self.keep_bad = keep_bad
        logger.debug(self)

    def to_text(self, html: Union[str, bytes], joiner=None, keep_bad=None, **kwargs) -> str:
        if keep_bad is None:
            keep_bad = self.keep_bad
        if joiner is None:
            joiner = self.joiner

        try:
            # justext uses the decode/replace strategy by default, so encoding errors shouldn't happen
            # see justext core.py:DEFAULT_ENC_ERRORS ... well I don't know why, but errors are still triggered,
            # but not if I do the decoding here... maybe the encoding parameter ? Problematic URLs examples
            # - http://www.triumphowners.ch/index.php?page=Thread%3D654%3D13
            # - https://angerweit.tikon.ch/lieder/lied.php?src=folk-de%2Fsimeli
            if isinstance(html, bytes):
                dammit = UnicodeDammit(html, [None], is_html=True) # way more precise than requests
                if 'encoding' in kwargs and dammit.original_encoding != kwargs['encoding']:
                    logger.debug(f"encoding: declared={kwargs['encoding']}, dammit={dammit.original_encoding}")
                html = html.decode(encoding=dammit.original_encoding, errors='replace')
            paragraphs = justext.justext(html, **self.kwargs)
            # paragraphs = justext.justext(content, encoding=soup.original_encoding, **self.kwargs)
            text_blocks = (self._get_text(p) for p in paragraphs if keep_bad or 'good' in p.cf_class)
            return joiner.join(text_blocks)
        except Exception as e:
            if 'Document is empty' in str(e):
                return ''  # Document is empty
            else:
                raise e

    def _get_text(self, p):
        # mmhh... In justext, they join on '', such that we often have things like:
        # "end of sentence.Start of sentence".
        text = ' '.join(p.text_nodes).replace('\n', ' ')
        return re.sub(' +', ' ', text).strip()

    def __str__(self):
        return f'{self.__class__.__name__}({vars(self)})'.replace("'", '')


def main():
    import argparse, sys
    import requests
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', nargs='+', default=[])
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=None)
    parser.add_argument('-j', '--joiner', default='\n')
    parser.add_argument('-b', '--keep-bad', default=False, action='store_true',
                        help='Return all found sentences (vs "good" only).')
    args = parser.parse_args()

    jt = JustextConverter(joiner=args.joiner, keep_bad=args.keep_bad)

    if args.file:
        print(f'=== from TEXT', file=sys.stderr)
        print(jt.to_text(args.file.read()))

    for url in args.url:
        try:
            response = requests.get(url)
            text = jt.to_text(response.content)
            print(f'=== from URL {url}', file=sys.stderr)
            print(text)
        except Exception as e:
            print(e)
