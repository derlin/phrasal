import os

import streamlit as st
from pages import showcase, customizer

st.markdown('<a href="https://github.com/derlin/phrasal" target="_blank">View on GitHub</a>', unsafe_allow_html=True)

# == page selector

CUSTOMIZER_PAGE = 'Live Customizer'
SHOWCASE_PAGE = 'Showcase'
ABOUT_PAGE = 'About'

page = st.sidebar.selectbox("Pages", [SHOWCASE_PAGE, CUSTOMIZER_PAGE, ABOUT_PAGE])
if page == ABOUT_PAGE:
    with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'README.md')) as f:
        st.markdown(f.read())

elif page == SHOWCASE_PAGE:
    showcase.render()

elif page == CUSTOMIZER_PAGE:
    customizer.render()

# == general "footer"
st.markdown("""
<style type="text/css">
    tbody tr:hover { background: #f8f8f9; }
    /* footer:after { content: ' by Derlin'; } */
    .me { color: #bfc5d3; font-size: .9em; margin-top: 20px; text-align: right; margin-right: 20px; }
    .me a { color: #808495 !important; }
    .me a:hover { text-decoration: underline; }

    section.main .element-container:first-of-type {
        text-align: right;
        position: absolute;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="me">Made with ♡ by <a href="https://derlin.ch">Derlin</a></div>', unsafe_allow_html=True)
