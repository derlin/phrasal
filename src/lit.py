import base64

import streamlit as st
import pandas as pd

pd.set_option('display.max_colwidth', None)
from corona.tools import *


class Pipeline:
    crawler = JustextCrawler()
    splitter = MocySplitter()
    filter = PatternSentenceFilter()
    normalizer = Normalizer()


@st.cache()
def get_pipeline():
    return Pipeline()


@st.cache()
def fetch_url(p, url):
    return p.crawler.crawl(url).text


@st.cache()
def parse_text(p, text, normalize, fix_encoding, strip_emojis):
    if normalize:
        text = p.normalizer.normalize(text, fix_encoding=fix_encoding, strip_emojis=strip_emojis)
    return p.splitter.split(text)


@st.cache()
def get_df(p, sentences):
    return pd.DataFrame([[p.filter.is_valid(s), s] for s in sentences], columns=['valid', 'text'])


def get_table_download_link(df, filename='corona.csv', text='Download CSV file'):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# == general style

st.markdown("""
<style type="text/css">
    tbody tr:hover { background: #f8f8f9; }
</style>
""", unsafe_allow_html=True)

# == sidebar

st.sidebar.markdown('**Options**')
st.sidebar.markdown('*Parsing*')
normalize = st.sidebar.checkbox('Normalize text', value=True)
if normalize:
    fix_encoding = st.sidebar.checkbox('Fix encoding')
    strip_emojis = st.sidebar.checkbox('Strip emojis')
else:
    fix_encoding, strip_emojis = False, False

st.sidebar.markdown('*Display*')
valid_only = st.sidebar.checkbox('Show valid only', value=True)
hide_duplicates = st.sidebar.checkbox('Hide duplicates')

# == main content
st.markdown("""
# Corona

Easily extract proper sentences from webpages. Try it out:
""")

url = st.text_input('url')
p = get_pipeline()

if url:
    if not url.startswith('http'):
        st.error(f'{url}: not a valid URL')
    else:
        try:
            text = fetch_url(p, url)
            res = parse_text(p, text, normalize, fix_encoding, strip_emojis)
            df = get_df(p, res)
            st.markdown(f"""
            The raw extracted text had `{len(text)}` characters split into `{len(res)}` "chunks"
            (`{len(df.drop_duplicates())}` unique). `{len(df[df.valid])}` are considered proper sentences.
            """)
            if valid_only:
                df = df[df.valid][['text']]
            if hide_duplicates:
                df.drop_duplicates('text', inplace=True)
            st.markdown(f'<p style="text-align: right">{get_table_download_link(df)} ({len(df)} rows)</p>',
                        unsafe_allow_html=True)
            st.table(df)
        except CrawlError as e:
            st.error(f'Oops, {e.name}: {e.message}')
