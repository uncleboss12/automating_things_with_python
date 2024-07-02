

import pandas as pd
import json

# Load the Excel data
df = pd.read_excel('stream-data.xlsx')  # replace with your file name

# Load the JSON data
with open('stream-for-all-pages.json', 'r') as f:
    data = json.load(f)

# Create a dictionary from the Excel data for easy lookup
excel_data = df.set_index('Year').T.to_dict('list')

# Update the JSON data
for item in data['analysis']['data']['4']:  # Accessing '1'
    if item['label'] in excel_data:
        item['F2'] = excel_data[item['label']][0:3]  # Only the first three values for 'F2'

# Write the data back to the file
with open('stream-for-all-pages.json', 'w') as f:
    json.dump(data, f, indent=4)