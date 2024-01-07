import os

# Define the path to the directory containing the text files
directory = r'C:\Users\interactwel\Desktop\PRISM datasets\excel_to_text_script_folder'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        
        # Read the contents of the file
        with open(filepath, 'r') as file:
            content = file.read()
        
        # Add commas between two integers
        content = content.replace(' ', ',')
        
        # Write the modified content back to the file
        with open(filepath, 'w') as file:
            file.write(content)
