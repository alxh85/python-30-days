import pandas as pd
import argparse
import json
import logging # <--- NEW: Import logging library

# 1. SETUP LOGGING
def setup_logging(log_file="cleaner.log"):
    # This configures the logging system
    # - level=logging.INFO: Record everything INFO and above (WARNING, ERROR)
    # - format: Adds timestamp, severity level, and message
    # - handlers: Writes to BOTH a file (FileHandler) and the screen (StreamHandler)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file), # Writes to cleaner.log
            logging.StreamHandler()        # Writes to terminal
        ]
    )

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Log the error before crashing
        logging.error("Config file not found! Please ensure config.json exists.")
        raise

def clean_data(input_path, config):
    logging.info(f"Loading data from: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_path}")
        raise

    # Cleaning Logic
    # check for missing values and log a warning if found
    missing_count = df['stock_qty'].isna().sum()
    if missing_count > 0:
        logging.warning(f"Found {missing_count} missing stock values. Filling with 0.")

    df['stock_qty'] = df['stock_qty'].fillna(0)
    
    # Use config for currency symbol
    currency = config.get('currency_symbol', '$') 
    df['unit_price'] = df['unit_price'].str.replace(currency, '').str.replace(',', '')
    df['unit_price'] = pd.to_numeric(df['unit_price'])
    
    df['total_value'] = df['stock_qty'] * df['unit_price']
    return df

def analyze_data(df, output_path):
    summary = df.groupby('category')['total_value'].sum()
    summary.to_csv(output_path)
    logging.info(f"Report saved successfully to {output_path}")

if __name__ == "__main__":
    # Initialize logging immediately
    setup_logging()
    
    logging.info("--- Script Started ---")
    
    # Wrap main logic in a try/except to catch unexpected crashes
    try:
        config = load_config()
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", default=config['default_input'])
        parser.add_argument("--output", default=config['default_output'])
        args = parser.parse_args()

        # Pass config into clean_data
        cleaned_df = clean_data(args.input, config)
        analyze_data(cleaned_df, args.output)
        
        logging.info("--- Script Finished Successfully ---")
        
    except Exception as e:
        # Catch-all: If anything unexpected crashes the script, log it!
        logging.error(f"Script crashed: {e}")