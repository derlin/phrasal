# Phrasal

## Forewords 

### What is it ?

Phrasal is a library of tools to help gather meaningful, proper sentences from websites. 

Well, at least if used together. Each tool has a value of its own. 
For example, the `Normalizer` (my favorite!) is very useful for NLP, when you have a crappy text corpus you need to clean.
The `Crawler` is good when you need the raw text of a web page, properly decoded in UTF-8.
The `MocySplitter` is a nice alternative to Moses when you need to cleverly split a stream of text into sentences, one per line. 
Etc.

### Why was it developed ?

I have been working on a project lately, called [SwissText](https://github.com/derlin/swisstext) that gathers Swiss German sentences from scraping the Internet (no kidding, see the LREC 2020 publication on [arXiv](https://arxiv.org/abs/1912.00159)).
To do so, I had to build upon existing tools and develop some of my own. 
While they were initially for Swiss German, I figured that it would maybe be useful in other contexts, hence this repo which is a stripped-down version of some of the SwissText modules.

### How does it work ?

This repo contains implementations of four types of tools, which constitute together a pipeline:

1. *crawler*: extract (main) text from webpages;
2. *normalizer*: normalize the raw text, including the encoding, quotes, spaces, etc.;
3. *splitter*: split the text into chunks (potential sentences);
4. *filterer*: filter chunks to keep only "proper" sentences.

For each step, I propose one or more implementations.

## Tools available

**Crawlers**

* `phrasal.Crawler` \
A "crawler" built upon `BeautifulSoup` that exact text found on the page. 
It deals cleverly with encodings and always delivers text in UTF-8.
As a bonus, it is able to find, resolve (i.e. make absolute) and return all "text links" (links pointing to other web pages with potential text, so no images, scripts or the like).

* `phrasal.JustextCrawler` \
a crawler that in addition to what the basic `Crawler` does, uses `justext` to remove boilerplate content and preserve mainly text containing full sentences.

**Normalizers**

* `phrasal.Normalizer`, or simply `phrasal.normalize_text`\
Normalize some text (using a serie of homemade regexes), including: normalize spaces, replace combining diacritics by the accented letter codepoints and strip leftovers, normalize dashes and quotemarks, replace non-breakable spaces with regular ones, etc. \
It can also try to fix encoding errors (see [`ftfy`](https://pypi.org/project/ftfy/)) and strip most unicode emoji symbols.

**Splitters**

* `phrasal.MosesSplitter`\
Moses' splitter [`split-sentences.perl`](https://github.com/moses-smt/mosesdecoder/blob/master/scripts/ems/support/split-sentences.perl) completely rewritten in Python. It thus perfectly mimics the behavior, while being 5x faster than calling perl from Python (approach taken by [`MosesTokenizer`](https://pypi.org/project/mosestokenizer/) for example).
* `phrasal.MocySplitter`\
An improvement upon `MosesSplitter`, which: deals more efficiently with lowercase (people are lazy on the Web), try to preserve links, can split on `:` or `;` (optional), etc.

**Filterers**

* `phrasal.PatternSentenceFilter`\
A filterer based on a list of simple rules a proper sentence should respect, such as "*at least five words*", "*no S P E L L E D* words", etc. \
What is *awesome* ? The rules are expressed in a (homemade) YAML-based syntax and are highly customizable. If you don't like the behavior, have a look at `pattern_sentence_filter.yaml` and try writing your own set of rules !


**link_utils**

The `phrasal.link_utils` module is a simple utility to process href links found on a page. It will resolve relative links
(given a base URL), remove duplicates, strip anchors and exclude non-HTTP/HTTPs links.

## How to use

Install the library using:
```bash
# regular install, one of:
python setup.py install 
pip install .

# for development, one of:
python setup.py develop
pip install -e .
pip install -e .[showcase] # for streamlit
```

### As a library

```python
from phrasal import *
```
Done.

### From the command line

Each tool contains a command line interface with different arguments. Discover it by typing:
```bash
python -m phrasal --help
```
```bash
python -m phrasal --help
Call one of the tools from the command line. Usage: 
   classname [other arguments specific to classname]|[-h]

Allowed classname arguments:
 - Crawler
 - JustextCrawler
 - PatternSentenceFilter
 - MocySplitter
 - MosesSplitter
 - Normalizer
```
Here are some examples:
```bash
python -m phrasal Crawler --links https://loremipsum.io/
=== from URL https://loremipsum.io/
https://www.facebook.com/sharer/sharer.php
https://plus.google.com/share?url=https://loremipsum.io/
[...]
```
```bash
python -m phrasal PatternSentenceFilter -i <(echo 'not-a-sentence\nYEAH !!!\nCet outil fonctionne très bien, je l’utilise tous les jours.')
Cet outil fonctionne très bien, je l’utilise tous les jours.
```
```bash
python -m phrasal Normalizer -i raw_text.txt -o clean_text.txt
```

### I just need one tool...

No problem, each tool is more or less independent. 
You may want to simplify the code a bit (e.g. remove the interface inheritance, transform classes into static scripts, I don't know), but I hope the source code is self-explaining. 

## License

This work is licensed under Apache 2.0, so you can basically do anything with it. 

*However*, I would **really enjoy** it if you **credit me** somehow, either by citing my name, send me an email to say hi (I get lonely sometime, may be nice to chat), leave a star on GitHub, or any other way you think may give me strength to keep doing open-source :blush:.

## Related resources

* [SwissText](https://github.com/swisstext)
* [SwissTranslation project page](https://icosys.ch/swisscrawl)
* :octopus::octopus::octopus::octopus::octopus::octopus::octopus::octopus: (I just love octopuses)
* [Personal website](https://derlin.ch)

## TODO

* twitter is now fully powered by JS, so text can't be accessed anymore... Find a way to circumvent that / use the old version?

TODO: add some usecases, such as finding links, cleaning a text file, etc. add language support information 