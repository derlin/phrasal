from typing import List

from bs4 import BeautifulSoup
from get_html.env_defined_get import do_get

from . import link_utils


def extract_links(url: str) -> List[str]:
    resp = do_get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # see https://stackoverflow.com/a/22800287/2667536
    # kill all script and style elements
    for script in soup(['script', 'style', 'form']):
        script.decompose()  # rip it out

    links = (a.get('href') for a in soup.find_all('a', href=True))
    return [l for l in link_utils.process_links(url, links)]