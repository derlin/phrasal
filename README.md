# Phrasal

## Forewords 

### What is it ?

Phrasal is a library of tools to help gather meaningful, proper sentences from websites. 

Well, at least if used together. Each tool has a value of its own. 
For example, the `Normalizer` (my favorite!) is very useful for NLP, when you have a crappy text corpus you need to clean.
The `MocySplitter` is a nice alternative to Moses when you need to cleverly split a stream of text into sentences, one per line. 
Etc.

### Why was it developed ?

I have been working on a project lately, called [SwissText](https://github.com/derlin/swisstext) that gathers Swiss German sentences from scraping the Internet (no kidding, see the LREC 2020 publication on [arXiv](https://arxiv.org/abs/1912.00159)).
To do so, I had to build upon existing tools and develop some of my own. 
While they were initially for Swiss German, I figured that it would maybe be useful in other contexts, hence this repo which is a stripped-down version of some of the SwissText modules.

### How does it work ?

This repo contains implementations of four types of tools, which constitute together a pipeline:

1. *converter*: extract (main) text from raw HTML;
2. *normalizer*: normalize the raw text, including the encoding, quotes, spaces, etc.;
3. *splitter*: split the text into chunks (potential sentences);
4. *filterer*: filter chunks to keep only "proper" sentences.

For each step, I propose one or more implementations.

## Tools available

**HtmlConverters**

* `phrasal.BsConverter` \
A converter built upon `BeautifulSoup` that exact text found on the HTML. 
Text from code blocks, scripts or styles is ignored.
It deals cleverly with encodings and always delivers text in UTF-8.


* `phrasal.JustextConverter` \
a converter based on [`justext`](https://pypi.org/project/jusText/), that try to spot and remove boilerplate content.
By default, it only keeps "good" paragraph, that is text long enough to be a full sentences and with a low link density.

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

To get the list of links from a URL (i.e. `href` found on the page main content), use `extract_links`:
```python
import phrasal

all_links = phrasal.extract_links('https://github.com/derlin/phrasal')
```

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
import phrasal
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
 - BsConverter
 - JustextConverter
 - PatternSentenceFilter
 - MocySplitter
 - MosesSplitter
 - Normalizer
```
Here are some examples:
```bash
python -m phrasal JustextConverter -u https://icosys.ch/swisscrawl
=== from URL https://icosys.ch/swisscrawl
As part of the SwissTranslation project, SwissCrawl is a corpus of 500,000+ Swiss German (GSW)  [...]
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

## Running tests

Tests are using `tox` and `pytest`. The easiest way to run them is:
```bash
pip install tox tox-venv
tox
```

## Running the showcase

A showcase using [streamlit](https://www.streamlit.io/) is included. 
It allows you to test the full pipeline straight from your browser and also play with the different tools and options
from the **Live Customizer**. Once you found what works for you, you can simply copy-paste the code snippet generated.

Run the showcase locally by doing:
```bash
pip install streamlit
streamlit run src/showcase/lit.py
```


## License

This work is licensed under Apache 2.0, so you can basically do anything with it. 

*However*, I would **really enjoy** it if you **credit me** somehow, either by citing my name, send me an email to say hi (I get lonely sometime, may be nice to chat), leave a star on GitHub, or any other way you think may give me strength to keep doing open-source :blush:.

## Related resources

* [get-html](https://pypi.org/project/get-html/) to get raw or renderer HTML (used in this repo)
* [SwissText](https://github.com/swisstext)
* [SwissTranslation project page](https://icosys.ch/swisscrawl)
* :octopus::octopus::octopus::octopus::octopus::octopus::octopus::octopus: (I just love octopuses)
* [Personal website](https://derlin.ch)

## TODO

* add some usecases, such as finding links, cleaning a text file, etc. add language support information 