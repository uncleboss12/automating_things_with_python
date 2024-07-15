# import pandas as pd

# # Load the Excel file
# df = pd.read_csv('jennings_precipitation_new_PRISM.csv')

# # Loop over the columns
# for i in range(83):
#     # Get the column data, using all the rows
#     data = df.iloc[:, 3:83]
    
#     # Create a .txt file for the column
#     with open(f'{i}.txt', 'w') as f:
#         # Write the data to the .txt file
#         f.write('\n'.join(data.iloc[:, i].astype(str)))
#         # f.write('\n'.join(data.astype(str))) 
import pandas as pd

# Specify file paths
csv_file = "Precipitation_from_website.xlsx"  # Replace with your actual Excel file path

# Load Excel data
data = pd.read_excel(csv_file)

# Loop through columns (starting from the 4th column, ending at the 83rd column)
for i in range(1, 27):
    column_data = data.iloc[1:, i]  # Select the current column
    txt_file = f"column_{i+1}.txt"  # Create a filename based on column index
    column_data.to_string(txt_file, index=False, header=False)  # Write to text file

print("24 text files created successfully!")
