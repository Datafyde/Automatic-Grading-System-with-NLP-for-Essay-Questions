# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""
import streamlit as st

# About Page content
about = """
Courtesy of [Datafied Academy (2025)](https://github.com/Datafyde), this project is a deliverable of the
Student Industrial Work Experience Scheme (SIWES) II Placement from the Data Science students ("23) at
[Miva Open University](https://miva.university/).

### Team members
- **[Aduragbemi Kinoshi](https://github.com/pkinoshi)**
- **[Yomi Aledare](https://github.com/yomi-aledare)**
- **[Solomon Ayuba](https://github.com/SolomonAyuba)**
- **[Okon Enang](https://github.com/Nanoshogun)**
- **Cornelius Alobu**
- **[Amos Adejesubisi](https://github.com/adejesubisi)**
- **[Abel Odemudia](https://github.com/Mudiable)**
- **[Christiana Richards](https://github.com/christinechatt)**
"""

def about_page():
  #Home Page
  st.title("About")
  #st.header("Documentation")
  st.markdown(about, unsafe_allow_html=True)
