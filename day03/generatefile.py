import pandas as pd
import numpy as np

# RUN THIS ONCE TO CREATE THE FILE
data = {
    'part_id': ['101-A', '102-B', '103-A', '104-C', '105-B', '106-A', '107-C'],
    'category': ['Server', 'Rack', 'Server', 'Cable', 'Rack', 'Server', 'Cable'],
    'stock_qty': [50, 20, np.nan, 100, 15, 60, np.nan],  # NaN means missing data
    'unit_price': ['$1,200', '$800', '$1,250', '$15', '$850', '1200', '$15'], # Mixed strings/numbers
    'last_audit': ['2023-01-01', '2023-01-05', 'N/A', '2023-01-02', '2023-01-05', '2023-01-01', '2023-01-02']
}

df = pd.DataFrame(data)
df.to_csv('raw_inventory.csv', index=False)
print("✅ raw_inventory.csv created successfully.")