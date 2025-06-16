# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:33:05 2025

@author: ADURA
"""
import pandas as pd

# Function to validate the uploaded CSV file
def validate_csv(file, expected_columns):
    
    try:
        df = pd.read_csv(file)
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"
        elif df.isnull().values.any():
            return None, "The file contains missing values. Please check and re-upload."
        elif df.duplicated().any():
            return None, "The file contains duplicate rows. Please check and re-upload."
        else:
            return df, None
    except Exception as e:
        return None, f"Error reading the file: {str(e)}"