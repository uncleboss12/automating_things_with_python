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

        # Add '0.000000' to the last line
        lines[-1] = lines[-1].strip() + '\n'  + '0.000000, 0.000000\n' # [linee[-1]] is the last line of the file

        # Write the new lines back to the file
        with open(filepath, 'w') as file:
            file.writelines(lines)