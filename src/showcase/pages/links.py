import base64

import streamlit as st
import pandas as pd
from phrasal import extract_links, link_utils

pd.set_option('display.max_colwidth', None)


@st.cache
def fetch_links(cr, url):
    return cr.crawl(url, ignore_links=False).links


def get_table_download_link(df, filename='links.csv', text='Download TXT file'):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


def render():
    # == main content
    st.markdown("""
    # Links extractor
    
    This page let's you test the links extraction tool available with phrasal.
    The link extractor will filter out non HTTP links, resolve relative URLs and remove duplicates. 
    
    *Note*: by links, we mean <u>`a[href]` attributes only</u> (so no images).
    
    Basic usage:
    ```python
    import phrasal
    
    url = "<URL>"
    
    all_links = phrasal.extract_links(url)
    non_media_links = [l for l in all_links if not phrasal.link_utils.is_media_link(l)]
    ```
    
    Give it a spin!
    """, unsafe_allow_html=True)

    url = st.text_input('url')

    if url:
        if not url.startswith('http'):
            st.error(f'{url}: not a valid URL')
        else:
            try:
                links = extract_links(url)
                df = pd.DataFrame([
                    [l, link_utils.is_media_link(l)] for l in links
                ], columns=['link', 'is_media'])

                st.markdown(f"Found `{len(df)}` links, `{df.is_media.sum()}` being [probably] links to medias. ")

                if st.checkbox('Sort ascending'):
                    df = df.sort_values('link')
                if df.is_media.sum() > 0 and st.checkbox('Hide media links'):
                    df = df[~df.is_media]

                st.markdown(f'<p style="text-align: right">{get_table_download_link(df)} ({len(df)} lines)</p>',
                            unsafe_allow_html=True)
                st.table(df)
            except Exception as e:
                st.error(f'{e.__class__.__name__}: {str(e)}')
