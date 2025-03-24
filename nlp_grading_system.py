# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""

# Import necessary libraries
import streamlit as st  # Streamlit for UI
import pandas as pd  # Pandas for data manipulation
import numpy as np  # Numpy for numerical operations
import time  # Time module for delays
from sentence_transformers import SentenceTransformer, util  # Transformer model for grading essays

# Load sentence transformer model for text similarity analysis
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


# Documentation content
documentation = """


## Overview
The **Automatic Grading System** is a tool designed to evaluate student answers for both **multiple-choice questions (MCQs)** and **essay-type questions**. It compares MCQ answers directly and uses a deep learning model to assess the similarity between student and correct essay answers. This system automates the grading process, ensuring accuracy and efficiency.

## Features
- Supports both **MCQs** and **Essay** questions.
- Uses **predefined answer keys** for grading MCQs.
- Employs a **sentence transformer model** for grading essays.
- **Validates** uploaded CSV files to check for missing data or errors.
- Generates **final scores** for each student.
- Provides **data visualization** through charts.
- Allows users to **download results** in CSV format.

## Workflow
### 1. Uploading the Required Files
Users need to upload two CSV files:
- **Assessment Key File**: Contains the correct answers and question types.
- **Student Submission File**: Contains student responses.

The system verifies that these files have the necessary columns and do not contain missing or duplicate data.

### 2. Grading Process
#### **MCQ Grading**
- Extracts MCQ-type questions from both uploaded files.
- Removes duplicate questions and responses.
- Compares student answers with correct answers.
- Assigns a score of **1 for correct answers** and **0 for incorrect answers**.

#### **Essay Grading**
- Extracts essay-type questions from both files.
- Uses a **sentence transformer model** to compute the **cosine similarity** between student answers and the correct answers.
- Assigns a score between **0 to 10**, where higher similarity results in a higher score.

### 3. Displaying and Downloading Results
- The system **compiles scores** for both MCQs and essays.
- Final scores are displayed along with a **bar chart** visualization.
- Users can **download** the final results as a CSV file.

## Navigation
The grading system includes a **user-friendly interface** with three main sections:
1. **Home Page**: Introduction to the grading system.
2. **Grading System Page**: File uploads, grading, and results.
3. **User Guide Page**: Instructions on how to use the system.

## Conclusion
The **Automatic Grading System** simplifies the evaluation process, providing fast and accurate grading for MCQs and essays. By leveraging AI and automation, it ensures efficiency and fairness in assessments.
"""


#PAGES
def home_page():
    #Home Page
    st.title("Welcome to the Automatic Grading System")
    #st.header("Documentation")
    st.markdown(documentation, unsafe_allow_html=True)


def grading_system_page():
    #Grading Page
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
                
            st.bar_chart(data=final_scores, x='StudentID', y='Score', horizontal=True, 
                         height=300)
            col1, col2, col3 = st.columns(3)

            col1.download_button("Download final result", file_name="final.csv", data = file, 
                                   mime="text/csv", type='primary')
            if col3.button("Refresh", type='primary'):
                grading_system_page()
            

def user_guide_page():

    # User Guide content as a Markdown string
    user_guide = """
    # User Guide - Automatic Grading System
    
    ## Introduction
    Welcome to the **Automatic Grading System**! This guide provides step-by-step instructions on how to use the system to evaluate student assessments efficiently.
    
    ## Steps to Use the System
    ### 1. Navigate to the Grading System Page
    - Click on the **Grading System** option in the sidebar to start grading.
    
    ### 2. Upload Required Files
    #### **Assessment Key File**
    - Upload a CSV file containing the correct answers.
    - Ensure the file has the following columns:
      - `QuestionID`
      - `Correct_Answer`
      - `Type` (MCQ or ESSAY)
    
    #### **Student Submission File**
    - Upload a CSV file containing student responses.
    - Ensure the file has the following columns:
      - `StudentID`
      - `QuestionID`
      - `Student_Answer`
      - `Type` (MCQ or ESSAY)
    
    ### 3. Validate Uploaded Files
    - The system will automatically check for missing or duplicate data.
    - If errors are found, you will receive a notification to correct and re-upload the files.
    
    ### 4. Start the Grading Process
    - Click the **Show Results** button to begin grading.
    - The system will process MCQs and essays separately:
      - **MCQs** are graded based on exact matching.
      - **Essays** are graded using a sentence similarity model.
    
    ### 5. View and Download Results
    - The results will be displayed in three sections:
      1. **MCQ Scores**
      2. **Essay Scores**
      3. **Final Scores** (combined MCQ and Essay scores)
    - A bar chart visualization is also provided for better insights.
    - Click the **Download Final Result** button to save the scores as a CSV file.
    
    ### 6. Refresh the Page
    - If needed, click the **Refresh** button to start a new grading session.
    
    ## Troubleshooting
    ### Common Issues & Solutions
    | Issue | Solution |
    |--------|----------|
    | Missing columns error | Ensure the uploaded file includes all required columns. |
    | Duplicate rows error | Remove duplicate rows before uploading. |
    | Grading failed | Check if the correct file format (CSV) is used. |
    
    ## Conclusion
    By following these steps, you can efficiently grade student assessments using the **Automatic Grading System**. If you encounter any issues, ensure your files are correctly formatted and try again.
    """
    
    #st.title("User Guide")  # Set the page title
    st.markdown(user_guide, unsafe_allow_html=True)  # Render the Markdown content in Streamlit with formatting



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

# Display home page content if selected
if st.session_state.page == "Home":
    home_page()

# Display grading system content if selected
elif st.session_state.page == "Grading System":
    grading_system_page()
    
        
else:
    user_guide_page()
