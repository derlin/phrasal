from phrasal.tools import *

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    res = JustextCrawler().crawl(args.url)
    text = normalize_text(res.text)
    split = MocySplitter().split(text)
    filter = PatternSentenceFilter()

    for l in split:
        print(['x', "*"][int(filter.is_valid(l))], l)
