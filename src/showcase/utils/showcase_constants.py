from phrasal import *


class Pipeline:
    converter = JustextConverter(keep_bad=True)
    splitter = MocySplitter()
    filter = PatternSentenceFilter()
    normalizer = Normalizer()