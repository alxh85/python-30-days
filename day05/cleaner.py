import pandas as pd
import argparse
import json # <--- NEW: Library for reading JSON files

def load_config():
    # 1. Open the JSON file and return the dictionary
    # Hint: with open('config.json', 'r') as f: ...
    #       return json.load(f)
    
    # TODO: Write the code to load 'config.json'
    with open('config.json', 'r') as f:
        return json.load(f)



def clean_data(input_path):
    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    
    # Cleaning Logic (Same as before)
    df['stock_qty'] = df['stock_qty'].fillna(0)
    
    # TODO: Optional Challenge - Can you read the currency symbol from the config 
    # instead of hardcoding '$'? (Pass config into this function if you want to try!)
    df['unit_price'] = df['unit_price'].str.replace(config['currency_symbol'], '').str.replace(',', '')
    df['unit_price'] = pd.to_numeric(df['unit_price'])
    
    df['total_value'] = df['stock_qty'] * df['unit_price']
    return df

def analyze_data(df, output_path):
    summary = df.groupby('category')['total_value'].sum()
    summary.to_csv(output_path)
    print(f"\n✅ Report saved to {output_path}")

if __name__ == "__main__":
    # 2. LOAD CONFIG FIRST
    config = load_config()
    
    parser = argparse.ArgumentParser()
    
    # 3. USE CONFIG AS DEFAULTS
    # logic: default=config['key_name']
    # required=False (because now we have a fallback!)
    
    parser.add_argument("--input", 
                        help="Path to input file", 
                        default=config['default_input']) # <--- Reads from JSON
                        
    parser.add_argument("--output", 
                        help="Path to output file", 
                        default=config['default_output']) # <--- Reads from JSON

    args = parser.parse_args()

    cleaned_df = clean_data(args.input)
    analyze_data(cleaned_df, args.output)