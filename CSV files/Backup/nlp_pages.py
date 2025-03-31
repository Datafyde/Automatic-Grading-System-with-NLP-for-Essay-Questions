# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA
"""

# Import necessary libraries
import streamlit as st  # Streamlit for UI
import pandas as pd  # Pandas for data manipulation
import numpy as np  # Numpy for numerical operations
import time  # Time module for delays
from sentence_transformers import SentenceTransformer, util  # Transformer model for grading essays

# Load the sentence transformer model for text similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to validate the uploaded CSV file
def validate_csv(file, expected_columns):
    try:
        df = pd.read_csv(file)  # Read CSV file into a DataFrame
        
        # Check for missing columns in the uploaded file
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"
        
        # Check for missing values in the dataset
        elif df.isnull().values.any():
            return None, "The file contains missing values. Please check and re-upload."
        
        # Check for duplicate rows in the dataset
        elif df.duplicated().any():
            return None, "The file contains duplicate rows. Please check and re-upload."
        
        else:
            return df, None  # Return validated DataFrame
    except Exception as e:
        return None, f"Error reading the file: {str(e)}"  # Return error message

# Function to grade objective (MCQ) questions
def grade_mcq_questions(key_df, response_df):
    try:
        # Filter only MCQ type questions from the dataset
        key_df = key_df[key_df['Type'] == 'MCQ']
        response_df = response_df[response_df['Type'] == 'MCQ']
        
        # Remove duplicate questions in the answer key
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        
        # Remove duplicate responses for a student-question pair
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        # Merge student responses with correct answers based on QuestionID and Type
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        
        # Compare student answers with correct answers and assign score (1 for correct, 0 for incorrect)
        merged_df['Score'] = (merged_df['Student_Answer'] == merged_df['Correct_Answer']).astype(float)
        
        # Return total scores for each student
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")  # Print error message if grading fails
        return None

# Function to grade essay questions
def grade_essay_questions(key_df, response_df):
    try:
        # Filter only essay-type questions from the dataset
        key_df = key_df[key_df['Type'] == 'ESSAY']
        response_df = response_df[response_df['Type'] == 'ESSAY']
        
        # Remove duplicate questions in the answer key
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        
        # Remove duplicate responses for a student-question pair
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        # Merge student responses with correct answers based on QuestionID and Type
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        
        # Function to compute similarity between correct and student answer
        def compute_similarity(row):
            correct_embedding = model.encode(row['Correct_Answer'], convert_to_tensor=True)  # Encode correct answer
            student_embedding = model.encode(row['Student_Answer'], convert_to_tensor=True)  # Encode student answer
            similarity = util.pytorch_cos_sim(correct_embedding, student_embedding).item()  # Compute cosine similarity
            return 10 if similarity >= 0.75 else round(similarity*10)  # Convert similarity score to a scale of 10
        
        # Apply similarity function to each row
        merged_df['Score'] = merged_df.apply(compute_similarity, axis=1)
        
        # Return total scores for each student
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")  # Print error message if grading fails
        return None

# Streamlit navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Grading System", "User Guide"])

if page == "Home":
    st.title("Welcome to the Automatic Grading System")
    st.write("""
    This project provides an automated system for grading both multiple-choice and essay-type questions.
    The system uses predefined correct answers for MCQs and a deep learning model for evaluating the similarity of essay answers.
    Upload your files and let the system do the grading for you!
    """)
    
elif page == "Grading System":
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
            
            with st.spinner("In progress"):
                time.sleep(5)
                
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
                st.dataframe(final_scores)
                #st.subheader("Final Scores")
                file = final_scores.set_index('StudentID')
                file = file.to_csv().encode("utf-8")
            else:
                st.error("Grading failed. Please check the input files and try again.")
                
                
            st.header("Grade Visualization")
            st.bar_chart(data=final_scores, x='StudentID', y='Score', horizontal=True, 
                         height=300)
            

            st.download_button("Download final result", file_name="final.csv", data = file, 
                               mime="text/csv", type='primary')
else:
    st.subheader("User Guide")