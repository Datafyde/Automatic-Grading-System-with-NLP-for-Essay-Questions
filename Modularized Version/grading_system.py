# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""
import streamlit as st
import pandas as pd
import time  # Time module for delays
from validators import validate_csv
from graders import grade_mcq_questions, grade_essay_questions


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
