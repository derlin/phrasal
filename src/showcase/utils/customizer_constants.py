from phrasal import *
from phrasal.interfaces import *

# the first in impl is the default
class CustomizerConstants:

    tools = dict(
        crawlers=dict(
            impl={
                'JustextCrawler': JustextCrawler(),  # keep_bad=True
                'Crawler': Crawler()
            },
            options={
                'JustextCrawler': [('keep_bad', 'keep everything', False)]
            }
        ),
        normalizers=dict(
            impl={
                'Normalizer': Normalizer(),  # fix_encoding=False, strip_emojis=False
                'None': INormalizer(),
            }, options={
                'Normalizer': [('fix_encoding', 'Fix encoding', False), ('strip_emojis', 'Strip emojis', False)]
            }
        ),
        splitters=dict(
            impl={
                'MocySplitter': MocySplitter(),  # more=True
                'MosesSplitter': MosesSplitter(),
                'None': ISplitter(),
            },
            options={
                'MocySplitter': [('more', 'break on :;', True)]
            }
        ),
        filterers=dict(
            impl={
                'PatternSentenceFilter': PatternSentenceFilter(),
                'None': IFilterer(),
            },
            options={}
        )
    )