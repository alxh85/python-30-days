import pandas as pd

def clean_data():
    # 1. LOAD: Read the csv file into a DataFrame
    # Hint: Use pd.read_csv()

    df = pd.read_csv('raw_inventory.csv') # TODO: Load 'raw_inventory.csv' here
    
    print("--- Initial Inspection ---")
    print(df.info()) # This helps you see data types and missing values
    
    # 2. CLEANING: Handle Missing Values
    # The 'stock_qty' column has NaNs. Fill them with 0.
    # Hint: Look up .fillna() or directly assign df['col'] = ...
    # TODO: Write logic to fill NaNs in 'stock_qty'
    df['stock_qty'] = df['stock_qty'].fillna(0)
    
    # 3. CLEANING: Fix Data Types
    # 'unit_price' is currently an 'object' (string) because of '$' and ','.
    # We need to remove '$' and ',' and then convert to numeric.
    # Hint: .str.replace('$', '')... and pd.to_numeric() or .astype(float)
    # TODO: Clean the 'unit_price' column
    
    # Remove $ AND ,
    df['unit_price'] = df['unit_price'].str.replace('$', '').str.replace(',', '')
    # Now convert
    df['unit_price'] = pd.to_numeric(df['unit_price'])
    

    
    # 4. CALCULATION: Create a new column 'total_value'
    # Logic: stock_qty * unit_price
    # TODO: Create the new column
    df['total_value'] = df["stock_qty"] * df['unit_price']
    

    return df

def analyze_data(df):
    print("\n--- Final Analysis ---")
    
    # 5. AGGREGATION: Group by 'category' and sum the 'total_value'
    # Hint: df.groupby('...')['...'].sum()
    summary = df.groupby('category')['total_value'].sum() # TODO: Write the groupby logic
    
    print(summary)

# --- Execution ---
if __name__ == "__main__":
    cleaned_df = clean_data()
    
    # Check if cleaning worked (print first few rows)
    print("\n--- Cleaned Data Head ---")
    print(cleaned_df.head())
    
    analyze_data(cleaned_df)