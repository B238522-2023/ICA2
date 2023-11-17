#!/usr/bin/python3
#Importing the subprocess module to execute external commands
import subprocess

#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
def efetch_fasta_ncbi(protein_name, taxon_group):
    print("Starting querying from NCBI")
    #build a string called query to contain protein name and taxon_group
    query = f"{protein_name}[Protein] AND {taxon_group}[Organism] NOT PARTIAL"
    #define the command of searching in NCBI as cmd
    cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
    #using subprocess run the command and capture its output and errors
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    #check if the command excuted successfully,if not then raise an exception
    if result.returncode != 0:
        print("An error occurred in efetch_fasta_ncbi function")
        return None
    #tell the user their query is finish
    print("Finished querying from NCBI")
    #return the standard output in fasta format
    return result.stdout

#count the sequence nuber of the output and return it to 'fasta_data'
def count_sequences_in_fasta(fasta_data):
    return fasta_data.count('>')

#show the user's input on the screen to check
#define a function called get_user_input that takes two arguments 
def get_user_input(input_prompt, input_type):
    #create an infinite loop,execute code until encounter a return statement
    while True:
        user_input = input(input_prompt)
        #check if the user's input is valid,using strip function to remove whitespace,if result is empty,means the user's input has no valid content
        if not user_input.strip():#if the user's input is not empty,nothing happeneds here
            print(f"{input_type} cannot be empty. Please enter a valid {input_type}.")
            continue 
        print(f"Your input is: '{user_input}'") #let user confirm the input
    #if user confirmed the input, using it for the query
        if input("Do you confirm yout input? (y/n): ").lower() == "y":
            return user_input

#ask the user to name the filename
def get_filename_input(input_prompt):
  while True:
    filename = input(input_prompt)
    if not filename.strip():
      print("Filename cannot be empty.Please enter a valid filename.")#aviod empty input
      continue
    if not filename.lower().endswith('.fasta'):#add file extension '.fasta' 
      filename += '.fasta'
      print(f"Your filename is: '{filename}'")
      if input("Do you confirm your filename? (y/n): ").lower() == "y":
        return filename
      

#save the output fasta into a file
def save_output_to_file(data, filename):
  #open the file in a write mode
    with open(filename, 'w') as file:
  #write the data into a file
        file.write(data)
    print(f"Data saved to {filename}")

while True:
    #ask the user to input protein name
    protein_name = get_user_input("Enter the protein name:", "protein name")
    #ask the user to input the taxon_group name
    taxon_group = get_user_input("Enter the taxon_group name: ", "taxon_group name")
    # Executing the query based on user input
    fasta_result = efetch_fasta_ncbi(protein_name, taxon_group)

    # Printing the query results
    if fasta_result:
    #count the number of sequences queried
        sequence_count = count_sequences_in_fasta(fasta_result)
        print(f"Number of sequences found: {sequence_count}")
    #ask the user to put the output into a file and let them to name the filename
    
        if input("Do you want to save the results to a file? (y/n): ").lower() == "y":
            filename = get_filename_input("Enter the filename to save (it will be saved with .fasta extension): ")
            save_output_to_file(fasta_result, filename)
      
   
    #ask if the user want to query other proteins and organisms
    #if they do not want to query other sequences, then finish the query
        if input("Do you want to continue querying other sequences? (y/n): ").lower() != "y":
            break
    else:#if the sequence number is 0,means find nothing from NCBI,using 'print'to tell the user
        print("No results found for the given protein name and organism. Please try again.")
        if input("Do you want to try again? (y/n): ").lower() != "y":
            break
