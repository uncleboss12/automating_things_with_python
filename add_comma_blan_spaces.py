# Open the input file in read mode
with open('pcp_fork.txt', 'r') as infile:
    # Read the file
    lines = infile.readlines()

# Replace blank spaces with commas
lines = [line.replace('\t', ',') for line in lines]

# Open the output file in write mode
with open('pcp_fork.txt', 'w') as outfile:
    # Write the modified content to the file
    outfile.writelines(lines)
