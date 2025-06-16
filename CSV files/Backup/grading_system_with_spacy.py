# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA
"""

# Import necessary libraries
import streamlit as st  # Streamlit is used to create the web app
import pandas as pd  # Pandas is used to handle CSV file operations
import numpy as np
import math as m
import spacy

nlp = spacy.load('en_core_web_lg')

#FUNCTIONS
# Function to validate the uploaded CSV file
def validate_csv(file, expected_columns):
    try:
        df = pd.read_csv(file)  # Read the uploaded CSV file into a Pandas DataFrame
        
        # Check for missing columns in the uploaded file
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"  # Return error if any column is missing
        
        # Check if there are any empty (NaN) values in the DataFrame
        elif df.isnull().values.any():
            return None, "The file contains missing values. Please check and re-upload."  # Return error if missing values exist
        
        # Check if there are any duplicate rows in the DataFrame
        elif df.duplicated().any():
            return None, "The file contains duplicate rows. Please check and re-upload."  # Return error if duplicates exist
        else:
            return df, None  # If all checks pass, return the DataFrame and no error message
    except Exception as e:
        return None, f"Error reading the file: {str(e)}"  # Catch errors that occur while reading the file and return an error message


#Grading marks for objective and theory
def calculate_similarity_score(key,ans):
    res1 = nlp(ans)
    res2 = nlp(key)
    sim = res1.similarity(res2)
    #scale the score to 2
    score = sim*1
    return score



# Function to Grade objective questions. By OKON
def grade_objective_questions(key_df, response_df):
    """
    Grades objective questions using assessment key and student submission DataFrames

    Parameters:
    - key_df(DataFrame): Assessment Key CSV file
    _ submission_df(DataFrame): Student Submission CSV file

    Returns:
    - DataFrame: Student Scores
    """
    try:
        
        # Merge student responses with the assessment key
        merged_df = pd.merge(response_df, key_df, on=['QuestionID','Question_Type'])

        #filter based on question type
        objective_df = merged_df[merged_df["Question_Type"] == "Objective"]
        theory_df = merged_df[merged_df["Question_Type"] == "Theory"]
        
        # Assign scores based on mark obtainable for objective
        objective_df['Score'] = (objective_df['Correct_Answer'] == objective_df['Student_Answer']).astype(float)*(objective_df['Marks_Obtainable']).astype(float)
    
        # Assign scores based on mark obtainable for theory
        theory_df["Score"] = round(theory_df.apply(lambda row: calculate_similarity_score(row["Student_Answer"],row["Correct_Answer"]) * row["Marks_Obtainable"], axis=1),2)
        
        #append the dataframes as merged_df
        frames = [objective_df,theory_df]
        merged_df = pd.concat(frames)
        #return merged_df

        # Summarize scores per student
        #student_scores = merged_df.groupby('StudentID', as_index=False)['Score'].sum()
        student_scores = merged_df.groupby("StudentID", as_index=False).agg({"Score": "sum", "Marks_Obtainable": "sum"})
        return student_scores


    except Exception as e:
        print(f"Error: {e}")
        return None

#UI implementation starts here
# Create a sidebar header
st.sidebar.header("Others")  # This section is for additional features, like refreshing the page, etc.


# Button to refresh the page and wipe uploaded files
if "refresh" not in st.session_state:
    st.session_state.refresh = False

if st.sidebar.button("Refresh Page & Wipe Files", type="primary"):
    st.session_state.clear()  # Clear all session state variables
    st.rerun()
    st.refresh()




# Title of the web app
st.title("Automatic Grading System")  # This is the main title of the app

# Section to upload the answer key file
st.subheader("Upload the Assessment Key (CSV)")  # Subtitle for the answer key upload section
key_file = st.file_uploader("*answer key.csv*", type=["csv"], key="key_file")  # File uploader for the answer key

# Section to upload the student responses file
st.subheader("Upload the Student's Submission (CSV)")  # Subtitle for the student response upload section
response_file = st.file_uploader("*student submission.csv*", type=["csv"], key="response_file")  # File uploader for student responses

# Define the expected column names for both uploaded files
expected_key_columns = ["QuestionID", "Correct_Answer","Question_Type","Marks_Obtainable"]  # The correct answer file should have these columns
expected_response_columns = ["StudentID", "QuestionID", "Student_Answer","Question_Type"]  # The student response file should have these columns

# Process the uploaded answer key file
if key_file:  # If a file has been uploaded
    key_df, key_error = validate_csv(key_file, expected_key_columns)  # Validate the file structure
    if key_error:  # If there's an error in the file
        st.error(key_error)  # Display the error message in red
    else:
        st.success("Correct answers uploaded and validated successfully.")  # Show a success message in green
        st.dataframe(key_df.head(20))  # Display the first few rows of the validated file

# Process the uploaded student responses file
if response_file:  # If a file has been uploaded
    response_df, response_error = validate_csv(response_file, expected_response_columns)  # Validate the file structure
    if response_error:  # If there's an error in the file
        st.error(response_error)  # Display the error message in red
    else:
        st.success("Student's answers uploaded and validated successfully.")  # Show a success message in green
        st.dataframe(response_df.head(20))  # Display the first few rows of the validated file


# Check if both files are validated successfully before showing the button
if key_file and response_file and key_df is not None and response_df is not None:
    # Add a button to trigger grading
    if st.button("Show Results", type="primary"):
        # Perform grading and display results
        st.subheader("Results for Objective Questions")
        scores_df = grade_objective_questions(key_df, response_df)

        if scores_df is not None:
            st.dataframe(scores_df)  # Display the grading results in a table
        else:
            st.error("Grading failed. Please check the input files and try again.")
