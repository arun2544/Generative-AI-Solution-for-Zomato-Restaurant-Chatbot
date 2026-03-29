# File: src/data_loader.py
import pandas as pd
import re
from pathlib import Path

def load_and_preprocess_data(csv_path):
    """Load and preprocess restaurant data"""
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Extract location from URL
    df['location'] = df['links'].apply(
        lambda x: x.split('/')[4].replace('-', ' ').title() 
        if len(x.split('/')) >= 5 else 'Unknown'
    )
    
    # Create searchable text
    df['search_text'] = df.apply(
        lambda row: f"{row['names']} {row['cuisine']} {row['location']} "
                    f"Rating: {row['ratings']} Price: {row['price for one']}", 
        axis=1
    )
    
    return df
