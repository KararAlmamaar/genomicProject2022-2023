import os

# path to the directory containing the .tsv files
path = "lirical-files"

# loop through each file in the directory
for filename in os.listdir(path):
    if filename.endswith(".tsv"):
        print(f"Processing {filename}")
        # read the contents of the file into memory
        with open(os.path.join(path, filename), "r") as file:
            contents = file.read()
        # replace commas with dashes in the diseaseName column
        contents = contents.replace('diseaseName\t', 'diseaseName-replaced\t').replace(',', '-')
        # write the modified contents back to the file
        with open(os.path.join(path, filename), "w") as file:
            file.write(contents)

# open the liricalOutput.csv file for writing
with open("liricalOutput.csv", "w") as f:
    # write the header row
    f.write("fileName,rank,diseaseName,diseaseCurie,pretestprob,posttestprob,compositeLR,entrezGeneId,variants\n")
    # loop through each file in the directory
    for filename in os.listdir(path):
        if filename.endswith(".tsv"):
            print(f"Processing {filename}")
            # open the file
            with open(os.path.join(path, filename), "r") as file:
                lines = file.readlines()
                header_row = None
                # find the header row
                for i, line in enumerate(lines):
                    values = line.strip().split("\t")
                    if values[0] == "rank":
                        header_row = i
                        break
                if header_row is None:
                    print(f"Header row not found in {filename}")
                else:
                    # loop through the remaining rows in the file
                    for line in lines[header_row+1:]:
                        values = line.strip().split("\t")
                        # check if the value in the 6th column is greater than 0
                        if "-" in values[5]:
                            print(f"Found dash in {filename}, line: {values[0]}")
                        if float(values[5].replace(",", "").replace("-", "")) > 0:
                            # write the file name, rank, and whole row to the liricalOutput.csv file
                            f.write(f"{filename[:-4]},{values[0]},{values[1]},{values[2]},{values[3]},{values[4]},{values[5]},{values[6]},{values[7]}\n")


print(f"Complete.")
