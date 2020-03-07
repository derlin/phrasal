from phrasal import *
from phrasal.interfaces import *

# the first in impl is the default
class CustomizerConstants:

    tools = dict(
        converters=dict(
            impl={
                'JustextConverter': JustextConverter(),  # keep_bad=True
                'BsConverter': BsConverter()
            },
            options={
                'JustextConverter': [('keep_bad', 'keep everything', False)]
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
                'MocySplitter': [('more', 'break on :;', True), ('keep_newlines', 'preserve new lines', True)]
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