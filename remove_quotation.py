import os

# Specify the directory you want to use
directory = r'C:\Users\interactwel\Desktop\PRISM datasets\excel_to_text_script_folder'


# Loop over all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a .txt file
    if filename.endswith('.txt'):
        # Get the full path of the file
        filepath = os.path.join(directory, filename)
        
        # Read the original file
        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Remove the quotation marks from each line, starting from the second line
        new_lines = lines[:1] + [line.replace("\"", "").replace(",", ",\n").strip() for line in lines[1:]]

        # Write the new lines back to the file
        with open(filepath, 'w') as file:
            file.writelines(new_lines)





