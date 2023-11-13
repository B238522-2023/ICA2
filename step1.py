#!/usr/bin/python3
#Importing the subprocess module to execute external commands
import subprocess
#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
def efetch_fasta_ncbi(protein_name, organism):
    try:
        #build a string called query to contain protein name and prganism
        query = f"{protein_name} AND {organism}[ORGN]"
        #define the command of searching in NCBI as cmd
        cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
        #using subprocess run the command and capture its output and errors
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        #check if the command excuted successfully,if not then raise an exception
        if result.returncode != 0:
            raise Exception(result.stderr)
        #return the standard output in fasta format
        return result.stdout
    except Exception as e:
        #if there is an exception, print the error and return None
        print(f"An error occurred: {e}")
        return None

# Main program entry point
if __name__ == "__main__":
    # Prompting the user to input the protein name and the organism name
    protein_name = input("Enter the protein name: ")
    organism = input("Enter the organism name: ")

    # Executing the query based on user input
    fasta_result = efetch_fasta_ncbi(protein_name, organism)
    # Printing the query results
    print(fasta_result)


