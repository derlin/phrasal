import base64

import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from corona.tools import *


class Pipeline:
    crawler = JustextCrawler()
    splitter = MocySplitter()
    filter = PatternSentenceFilter()

    def parse(self, url, normalize=True, fix_encoding=False, strip_emojis=False):
        text = self.crawler.crawl(url).text
        if normalize:
            text = normalize_text(text, fix_encoding=fix_encoding, strip_emojis=strip_emojis)
        split = self.splitter.split(text)
        return split


@st.cache
def get_pipeline():
    return Pipeline()

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="corona.csv">Download csv file</a>'

p = get_pipeline()

url = st.text_input('url')
normalize = st.checkbox('Normalize text', value=True)
fix_encoding = st.checkbox('Fix encoding')
strip_emojis = st.checkbox('Strip emojis')
valid_only = st.checkbox('Show valid only', value=True)

if url:
    if not url.startswith('http'):
        st.error(f'{url}: not a valid URL')
    else:
        try:
            res = p.parse(url, normalize, fix_encoding, strip_emojis)
            df = pd.DataFrame([[p.filter.is_valid(s), s] for s in res], columns=['valid', 'text'])
            if valid_only:
                df = df[df.valid][['text']]
            st.markdown(f'<p style="text-align: right">{get_table_download_link(df)}</p>', unsafe_allow_html=True)
            st.table(df)
        except CrawlError as e:
            st.error(f'Oops, {e.name}: {e.message}')
