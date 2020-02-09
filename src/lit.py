import base64

import streamlit as st
import pandas as pd
from phrasal.pipeline import Pipeline as p, CrawlError

pd.set_option('display.max_colwidth', None)


@st.cache
def fetch_url(p, url):
    return p.crawler.crawl(url).text


@st.cache
def get_df(p, text, normalize, fix_encoding, strip_emojis, more):
    if normalize:
        text = p.normalizer.normalize(text, fix_encoding=fix_encoding, strip_emojis=strip_emojis)
    sentences = p.splitter.split(text, more)
    return pd.DataFrame([[p.filter.is_valid(s), s] for s in sentences], columns=['valid', 'text'])


def get_table_download_link(df, filename='phrasal.csv', text='Download CSV file'):
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
    /* footer:after { content: ' by Derlin'; } */
    .me { color: #bfc5d3; font-size: .9em; margin-top: 20px; text-align: right; margin-right: 20px; }
    .me a { color: #808495 !important; }
    .me a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# == sidebar

st.sidebar.markdown('**Options**')
st.sidebar.markdown('*Parsing*')
normalize = st.sidebar.checkbox('Normalize text', value=True)
if normalize:
    fix_encoding = st.sidebar.checkbox('Fix encoding')
    strip_emojis = st.sidebar.checkbox('Strip emojis')
    more = st.sidebar.checkbox('Split on ;:', value=True)
else:
    fix_encoding, strip_emojis, more = False, False, True
proper_punc = st.sidebar.checkbox('Enforce proper ending (!?.:;)', value=True)

st.sidebar.markdown('*Display*')
valid_only = st.sidebar.checkbox('Show valid only', value=True)
hide_duplicates = st.sidebar.checkbox('Hide duplicates')

# == main content
st.markdown("""
# Phrasal

Easily extract proper sentences from webpages. Try it out:
""")

url = st.text_input('url')

if url:
    if not url.startswith('http'):
        st.error(f'{url}: not a valid URL')
    else:
        try:
            text = fetch_url(p, url)
            df = get_df(p, text, normalize, fix_encoding, strip_emojis, more)
            if proper_punc:
                df = df.copy()
                df.loc[df.text.apply(lambda t: t[-1] not in '!?.:;'), 'valid'] = False
            st.markdown(f"""
            The raw extracted text had `{len(text)}` characters split into `{len(df)}` "chunks"
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

st.markdown('<div class="me">Made with ♡ by <a href="https://derlin.ch">Derlin</a></div>', unsafe_allow_html=True)