from phrasal import *


class Pipeline:
    crawler = JustextCrawler(keep_bad=True)
    splitter = MocySplitter()
    filter = PatternSentenceFilter()
    normalizer = Normalizer()


