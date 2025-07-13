# -*- coding: utf-8 -*-
"""
This part of the code contains all the functions for each page in the app.
It is also responsible for controlling what page is active and it displays the navigation bars.
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""

import streamlit as st
from home import home_page
from grading_system import grading_system_page
from user_guide import user_guide_page
from about import about_page

# Ensure home page is the default landing page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar navigation with buttons
if st.sidebar.button("Home", type="primary"):
    st.session_state.page = "Home"
if st.sidebar.button("Grading System", type="primary"):
    st.session_state.page = "Grading System"
if st.sidebar.button("User Guide", type="primary"):
    st.session_state.page = "User Guide"
if st.sidebar.button("About", type="primary"):
      st.session_state.page = "About"

# Display home page content if selected
if st.session_state.page == "Home":
    home_page()

# Display grading system content if selected
elif st.session_state.page == "Grading System":
    grading_system_page()

# Display user guide content if selected
elif st.session_state.page == "User Guide":
  user_guide_page()

else:
    about_page()
