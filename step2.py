#!/usr/bin/python3
import os
import subprocess #####!!!delete when alaign the script

#Define a function called "run_clustalo" that takes input parameters:input_fasta,output_fasta,number of threads output_directory
#'None' is a default value,If the user does not provide output_dir, the output file will be saved in the current working directory because the default is None.
def run_clustalo(input_fasta, output_fasta="aligned.fasta", num_threads=64, output_dir=None):
    # create the directory if it doesn't exist,if it is existed, will raise no error
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        #using 'os.path.join' function to create the full path of the output directory, which was named by the user.
        output_fasta = os.path.join(output_dir, output_fasta)
    else:
        # use the current working directory if no output_dir provided
        output_fasta = os.path.join(os.getcwd(), output_fasta)

    # Define the Clustal Omega command with necessary arguments
    clustalo_command = [
        "clustalo", 
        "-i", input_fasta, 
        "-o", output_fasta, 
        "--force", #overwrite an existing output file
        "--auto", #choose the most appropriate strategy and paraneters automatically
        "--threads", str(num_threads),  # Add number of threads 64
        "--verbose"  # proved more detailed running information to help debug or understand the conparison progress
    ]
    try:
      print("Running command:", ' '.join(clustalo_command))#combine all the command into a string and seperated by a space
      # Run the Clustal Omega command
      subprocess.run(clustalo_command, check=True)
    except subprocess.CalledProcessError as e:
      print("Error occurred while running ClustalO:")
      print(e)
      #if any errors occur,return to None
      return None
      # Return the path to the output file
      return output_fasta

# Ask the user to input the input file name
input_file = input("Enter the input FASTA file name: ")
# Ask the user if they want to specify an output directory
output_dir = input("Do you want to save the aligned file in a specific directory? (y/n): ")

if output_dir.lower() == "y":
    # Ask the user to name the output directory
    output_directory_name = input("Enter the name of the output directory: ")
    # Call the function to perform the alignment with the specified output directory
    aligned_fasta = run_clustalo(input_file, output_dir=output_directory_name)
else:
    # Call the function to perform the alignment without specifying an output directory
    aligned_fasta = run_clustalo(input_file)

if aligned_fasta:  
    # Print the path to the aligned file
    print(f"Aligned sequences saved to {aligned_fasta}")
else:
    print("Alignment process failed.")
