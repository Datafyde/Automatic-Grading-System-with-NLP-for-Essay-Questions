# -*- coding: utf-8 -*-
"""
This part of the code is responsible for showing you the User Guide
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""
import streamlit as st

# User Guide content as a Markdown string
user_guide = """
# User Guide - Automatic Grading System

## Introduction
Welcome to the **Automatic Grading System**! This guide provides step-by-step instructions on how to use the system to
evaluate student assessments efficiently.

## Steps to Use the System
### 1. Navigate to the Grading System Page
- Click on the **Grading System** option in the sidebar to start grading.
"""

def user_guide_page():

    # Display text content
    st.markdown(user_guide, unsafe_allow_html=True)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%201.png",
      caption="Click on Grading System",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    ### 2. Upload Required Files
    #### **Assessment Key File**
    - Upload a CSV file containing the correct answers.
    - Ensure the file has the following columns:
      - `QuestionID`
      - `Correct_Answer`
      - `Type` (MCQ or ESSAY)
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%202.png",
      caption="Upload .CSV Correct Answers file",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    #### **Student Submission File**
    - Upload a CSV file containing student responses.
    - Ensure the file has the following columns:
      - `StudentID`
      - `QuestionID`
      - `Student_Answer`
      - `Type` (MCQ or ESSAY)
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%203.png",
      caption="Upload .CSV Student Submission File",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    ### 3. Validate Uploaded Files
    - The system will automatically check for missing or duplicate data.
    - If errors are found, you will receive a notification to correct and re-upload the files.
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%203%20Error%20Message.png",
      caption="Invalid Uploaded Files",
      width=700
    )
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%203%20Fixed.png",
      caption="Uploaded Files Validated",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    ### 4. Start the Grading Process
    - Click the **Show Results** button to begin grading.
    - The system will process MCQs and essays separately:
      - **MCQs** are graded based on exact matching.
      - **Essays** are graded using a sentence similarity model.
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%204.png",
      caption="Click on Show Results",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    ### 5. View and Download Results
    - The results will be displayed in three sections:
      1. **MCQ Scores**
      2. **Essay Scores**
      3. **Final Scores** (combined MCQ and Essay scores)
    - A bar chart visualization is also provided for better insights.
    - Click the **Download Final Result** button to save the scores as a CSV file.
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%205%20Scores.png",
      caption="MCQ and Esasy Scores",
      width=700
    )

    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%205%20Chart.png",
      caption="Bar Chart Visualization & Download Results",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""
    ### 6. Refresh the Page
    - If needed, click the **Refresh** button to start a new grading session.
    """)

    # Display screenshot of step
    st.image(
      "https://raw.githubusercontent.com/Datafyde/Automatic-Grading-System-with-NLP-for-Essay-Questions/main/User%20Guide/Step%206.png",
      caption="Click on Refresh Button",
      width=700
    )

    # Continue with the rest of the guide
    st.markdown("""

    ## Troubleshooting
    ### Common Issues & Solutions
    | Issue | Solution |
    |--------|----------|
    | Missing columns error | Ensure the uploaded file includes all required columns. |
    | Duplicate rows error | Remove duplicate rows before uploading. |
    | Grading failed | Check if the correct file format (CSV) is used. |

    ## Conclusion
    By following these steps, you can efficiently grade student assessments using the **Automatic Grading System**.
    If you encounter any issues, ensure your files are correctly formatted and try again.
    """)

    #st.title("User Guide")  # Set the page title
    #st.markdown(user_guide, unsafe_allow_html=True)  # Render the Markdown content in Streamlit with formatting
