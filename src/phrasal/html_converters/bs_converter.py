import re
from typing import Union

from bs4 import BeautifulSoup

from phrasal.interfaces import IHtmlConverter


class BsConverter(IHtmlConverter):

    def __init__(self, joiner=' '):
        self.joiner = joiner

    def to_text(self, html: Union[str, bytes], joiner=None, **kwargs) -> str:
        joiner = joiner if joiner is not None else self.joiner
        soup = BeautifulSoup(html, 'html.parser')

        # see https://stackoverflow.com/a/22800287/2667536
        # kill all script and style elements
        for script in soup(['script', 'style', 'form', 'code']):
            script.decompose()  # rip it out

        # strip all \n, which are sometimes used instead of spaces
        # - https://docs.streamlit.io/api.html?highlight=exception#streamlit.exception
        sents = (re.sub(' +', ' ', s.replace('\n', ' ')) for s in soup.stripped_strings)
        return joiner.join(sents)

    def __str__(self):
        return f'{self.__class__.__name__}({vars(self)})'.replace("'", '')

def main():
    import argparse, sys
    import requests
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', nargs='+', default=[])
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=None)
    parser.add_argument('-j', '--joiner', default=' ')
    args = parser.parse_args()

    jt = BsConverter(joiner=args.joiner)

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
