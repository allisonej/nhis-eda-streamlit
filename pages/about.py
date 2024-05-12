# -*- coding:utf-8 -*-

import streamlit as st

st.set_page_config(
    page_title="About Page",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.naver.com',
        'Report a bug': "https://www.google.com",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def main():
    st.write("# About Page 👋")