#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Homepage and App Module

"""
import datetime

import streamlit as st

from applications.streamlit.style import divider_style
from applications.streamlit.subpages.page_1 \
    import page_1
from applications.streamlit.subpages.page_2 \
    import page_2

YEAR = datetime.datetime.now().year


def home_page():
    st.subheader("Welcome to the Home Page")
    st.write("This is the home page of the applications.")


def main():
    st.title("My Streamlit App")
    st.markdown(divider_style, unsafe_allow_html=True)
    
    # Navigation
    page = st.sidebar.selectbox("Menu", ["Home", "Page 1", "Page 2"])

    if page == "Home":
        home_page()
    elif page == "Page 1":
        page_1()
    elif page == "Page 2":
        page_2()

    st.sidebar.write(f"**© {YEAR} [Be Happy]"
                     f"(https://github.com/mthnguyener/pyproject_starter)**")


if __name__ == "__main__":
    main()
