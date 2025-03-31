import streamlit as st
import pandas as pd
import numpy as np
import math as m
import spacy

nlp = spacy.load('en_core_web_lg')

st.title('Using Streamlit with Spacy')
#score = st.slider('Select Mark', 2, 5, 3)
ans = st.text_input('Type Answer key:')
sub = st.text_input('Type Submission:')
btn = st.button('Analyze')
if btn == True:
    res1 = nlp(ans)
    res2 = nlp(sub)
    sim = res1.similarity(res2)
    st.write("Similarity Score: ", sim)
    #scale the similarity score to 10
    sim = m.ceil(sim*1)
    st.write("Scaled Score: ", sim)