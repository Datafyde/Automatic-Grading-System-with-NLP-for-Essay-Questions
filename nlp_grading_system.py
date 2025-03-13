# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA
"""

import streamlit as st  # Streamlit for web app UI
import pandas as pd  # Pandas for handling CSV files
import numpy as np  # NumPy for numerical operations
from sentence_transformers import SentenceTransformer, util  # NLP model for essay grading

# Load sentence transformer model for grading essay questions
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to validate the uploaded CSV file
def validate_csv(file, expected_columns):
    try:
        df = pd.read_csv(file)  # Read CSV file into a Pandas DataFrame
        missing_columns = [col for col in expected_columns if col not in df.columns]  # Check for missing columns
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"  # Return error if columns are missing
        elif df.isnull().values.any():
            return None, "The file contains missing values. Please check and re-upload."  # Check for missing values
        elif df.duplicated().any():
            return None, "The file contains duplicate rows. Please check and re-upload."  # Check for duplicate rows
        else:
            return df, None  # Return validated DataFrame
    except Exception as e:
        return None, f"Error reading the file: {str(e)}"  # Handle file reading errors

# Function to grade MCQ questions
def grade_mcq_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'MCQ']  # Filter only MCQ questions from the answer key
        response_df = response_df[response_df['Type'] == 'MCQ']  # Filter only MCQ questions from student responses
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])  # Remove duplicate questions from key
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])  # Remove duplicate responses
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")  # Merge student responses with answer key
        merged_df['Score'] = (merged_df['Student_Answer'] == merged_df['Correct_Answer']).astype(float)  # Assign 1.0 for correct answers, 0 otherwise
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()  # Summarize scores per student
    except Exception as e:
        print(f"Error: {e}")  # Print error message if any
        return None

# Function to grade essay questions
def grade_essay_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'ESSAY']  # Filter only essay questions from the answer key
        response_df = response_df[response_df['Type'] == 'ESSAY']  # Filter only essay questions from student responses
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])  # Remove duplicate questions from key
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])  # Remove duplicate responses
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")  # Merge student responses with answer key
        
        # Function to compute similarity between correct answer and student answer
        def compute_similarity(row):
            correct_embedding = model.encode(row['Correct_Answer'], convert_to_tensor=True)  # Encode correct answer
            student_embedding = model.encode(row['Student_Answer'], convert_to_tensor=True)  # Encode student answer
            similarity = util.pytorch_cos_sim(correct_embedding, student_embedding).item()  # Compute similarity score
            return 1.0 if similarity >= 0.75 else similarity  # Score 1.0 if similarity is 75% or more
        
        merged_df['Score'] = merged_df.apply(compute_similarity, axis=1)  # Apply similarity function to each row
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()  # Summarize scores per student
    except Exception as e:
        print(f"Error: {e}")  # Print error message if any
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
    
    

# Streamlit UI for user interaction
st.title("Automatic Grading System")  # App title
st.subheader("Upload the Assessment Key (CSV)")  # Section for uploading answer key
key_file = st.file_uploader("*correct answers.csv*", type=["csv"], key="key_file")  # File uploader for answer key
st.subheader("Upload the Student's Submission (CSV)")  # Section for uploading student answers
response_file = st.file_uploader("*student submission.csv*", type=["csv"], key="response_file")  # File uploader for student responses

# Define expected column names for validation
expected_columns = ["QuestionID", "Correct_Answer", "Type"]  # Expected columns in the answer key
expected_response_columns = ["StudentID", "QuestionID", "Student_Answer", "Type"]  # Expected columns in student responses

# Process uploaded answer key file
if key_file:
    key_df, key_error = validate_csv(key_file, expected_columns)  # Validate answer key
    if key_error:
        st.error(key_error)  # Show error message if validation fails
    else:
        st.success("Correct answers uploaded successfully.")  # Success message if validation passes
        st.dataframe(key_df.head())  # Display first few rows of answer key

# Process uploaded student responses file
if response_file:
    response_df, response_error = validate_csv(response_file, expected_response_columns)  # Validate student responses
    if response_error:
        st.error(response_error)  # Show error message if validation fails
    else:
        st.success("Student's answers uploaded successfully.")  # Success message if validation passes
        st.dataframe(response_df.head())  # Display first few rows of student responses

# Perform grading if both files are uploaded and valid
if key_file and response_file and key_df is not None and response_df is not None:
    if st.button("Show Results", type="primary"):  # Button to trigger grading
        mcq_scores = grade_mcq_questions(key_df, response_df)  # Grade MCQs
        essay_scores = grade_essay_questions(key_df, response_df)  # Grade essays
        
        if mcq_scores is not None and essay_scores is not None:
            final_scores = pd.concat([mcq_scores, essay_scores]).groupby('StudentID', as_index=False)['Score'].sum()  # Combine scores
            st.subheader("Final Scores")  # Display final scores
            st.dataframe(final_scores)  # Show results in table
        else:
            st.error("Grading failed. Please check the input files and try again.")  # Error message if grading fails
