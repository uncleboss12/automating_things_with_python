import os

# Specify the directory you want to use
directory = r'C:\Users\interactwel\Desktop\PRISM datasets\excel_to_text_script_folder'

# Initialize a counter for the new filenames
counter = 1

# Loop over all files in the directory
for filename in sorted(os.listdir(directory)):
    # Check if the file is one of the files you want to rename
    if filename.startswith('column') and filename.endswith('.txt'):
        # Create the new filename
        new_filename = f'{counter}.txt'
        
        # Get the full paths of the old and new files
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)

        # Increment the counter
        counter += 1
