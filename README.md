# Automatic-Grading-System-with-NLP-for-Essay-Questions

## 1. Problem Statement
In educational settings, grading student submissions is often time-consuming and prone to subjective biases, especially for essay-type questions. Manually evaluating hundreds of answers consumes valuable resources and limits the ability to provide immediate feedback to students. A system that automates this process will streamline grading and ensure consistency.

## 2. Project Objective
The goal of this project is to develop a [Streamlit-based](https://youtu.be/2siBrMsqF44) application that can:
1. Automatically grade objective questions by comparing students' answers to the correct answers.
2. Use Natural Language Processing (NLP) to evaluate and grade essay-type questions by assessing the semantic similarity between student submissions and correct answers.
3. Provide functionality for uploading multiple files for grading and exporting the grading results.

## 3. Features of the System
### 1. File Upload Support
  - Upload the assessment key (correct answers) in CSV format.
  - Upload student submissions (answers) in CSV format.
### 2. Objective Question Grading
  - Compare student answers to the key for exact matches.
### 3. Essay Question Grading with NLP
  - Use semantic similarity to assess essay-type answers.
  - Scale similarity scores to a predefined range (e.g., 0-10 points).
### 4. Grading Results
  - Generate individual scores for each student.
  - Calculate overall scores and percentages.
### 5. Downloadable Results
  - Export grading results as a CSV file.

## 4. Requirements
### 4.1. Technical Requirements
- Python 3.8 or higher
- Required Libraries:
  - `streamlit`
  - `pandas`
  - `spacy`
  
### 4.2. Software Dependencies
- Install the `spaCy` English model:
 ``` python -m spacy download en_core_web_sm```

## 5. Project Workflow
### 5.1. Input Files
1. #### Assessment Key (CSV Format)
    - Columns:
      - **Question:** Unique identifier for each question.
      - **Answer:** Correct answer for the question.
      - **Type:** Type of question (objective or essay).
        
    - Example:

      | Question | Answer | Type |
      | --- | --- | --- |
      | Q1 | A | objective |
      | Q2 | Climate change is caused by greenhouse gases. | essay |

2. #### Student Submission (CSV Format)
    - Columns:
      - **Question:** Unique identifier for each question (must match the assessment key).
      - **Answer:** Student's response to the question.
    - Example:

      | Question | Answer |
      | --- | --- |
      | Q1 | A |
      | Q2 | Climate change results from carbon emissions. |

### 5.2. Grading Logic

1. **Objective Questions**
  - Award full marks (1.0) for exact matches between the student's answer and the correct answer.
  - Award 0 marks for incorrect answers.
2. **Essay-Type Questions**
  - Use `spaCy` to calculate the semantic similarity between the correct answer and the student’s answer.
  - Scale similarity scores to a 0-10 range.
  - Missing answers score 0.

### 5.3. Output
  - Grading Results:
    - Columns:
      - **Student:** Name of the student.
      - **Score:** Total score obtained.
      - **Max Score:** Total possible score.
      - **Percentage:** Overall percentage.
    - Example:

      | Student | Score | Max Score | Percentage |
      | --- | --- | --- | ---|
      | student1.csv | 15.8 | 30 | 52.67% |

## 6. Implementation
### 6.1. Application Workflow
### 1. **Step 1: Upload Assessment Key**
  - Upload a CSV file containing correct answers and question types.
  - The application validates the file format and displays its contents.
### 2. **Step 2: Upload Student Submissions**
  - Upload one or more CSV files containing students' answers.
  - The application validates each file and processes it for grading.
### 3. **Step 3: Grading Logic**
  - Objective questions are graded for exact matches.
  - Essay questions are graded using NLP-based semantic similarity.
### 4. **Step 4: Export Grading Results**
  - Display results for each student.
  - Allow download of the results as a CSV file.

### 6.2. Python Code
The implementation is based on Streamlit. Here’s a brief summary of the code:
- Load and validate uploaded files.
- Use `pandas` to merge assessment key and student submissions.
- Implement grading logic for both question types:
  - Exact match for objective questions.
  - Similarity scoring for essay questions using `spaCy`.
- Generate and display grading results.
- Provide the option to download the results.

## 7. Running the Application
1. Save the Python code (e.g., `grading_app_nlp.py`).
  - Run the application with Streamlit:
     ```streamlit run grading_app_nlp.py```

2. Follow the steps in the application interface to upload files, grade submissions, and download results.

## 8. Suggested Improvements
### **1. Advanced NLP Models**
  - Use transformer models (e.g., BERT) for more accurate essay evaluation.
### **2. Customized Grading Criteria**
  - Allow users to set weights for essay vs objective questions.
### **3. Question-Level Reports**
  - Provide insights on which questions most students struggled with.
### **4. User Interface Enhancements**
  - Add a progress bar during grading.

## 9. Conclusion
This project demonstrates how machine learning and NLP can automate grading to save time and improve consistency. By integrating semantic analysis for essay-type questions, the system ensures fair evaluation based on meaning rather than exact wording. This framework can be further expanded for diverse educational needs and enhanced with additional functionalities.
