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
        # Ensure required columns exist
        if not {'QuestionID', 'Correct_Answer', 'Type'}.issubset(key_df.columns):
            raise ValueError("Assessment key must contain 'QuestionID', 'Correct_Answer' and 'Type' columns.")
        if not {'StudentID', 'QuestionID', 'Student_Answer'}.issubset(response_df.columns):
            raise ValueError("Student responses must contain 'StudentID', 'QuestionID' and 'Student_Answer' columns.")

        # Remove Duplicates before merging to prevent incorrect mapping
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])

        # Merge student responses with the assessment key
        merged_df = response_df.merge(key_df, on="QuestionID", how="left")

        # Assign scores (1.0 for correct, 0 for incorrect)
        merged_df['Score'] = (merged_df['Student_Answer'] == merged_df['Correct_Answer']).astype(float)

        # Summarize scores per student
        student_scores = merged_df.groupby('StudentID', as_index=False)['Score'].sum()

        return student_scores


    except Exception as e:
        print(f"Error: {e}")
        return None

        # Perform grading and display results.
        # NOTE: Input this batch of code immediately after Adura's code ends or it will not run.
        st.subheader("Grading Results")
        scores_df = grade_objective_questions(key_df, response_df)

        if scores_df is not None:
            st.dataframe(scores_df)  # Display results in Streamlit
        else:
            st.error("Grading failed. Please check the input files and try again.")


st.info("Please upload both CSV files for validation.")