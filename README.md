# Phrasal

## Introduction 

### What is it ?

Phrasal is a library of tools to help gather meaningful, proper sentences from websites. 

### Why was it developed ?

I have been working on a project lately, called [SwissText](https://github.com/derlin/swisstext) that tries to find and gather Swiss German sentences online.
To do so, I had to build upon existing tools and develop some of my own. I figured that It would maybe be useful in other context, hence this repo which is a stripped down version of some of the SwissText modules.

### How does it work ?

This repo contains implementations of four types of tools, that constitute together a pipeline:

1. *crawler*: extract (main) text from webpages;
2. *normalizer*: normalize the raw text, including the encoding, quotes, spaces, etc.;
3. *splitter*: split the text into chunks (potential sentences);
4. *filterer*: filter chunks to keep only "proper" sentences.

For each step, I propose one or more implementations.

## Tools available

**Crawlers**

* `phrasal.Crawler`: a basic crawler built upon `BeautifulSoup` that exact all text and links found on the page. It also deals cleverly with encodings and always delivers text in UTF-8;
* `phrasal.JustextCrawler`: a crawler that in addition to what the basic `Crawler` does, uses `justext` to remove boilerplate content and preserve mainly text containing full sentences;

**Normalizers**

* `phrasal.Normalizer`, or simply `phrasal.normalize_text`: normalize the text using a mix of homemade and Moses regexes and optionally strip unicode emojis and fix encodings (using the `ftfy` library);

**Splitters**

* `phrasal.MosesSplitter`: Moses splitter `split-sentences.perl` completely rewritten in Python. It thus perfectly mimics the behavior, while being 5x faster than calling perl from Python (approach taken by `MosesTokenizer` for example);
* `phrasal.MocySplitter`: a improvement (at least in my opinion) upon `MosesSplitter`. The biggest difference is that it also deals with sentences starting with a lowercase.

**Filterers**

* `phrasal.PatternSentenceFilter`: a filter based on a list of simple rules a proper sentence should respect, such as "*at least five words*", "*no S P E L L E D* words", etc. The rules are expressed in a YAML-based syntax and completely customizable;

## How to use

### As a library

Install the library using:
```bash
python setup.py install
```

Import:
```python
from phrasal import *
```

Done.

### From the commandline

Each tool contains a commandline interface with different arguments. Discover it by typing:
```bash
python -m phrasal --help
```

Here is an example:
```bash
python -m phrasal --help
Call one of the tools from the commandline. Usage: 
   classname [other arguments specific to classname]|[-h]

Allowed classname arguments:
 - JustextCrawler
 - PatternSentenceFilter
 - MocySplitter
 - MosesSplitter
 - Normalizer
```
```bash
python -m phrasal JustextCrawler -good https://loremipsum.io/
==== https://loremipsum.io/
Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual m[...]
```

### Use just one tool

Each tool is more or less independent. The only thing that may cause problem is that I defined *interfaces* to ease the development. So to "export" one tool, just remove the `from ..interface` import and the interface name in the class definition and you should be good to go. 