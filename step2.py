#!/usr/bin/python3
import os
import subprocess

# Define the run_clustalo function
def run_clustalo(input_fasta, output_fasta="aligned.fasta", num_threads=64, output_dir=None):
    # Create the directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_fasta = os.path.join(output_dir, output_fasta)
    else:
        output_fasta = os.path.join(os.getcwd(), output_fasta)

    # Define the Clustal Omega command
    clustalo_command = [
        "clustalo",
        "-i", input_fasta,
        "-o", output_fasta,
        "--force",
        "--auto",
        "--threads", str(num_threads),
        "--verbose"
    ]

    try:
        print("Running command:", ' '.join(clustalo_command))
        subprocess.run(clustalo_command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error occurred while running ClustalO:")
        print(e)
        return None  # Return None if an error occurs
    except Exception as e:
        print("An unexpected error occurred:")
        print(e)
        return None  # Return None if an unexpected error occurs

    # Return the path to the output file
    return output_fasta

# Main program
def main():
    input_file = input("Enter the input FASTA file name: ")
    output_dir_choice = input("Do you want to save the aligned file in a specific directory? (y/n): ")

    if output_dir_choice.lower() == "y":
        output_directory_name = input("Enter the name of the output directory: ")
        aligned_fasta = run_clustalo(input_file, output_dir=output_directory_name)
    else:
        aligned_fasta = run_clustalo(input_file)

    if aligned_fasta:
        print(f"Aligned sequences saved to {aligned_fasta}")
    else:
        print("Alignment was not successful.")

if __name__ == "__main__":
    main()
