import csv
import os
import operator
import time
import shutil

start_time = time.time()

print("Reading input...")
# Open input.csv file and read the data
with open("exomiserInput.csv", "r") as input_file:
    reader = csv.reader(input_file)
    try:
        next(reader)  # skip the header
    except StopIteration:
        print("The exomiserInput.csv file is empty or only contains the header.")
    else:
        data = [row for row in reader]

        print("Creating combined TSV files for each patient ID...")
        # Create a combined.tsv file for each patientID
        patient_ids = set([row[0] for row in data])  # Use only the patient ID
        for patient_id in patient_ids:
            print(f"Processing patient ID: {patient_id}")
            tsv_files = [
                f
                for f in os.listdir("all-variant-files")
                if f.startswith(patient_id) and f.endswith(f".variants.tsv")
            ]
            combined_rows = []
            for tsv_file in tsv_files:
                # print(f"Reading TSV file: {tsv_file}")
                with open(os.path.join("all-variant-files", tsv_file), "r") as tsv_f:
                    tsv_reader = csv.reader(tsv_f, delimiter="\t")
                    try:
                        next(tsv_reader)  # skip the header
                    except StopIteration:
                        print(f"The TSV file {tsv_file} is empty or only contains the header.")
                    else:
                        combined_rows += [row for row in tsv_reader]

            print("Sorting and writing combined rows to the TSV file...")
            # Order/rank the rows of each combined file according to the 32nd column value, highest to smallest
            combined_rows.sort(key=lambda x: float(x[31]), reverse=True)

            # Write the combined data to a combined.tsv file
            with open(f"{patient_id}_combined.tsv", "w") as combined_file:
                tsv_writer = csv.writer(combined_file, delimiter="\t")
                tsv_writer.writerows(combined_rows)

print("Creating output.csv file...")
# Create output.csv file
with open("raw_output.csv", "w") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["PatientID", "Row Number", "Row Data"])  # Remove "Type" column

    # Search each patient combined file according to the data provided in input.csv
    for row in data:
        patient_id = row[0]  # Remove type information
        diagnostic_gene = row[3]  # Update the index due to the removed column
        if not diagnostic_gene:
            print(f"Skipping patient ID {patient_id} because no diagnostic gene was provided.")
            continue
        print(f"Searching combined file for patient ID {patient_id} and diagnostic gene {diagnostic_gene}...")
        with open(f"{patient_id}_combined.tsv", "r") as combined_file:
            tsv_reader = csv.reader(combined_file, delimiter="\t")
            try:
                print(f'debugtemp_') # next(tsv_reader)  # skip the header
            except StopIteration:
                print(f"The combined TSV file {patient_id}_combined.tsv is empty or only contains the header.")
            else:
                for i, combined_row in enumerate(tsv_reader):
                    if combined_row[10] == diagnostic_gene:
                        writer.writerow([patient_id, i + 1, "\t".join(combined_row)])   # Remove type_id from the output

print("Processing raw_output.csv and creating new_output.csv...")
# Open the input file
with open("raw_output.csv", "r") as file:
    lines = file.readlines()

# Split the data in the third column and write the updated data to a new file
with open("data_output.csv", "w") as file:
    for line in lines:
        line = line.strip().split(",")
        line[2:2] = line[2].split("\t")  # Change index due to the removed column
        file.write(",".join(line) + "\n")

def move_files():
    # Check if there are any files ending with 'combined.tsv' in the current directory
    files_to_move = [f for f in os.listdir() if f.endswith('combined.tsv')]

    if not files_to_move:
        print("No files ending with 'combined.tsv' found.")
        return

    # Ask for user confirmation
    confirmation = input("This will override pre-existing Combined Files folder, type yes to confirm: ")

    if confirmation.lower() == "yes":
        # Check if 'Combined Files' directory exists and remove it
        if os.path.exists('Combined Files'):
            shutil.rmtree('Combined Files')
        
        # Create 'Combined Files' directory
        os.makedirs('Combined Files')

        # Move files to 'Combined Files' directory
        for file in files_to_move:
            shutil.move(file, os.path.join('Combined Files', file))
        
        print(f"Moved {len(files_to_move)} files to 'Combined Files' folder.")

    else:
        print("Operation cancelled.")

move_files()

print("Finished!")

elapsed_time = time.time() - start_time
print(f"Time elapsed: {elapsed_time} seconds")
