import pandas as pd
import argparse  # <--- NEW LIBRARY

def clean_data(input_path): # <--- NOW ACCEPTS A PATH ARGUMENT
    print(f"Loading data from: {input_path}")
    
    # 1. LOAD: Use the variable 'input_path' instead of the hardcoded string
    df = pd.read_csv(input_path) 
    
    # ... (Your existing cleaning logic for NaNs and Prices goes here) ...
    # ... Copy/Paste your cleaning logic from Day 03 ...
    
    # RE-ADD YOUR CLEANING LOGIC HERE
    df['stock_qty'] = df['stock_qty'].fillna(0)
    df['unit_price'] = df['unit_price'].str.replace('$', '').str.replace(',', '')
    df['unit_price'] = pd.to_numeric(df['unit_price'])
    df['total_value'] = df['stock_qty'] * df['unit_price']

    return df

def analyze_data(df, output_path): # <--- NOW ACCEPTS AN OUTPUT PATH
    print("\n--- Final Analysis ---")
    summary = df.groupby('category')['total_value'].sum()
    print(summary)
    
    # Save to the specific output path provided by the user
    summary.to_csv(output_path)
    print(f"\n✅ Report saved to {output_path}")

if __name__ == "__main__":
    # --- CLI SETUP START ---
    parser = argparse.ArgumentParser(description="Clean inventory files.")
    
    # Define the arguments we expect from the user
    parser.add_argument("--input", help="Path to the raw CSV file", required=True)
    parser.add_argument("--output", help="Path to save the report", required=True)
    
    # Parse the arguments (Python splits the command line string for you)
    args = parser.parse_args()
    # --- CLI SETUP END ---

    # Now we pass the CLI arguments into our functions
    cleaned_df = clean_data(args.input)
    analyze_data(cleaned_df, args.output)