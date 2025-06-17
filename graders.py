# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:15:57 2025

@authors: YOMI, ADURA, OKON, SOLOMON, ABEL, AMOS, CHRISTIANA, CORNELIUS
"""
from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to grade objective (MCQ) questions
def grade_mcq_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'MCQ']
        response_df = response_df[response_df['Type'] == 'MCQ']
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        merged_df['Score'] = (merged_df['Student_Answer'] == merged_df['Correct_Answer']).astype(float)
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to grade essay questions
def grade_essay_questions(key_df, response_df):
    try:
        key_df = key_df[key_df['Type'] == 'ESSAY']
        response_df = response_df[response_df['Type'] == 'ESSAY']
        
        key_df = key_df.drop_duplicates(subset=['QuestionID'])
        response_df = response_df.drop_duplicates(subset=['StudentID', 'QuestionID'])
        
        merged_df = response_df.merge(key_df, on=['QuestionID', 'Type'], how="left")
        
        def compute_similarity(row):
            correct_embedding = model.encode(row['Correct_Answer'], convert_to_tensor=True)
            student_embedding = model.encode(row['Student_Answer'], convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(correct_embedding, student_embedding).item()
            return 10 if similarity >= 0.75 else round(similarity*10)
        
        merged_df['Score'] = merged_df.apply(compute_similarity, axis=1)
        
        return merged_df.groupby('StudentID', as_index=False)['Score'].sum()
    except Exception as e:
        print(f"Error: {e}")
        return None
