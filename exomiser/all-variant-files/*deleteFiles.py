import os

# Get the current directory
current_directory = os.getcwd()

# Get a list of all files in the current directory
files = os.listdir(current_directory)

# Iterate over each file
for file in files:
    # Check if the file ends with "genes.tsv"
    if 'ONLY-trio.variants' in file:
        # Construct the file path
        file_path = os.path.join(current_directory, file)
        
        # Delete the file
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
