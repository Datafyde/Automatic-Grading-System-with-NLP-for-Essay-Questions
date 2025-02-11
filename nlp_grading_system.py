# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@author: ADURA
"""

# Import necessary libraries
import streamlit as st  # Streamlit is used to create the web app
import pandas as pd  # Pandas is used to handle CSV file operations

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

# Create a sidebar header
st.sidebar.header("Others")  # This section is for additional features, like refreshing the page, etc.

# Button to refresh the page and wipe uploaded files
if st.sidebar.button("Refresh Page & Wipe Files"):
    st.rerun()  # When clicked, it should restart the app and clear the uploaded files.

# Title of the web app
st.title("Automatic Grading System")  # This is the main title of the app

# Section to upload the answer key file
st.subheader("Upload the Assessment Key (CSV)")  # Subtitle for the answer key upload section
key_file = st.file_uploader("*correct answers.csv*", type=["csv"], key="key_file")  # File uploader for the answer key

# Section to upload the student responses file
st.subheader("Upload the Student's Submission (CSV)")  # Subtitle for the student response upload section
response_file = st.file_uploader("*student submission.csv*", type=["csv"], key="response_file")  # File uploader for student responses

# Define the expected column names for both uploaded files
expected_key_columns = ["QuestionID", "Correct_Answer"]  # The correct answer file should have these columns
expected_response_columns = ["StudentID", "QuestionID", "Student_Answer"]  # The student response file should have these columns

# Process the uploaded answer key file
if key_file:  # If a file has been uploaded
    key_df, key_error = validate_csv(key_file, expected_key_columns)  # Validate the file structure
    if key_error:  # If there's an error in the file
        st.error(key_error)  # Display the error message in red
    else:
        st.success("Correct answers uploaded and validated successfully.")  # Show a success message in green
        st.dataframe(key_df.head())  # Display the first few rows of the validated file

# Process the uploaded student responses file
if response_file:  # If a file has been uploaded
    response_df, response_error = validate_csv(response_file, expected_response_columns)  # Validate the file structure
    if response_error:  # If there's an error in the file
        st.error(response_error)  # Display the error message in red
    else:
        st.success("Student's answers uploaded and validated successfully.")  # Show a success message in green
        st.dataframe(response_df.head())  # Display the first few rows of the validated file
