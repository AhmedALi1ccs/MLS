import streamlit as st
import pandas as pd
import os

def process_csv(file):
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Define the columns to combine
    columns_to_combine = ['Street #', 'Street PreDirection', 'Street Name', 
                          'Unit/Suite #', 'Street PostDirection', 'Street Suffix']
    
    # Combine columns into 'Mailing Address'
    def combine_columns(row):
        parts = [str(row[col]).strip() for col in columns_to_combine if pd.notna(row[col]) and str(row[col]).strip()]
        return ' '.join(parts)
    
    # Apply the function and create a new column
    df['Address'] = df.apply(combine_columns, axis=1)
    
    # Drop the original columns
    df = df.drop(columns=columns_to_combine)
    return df

# Streamlit App
st.title("CSV Mailing Address Combiner")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Get the file name without extension
    original_filename = os.path.splitext(uploaded_file.name)[0]
    
    st.write("Processing file...")
    # Process the file
    processed_df = process_csv(uploaded_file)
    
    # Show preview of the processed DataFrame
    st.write("Preview of Processed Data:")
    st.dataframe(processed_df.head())
    
    # Prepare the processed file name
    processed_filename = f"{original_filename}_processed.csv"
    
    # Allow downloading the processed file
    st.download_button(
        label=f"Download Processed CSV ({processed_filename})",
        data=processed_df.to_csv(index=False),
        file_name=processed_filename,
        mime="text/csv"
    )
