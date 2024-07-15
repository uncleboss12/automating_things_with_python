import csv
from collections import defaultdict

# Input CSV file path
input_csv_path = 'PRISM_ppt_stable_4km_20180101_20181231.csv'
# Output CSV file path
output_csv_path = 'web_prism_precipitation.csv'

# Initialize a dictionary to store data for each location
location_data = defaultdict(dict)

# Read data from the input CSV (skipping rows 1 to 10)
with open(input_csv_path, mode='r') as infile:
    reader = csv.DictReader(infile)
    for _ in range(9):
        next(reader)  # Skip the first 10 rows
    
    for row in reader:
        print(row)
        location  = row['PRISM Time Series Data']
        date = row['Date']
        ppt_mm = row['ppt (mm)']
        location_data[location][date] = ppt_mm

# Create a new CSV with columns for each location
with open(output_csv_path, mode='w', newline='') as outfile:
    fieldnames = ['Date', 'ppt (mm)'] + [f'Location {i}' for i in range(1, 25)]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write data for each date and location
    for date in sorted(location_data[1].keys()):  # Assuming all locations have the same dates
        row_data = {'Date': date, 'ppt (mm)': location_data[1][date]}
        for location in range(1, 25):
            row_data[f'Location {location}'] = location_data[location].get(date, '')
        writer.writerow(row_data)

print(f"New CSV file created at {output_csv_path}")

