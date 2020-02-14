import base64
from collections import defaultdict

import streamlit as st
import pandas as pd
import os, sys, re

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from utils.customizer_constants import CustomizerConstants as cc
from utils.session_state import get as get_state

MODE_URL = 'Url'
MODE_TEXT = 'Text'
MODE_FILE = 'File'


@st.cache()
def get_text_from_url(url, crawler, kargs):
    return crawler.crawl(url, ignore_links=True, **kargs).text


def get_text_download_link(df, filename='phrasal.txt', text='Download Text file'):
    """Generates a link to download the text from the 'text' column
    """
    txt = '\n'.join(df.text.values)
    b64 = base64.b64encode(txt.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/text;base64,{b64}" download="{filename}">{text}</a>'


def get_csv_download_link(df, filename='phrasal.csv', text='Download CSV file'):
    """Generates a link allowing the data in a given panda dataframe to be downloaded"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


def get_code(mode, pipeline, pipeline_args):
    is_interface = dict()

    # generate the tool instantiations: xx = YY()
    vars = []
    for key, cls in pipeline.items():
        cls_name = cls.__class__.__name__
        is_interface[key] = cls_name.startswith('I')
        if not is_interface[key]:
            args_list = ', '.join(f"{k}={v}" for k, v in pipeline_args[key].items())
            vars.append('{} = phrasal.{}({})'.format(key[:-1], cls_name, args_list))
    vars = '\n'.join(vars)
    # generate the input code
    inpt = {
        MODE_URL: "url = '<YOUR URL>'\ntext = crawler.crawl(url).text",
        MODE_FILE: "with open('<YOUR FILE>') as f:\n    text = f.read()",
        MODE_TEXT: "text = '<YOUR TEXT>'"
    }[mode]
    # generate the pipeline use
    code = []
    if not is_interface['normalizers']:
        code.append('text = normalizer.normalize(text)')
    code.append('chunks = ' + ('splitter.split(text)' if not is_interface['splitters'] else 'text.splitlines()'))
    if not is_interface['filterers']:
        code.append('sentences = [l for l in chunks if filterer.is_valid(l)]')
    code = '\n'.join(code)

    return re.sub(' *\\|', '', f"""
    |# import the library
    |import phrasal
    |
    |# instantiate the tools
    |{vars}
    |
    |# get the input
    |{inpt}
    |
    |# use the tools
    |{code}
    """)


def render():
    st.write('''
    # Live customizer

    Play with the different tool implementation on the sidebar, live test on files/url/text and get the code snippet
    to copy-paste in your code. P.S: don't forget to scroll down for results ^^.
    ''')

    pipeline = dict()
    pipeline_args = defaultdict(lambda: dict())

    session_state = get_state(**{k: 0 for k in cc.tools.keys()})

    # main input
    st.subheader('Data picker')
    mode = st.radio('Input type:', [MODE_URL, MODE_TEXT, MODE_FILE])
    text = None

    # sidebar toolchain
    st.sidebar.markdown('# Toolchain')
    st.sidebar.markdown('Customize the toolchain by selecting the different implementations.')

    for key, current in cc.tools.items():
        # BUG it looses state ...
        if mode != MODE_URL and key == 'crawlers':
            continue

        st.sidebar.markdown(f'**{key[:-1]}**')
        implementation_options = list(current['impl'].keys())
        tool_key = st.sidebar.selectbox(
            'Implementation',
            key=key, options=implementation_options, index=getattr(session_state, key))
        pipeline[key] = current['impl'][tool_key]
        setattr(session_state, key, implementation_options.index(tool_key))

        # BUG so always show the options ... TODO
        # for target, options in current['options'].items():
        #     for (arg, label, default_value) in options:
        #         arg_value = st.sidebar.checkbox(label, value=default_value)
        #         if target == tool_key:
        #             pipeline_args[key][arg] = arg_value

        # THIS should be the implementation, but somehow the state is lost ...
        options = current['options'].get(tool_key)
        if options:
            for (arg, label, default_value) in options:
                arg_value = st.sidebar.checkbox(label, key=arg, value=default_value)
                pipeline_args[key][arg] = arg_value

    # show/get input
    if mode == MODE_URL:
        url = st.text_input('Enter a valid URL:')
        if url:
            text = get_text_from_url(url, pipeline['crawlers'], pipeline_args['crawlers'])

    elif mode == MODE_FILE:
        file = st.file_uploader('Select a file:', type="txt")
        if file:
            try:
                text = file.read()
            except Exception as e:
                st.error(e)

    elif mode == 'Text':
        text = st.text_area('Paste some text:')

    if text:
        st.markdown('↓ Results available below :blush: ↓')

    # show potential code
    st.subheader('Code snippet')
    st.code(get_code(mode, pipeline, pipeline_args), language='python')

    # process
    if text is not None:
        st.subheader('Code output')
        text = pipeline['normalizers'].normalize(text, **pipeline_args['normalizers'])
        splits = pipeline['splitters'].split(text, **pipeline_args['splitters'])
        df = pd.DataFrame(
            [[pipeline['filterers'].is_valid(s, **pipeline_args['filterers']), s] for s in splits],
            columns=['valid', 'text'])

        st.markdown(f"""
        `{len(text)}` characters split into `{len(df)}` "chunks" (`{len(df[df.valid])}` "sentences").""")

        valid_only = st.checkbox('Show valid only', value=False)
        if valid_only:
            df = df[df.valid]

        st.markdown(f"""<p style="text-align: right">
            Download {get_text_download_link(df, text='TXT')} or {get_csv_download_link(df, text='CSV')} file
        </p>""", unsafe_allow_html=True)
        st.table(df)


if __name__ == '__main__':
    render()
