import csv

def load_gene_directory(file_path):
    gene_directory = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            gene_id = row[1]
            symbol = row[2]
            gene_directory[gene_id] = symbol
    return gene_directory

def replace_gene_id_with_symbol(gene_directory, input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(output_file, fieldnames)
        writer.writeheader()
        
        for row in reader:
            gene_id = row['entrezGeneId'].split(':')[1]
            symbol = gene_directory.get(gene_id)
            if symbol:
                row['entrezGeneId'] = symbol
            else:
                print(f"Symbol not found for GeneID {gene_id}")
            writer.writerow(row)

# Set the file paths
gene_directory_file = 'GeneDirectory.csv'
input_file = 'liricalOutput.csv'
output_file = 'updatedOutput.csv'

try:
    # Load the gene directory
    gene_directory = load_gene_directory(gene_directory_file)

    # Replace GeneID with Symbol and save the updated output
    replace_gene_id_with_symbol(gene_directory, input_file, output_file)

    print("Replacement completed successfully. The updated output file is 'updatedOutput.csv'.")

except FileNotFoundError:
    print("File not found. Please check the file paths and try again.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
