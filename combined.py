#!/usr/bin/python3
import os
import subprocess


def efetch_fasta_ncbi(protein_name, taxon_group):
    print("Starting querying from NCBI")
    query = f"{protein_name}[Protein] AND {taxon_group}[Organism] NOT PARTIAL"
    cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("An error occurred in efetch_fasta_ncbi function")
        return None
    print("Finished querying from NCBI")
    return result.stdout

def count_sequences_in_fasta(fasta_data):
    return fasta_data.count('>')

def get_user_inputs():
    while True:
        protein_name = input("Enter the protein name: ").strip()
        if not protein_name:
            print("Protein name cannot be empty. Please enter a valid protein name.")
            continue
        taxon_group = input("Enter the taxon group: ").strip()
        if not taxon_group:
            print("Taxon group cannot be empty. Please enter a valid taxon group.")
            continue
        print(f"Your protein name is: '{protein_name}'")
        print(f"Your taxon group is: '{taxon_group}'")
        if input("Do you confirm your inputs? (y/n): ").lower() == "y":
            return protein_name, taxon_group
        else:
            print("Please re-enter your inputs.")

def save_output_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)
    print(f"Data saved to {filename}")

def create_output_dir(output_dir):
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    else:
        return os.getcwd()

def run_clustalo(input_fasta, output_dir):
    output_fasta = os.path.join(output_dir, "aligned.fasta")
    clustalo_command = [
        "clustalo",
        "-i", input_fasta,
        "-o", output_fasta,
        "--force",
        "--auto",
        "--threads", "64"
    ]
    subprocess.run(clustalo_command, check=True)
    return output_fasta

def run_plotcon(input_fasta, output_dir):
    output_file = os.path.join(output_dir, "plotcon_output.png")
    if os.path.exists(output_file):
        print(f"Warning: '{output_file}' already exists. Please remove or rename it before running this script.")
        return output_file
    plotcon_command = [
        "plotcon",
        "-sequence", input_fasta,
        "-graph", "png",
        "-winsize", "4",
        "-goutfile", output_file,
    ]
    subprocess.run(plotcon_command, check=True)
    return output_file

def main():
    try:
        while True:
            protein_name, taxon_group = get_user_inputs()
            fasta_data = efetch_fasta_ncbi(protein_name, taxon_group)
            if fasta_data:
                sequence_count = count_sequences_in_fasta(fasta_data)
                print(f"Number of sequences found: {sequence_count}")
                filename = protein_name.replace(" ", "_") + ".fasta"
                save_output_to_file(fasta_data, filename)
                output_dir = protein_name.replace(" ", "_") + "_output"
                
                os.makedirs(output_dir, exist_ok=True)
                aligned_fasta = run_clustalo(filename, output_dir)
                print(f"Aligned sequences saved to {aligned_fasta}")
                plotcon_output = run_plotcon(aligned_fasta, output_dir)
                print(f"Conservation plot saved to {plotcon_output}")
                
            if input("Do you want to continue querying other sequences? (y/n): ").lower() != "y":
                break
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

