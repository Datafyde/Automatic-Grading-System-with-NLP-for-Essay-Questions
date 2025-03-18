# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA
"""

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to validate the uploaded CSV file
def validate_csv(file, expected_columns):
    try:
        df = pd.read_csv(file)
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"
        elif df.isnull().values.any():
            return None, "The file contains missing values. Please check and re-upload."
        elif df.duplicated().any():
            return None, "The file contains duplicate rows. Please check and re-upload."
        else:
            return df, None
    except Exception as e:
        return None, f"Error reading the file: {str(e)}"

# Function to grade objective (MCQ) questions
def grade_mcq_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'MCQ']
        response_df = response_df[response_df['Type'] == 'MCQ']
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        merged_df['Score'] = (merged_df['Student_Answer'] == merged_df['Correct_Answer']).astype(float)
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to grade essay questions
def grade_essay_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'ESSAY']
        response_df = response_df[response_df['Type'] == 'ESSAY']
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        
        def compute_similarity(row):
            correct_embedding = model.encode(row['Correct_Answer'], convert_to_tensor=True)
            student_embedding = model.encode(row['Student_Answer'], convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(correct_embedding, student_embedding).item()
            return 10 if similarity >= 0.75 else round(similarity*10)
        
        merged_df['Score'] = merged_df.apply(compute_similarity, axis=1)
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Create a sidebar header
st.sidebar.header("Others")  # This section is for additional features, like refreshing the page, etc.

# Button to refresh the page and wipe uploaded files
if "refresh" not in st.session_state:
    st.session_state.refresh = False

if st.sidebar.button("Refresh Page & Wipe Files", type="primary"):
    st.session_state.clear()  # Clear all session state variables
    st.rerun()
    st.refresh()
    

# Streamlit UI
st.title("Automatic Grading System")
st.subheader("Upload the Assessment Key (CSV)")
key_file = st.file_uploader("*correct answers.csv*", type=["csv"], key="key_file")
st.subheader("Upload the Student's Submission (CSV)")
response_file = st.file_uploader("*student submission.csv*", type=["csv"], key="response_file")

expected_columns = ["QuestionID", "Correct_Answer", "Type"]
expected_response_columns = ["StudentID", "QuestionID", "Student_Answer", "Type"]

if key_file:
    key_df, key_error = validate_csv(key_file, expected_columns)
    if key_error:
        st.error(key_error)
    else:
        st.success("Correct answers uploaded successfully.")
        st.dataframe(key_df)

if response_file:
    response_df, response_error = validate_csv(response_file, expected_response_columns)
    if response_error:
        st.error(response_error)
    else:
        st.success("Student's answers uploaded successfully.")
        st.dataframe(response_df)

if key_file and response_file and key_df is not None and response_df is not None:
    if st.button("Show Results", type="primary"):
        mcq_scores = grade_mcq_questions(key_df, response_df)
        essay_scores = grade_essay_questions(key_df, response_df)
        
        if mcq_scores is not None:
            st.success("MCQ Result.")
            #st.subheader("MCQ Scores")
            st.dataframe(mcq_scores)
            
        
        if essay_scores is not None:
            st.success("Essay Result.")
            #st.subheader("Essay Scores")
            st.dataframe(essay_scores)
            
            
        if mcq_scores is not None and essay_scores is not None:
            final_scores = pd.concat([mcq_scores, essay_scores]).groupby('StudentID', as_index=False)['Score'].sum()
            st.success("Final Result.")
            #st.subheader("Final Scores")
            st.dataframe(final_scores)
        else:
            st.error("Grading failed. Please check the input files and try again.")
