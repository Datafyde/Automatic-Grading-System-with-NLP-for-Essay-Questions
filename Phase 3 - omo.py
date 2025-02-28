# Import required libraries
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load data
assessment_key = pd.read_csv("Input Files/assessment_key.csv")
student_submissions = pd.read_csv("Input Files/students_submission.csv")

# Initialize NLP models
# For Multiple Choice: Simple exact match
# For Essays: Sentence-BERT for semantic similarity
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def grade_mcq(student_answer, correct_answer):
  """Grade multiple-choice questions using exact match"""
  return 1 if student_answer.strip().lower() == correct_answer.strip().lower() else 0

def grade_essay(student_answer, reference_answer, threshold=0.6):
  """Grade essays using semantic similarity"""
  # Generate embeddings
  embeddings = model.encode([student_answer, reference_answer])
  # Calculate similarity score
  similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
  return 1 if similarity >= threshold else 0

def main():
  results = []

  for _, student_row in student_submissions.iterrows():
    student_id = student_row['StudentID']
    question_id = student_row['QuestionID']
    student_answer = student_row['Answer']
    question_type = student_row['Type']

    # Get correct answer from assessment key
    correct_answer_row = assessment_key[assessment_key['QuestionID'] == question_id].iloc[0]
    correct_answer = correct_answer_row['Answer']

    # Grade based on question type
    if question_type == 'MCQ':
      score = grade_mcq(student_answer, correct_answer)
    elif question_type == 'Essay':
      score = grade_essay(student_answer, correct_answer)

    results.append({
      'StudentID': student_id,
      'QuestionID': question_id,
      'Score': score,
      'Type': question_type
    })

  return pd.DataFrame(results)

# Run the grading system
results_df = main()
print(results_df)
