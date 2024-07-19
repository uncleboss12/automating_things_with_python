import pandas as pd


# Read the first Excel sheet
df1 = pd.read_csv('Max_Temperature_data_big_watershed.csv')
# Read the second Excel sheet
df2 = pd.read_csv('Min_Temperature_data_big_watershed.csv')

# Select the desired columns from both dataframes
columns1 = df1.columns[1:52]
columns2 = df2.columns[1:52]

# Iterate over the columns and create separate text files
for i, (col1, col2) in enumerate(zip(columns1, columns2)):
    # Combine the columns with commas
    combined_column = df1[col1].astype(float).astype(str) + ' ' + df2[col2].astype(float).astype(str)
   # combined_column.to_csv(f'output{i+1}.txt', index=False)
    # Write the combined column to a text file
    combined_column.to_csv(f'output{i+1}.txt', index=False)
 