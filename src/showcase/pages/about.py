import streamlit as st
import os, re


def render():
    with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', '..', '..', 'README.md')) as f:
        github_markdown = f.read()
        markdown = re.sub(r'\\\n', '<br>', github_markdown)  # streamlit doesn't handle \ for newlines...
        st.markdown(markdown, unsafe_allow_html=True)
