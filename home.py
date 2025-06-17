# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""

import streamlit as st
documentation = """


## Overview
The **Automatic Grading System** is a tool designed to evaluate student answers for both **multiple-choice questions
(MCQs)** and **essay-type questions**. It compares MCQ answers directly and uses a deep learning model to assess the
similarity between student and correct essay answers. This system automates the grading process, ensuring accuracy
and efficiency.

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
- Uses a **sentence transformer model** to compute the **cosine similarity** between student answers and the correct
answers.
- Assigns a score between **0 to 10**, where higher similarity results in a higher score.

### 3. Displaying and Downloading Results
- The system **compiles scores** for both MCQs and essays.
- Final scores are displayed along with a **bar chart** visualization.
- Users can **download** the final results as a CSV file.

## Navigation
The grading system includes a **user-friendly interface** with four main sections:
1. **Home Page**: Introduction to the grading system.
2. **Grading System Page**: File uploads, grading, and results.
3. **User Guide Page**: Instructions on how to use the system.
4. **About Page**: Credits and acknowledgements.

## Conclusion
The **Automatic Grading System** simplifies the evaluation process, providing fast and accurate grading for MCQs
and essays.
By leveraging AI and automation, it ensures efficiency and fairness in assessments.
"""

def home_page():
    #Home Page
    st.title("Welcome to the Automatic Grading System")
    #st.header("Documentation")
    st.markdown(documentation, unsafe_allow_html=True)
