#!/usr/bin/python3
import os#import os module to make a directory
import subprocess#Importing the subprocess module to execute external commands

#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
#build a string called query to contain protein name and taxon_group
#define the command of searching in NCBI as cmd
#using subprocess run the command and capture its output and errors
def efetch_fasta_ncbi(protein_name, taxon_group, include_not_partial):
    print("Starting querying from NCBI")
    if include_not_partial == "y":
        query = f"{protein_name}[Protein] AND {taxon_group}[Organism] NOT PARTIAL"
    else:
        query = f"{protein_name}[Protein] AND {taxon_group}[Organism]"
    cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    #check if the command excuted successfully,if not then raise an exception
    if result.returncode != 0:
        print("An error occurred in efetch_fasta_ncbi function")
        return None
    print("Finished querying from NCBI")#tell the user their query is finish
    return result.stdout# return the standard output in fasta format
    
#count the sequence nuber of the output and return it to 'fasta_data'
def count_sequences_in_fasta(fasta_data):
    return fasta_data.count('>')

#show the user's input on the screen to confirm
def get_user_inputs():#create an infinite loop,execute code until encounter a return statement
    while True:
        protein_name = input("Enter the protein name: ").strip()
        taxon_group = input("Enter the taxon group: ").strip()#check if the input is empty
        include_not_partial = input("Do you want to query sequences only match the specified input?(y/n): ").strip().lower()
        if not protein_name or not taxon_group:
            print("Your input cannot be empty. Please enter a valid protein name.")
            continue
        #print the user's input on the screen to confirm
        print(f"Your protein name is: '{protein_name}'")
        print(f"Your taxon group is: '{taxon_group}'")
        if input("Do you confirm your inputs? (y/n): ").lower() == "y":
            return protein_name, taxon_group, include_not_partial
        else:
            print("Please re-enter your inputs.")

#save the output in to a file
def save_output_to_file(data, filename):#data need to be saved and the file name
    with open(filename, 'w') as file:#using write mode to open a file
        file.write(data)#write the data into the file
    print(f"Data saved to {filename}")

#Create the output directory (if it does not exist) and return the directory path
#If a valid output directory path is provided, try to create the directory, and no error is raised if the directory already exists
def create_output_dir(output_dir):
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    else:
        return os.getcwd()#If no valid output directory path is provided, return the path to the current working directory

# Define a function called "run_clustalo" that takes input parameters: input_fasta, output_fasta, number of threads, output_directory
def run_clustalo(input_fasta, output_dir):
    output_fasta = os.path.join(output_dir, "aligned.fasta")
    clustalo_command = [
        "clustalo",
        "-i", input_fasta, #-full??
        "-o", output_fasta,
        "--force",# Overwrite an existing output file
        "--auto",# Choose the most appropriate strategy and parameters automatically
        "--threads", "64"#using 64 threads to raise the speed
    ]
    subprocess.run(clustalo_command, check=True)# Run the Clustal Omega command
    return output_fasta

#Plot conservation of a sequence alignment using 'plotco'
def run_plotcon(input_fasta, output_dir):
    output_file = os.path.join(output_dir, "plotcon_output.png")
    if os.path.exists(output_file):
        print(f"Warning: '{output_file}' already exists. Please remove or rename it before running this script.")
        return output_file
    plotcon_command = [
        "plotcon",
        "-sequence", input_fasta,
        "-graph", "png",#define the format of the output graph into 'png'
        "-winsize", "4",
        "-goutfile", output_file,
    ]
    subprocess.run(plotcon_command, check=True)
    return output_file

#define a main function 
#define the protein and taxon group according to the user's input
def main():
    try:#add an error trapping to check the code
        while True:
            protein_name, taxon_group,include_not_partial = get_user_inputs()
            fasta_data = efetch_fasta_ncbi(protein_name, taxon_group, include_not_partial)
            if fasta_data:
                sequence_count = count_sequences_in_fasta(fasta_data)#count the number of fasta data
                print(f"Number of sequences found: {sequence_count}")#print the count to the screen
            else:
                print("No data returned from NCBI.")
                filename = protein_name.replace(" ", "_") + ".fasta"#using `replace` methond to name the out put file using the queried protein name
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
        
#check whether the script is run as a master program,if is ,the variable '__name__' will be set to main and main function will be called, allowing other scripts to use the functions defined in this script, without executing the code in the main function.
if __name__ == "__main__":
    main()

