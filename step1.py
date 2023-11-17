#!/usr/bin/python3
#Importing the subprocess module to execute external commands
import subprocess

#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
#build a string called query to contain protein name and taxon_group
#define the command of searching in NCBI as cmd
#using subprocess run the command and capture its output and errors
def efetch_fasta_ncbi(protein_name, taxon_group):
    print("Starting querying from NCBI")
    query = f"{protein_name}[Protein] AND {taxon_group}[Organism] NOT PARTIAL" 
    cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    #check if the command excuted successfully,if not then raise an exception
    if result.returncode != 0:
        print("An error occurred in efetch_fasta_ncbi function")
        return None
    
    print("Finished querying from NCBI")#tell the user their query is finish
    return result.stdout # return the standard output in fasta format

#count the sequence nuber of the output and return it to 'fasta_data'
def count_sequences_in_fasta(fasta_data):
    return fasta_data.count('>')

#show the user's input on the screen to confirm

def get_user_inputs():#create an infinite loop,execute code until encounter a return statement
    while True:
        protein_name = input("Enter the protein name: ").strip()
        if not protein_name:
            print("Protein name annot be empty.Please enter a valid protein name.")
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

#define a main function 
#define the protein and taxon group according to the user's input
def main():
    try:#add an error trapping to check the code
        while True:
          protein_name,taxon_group = get_user_inputs() 
          fasta_data = efetch_fasta_ncbi(protein_name, taxon_group)
      
          if fasta_data:
              sequence_count = count_sequences_in_fasta(fasta_data)#count the number of fasta data
              print(f"Number of sequence found: {sequence_count}")#print the count to the screen
        
              if input("Do you want to save the results to a file? (y/n): ").lower() == "y":
                  filename = protein_name.replace(" ", "_") + ".fasta"#using `replace` methond to name the out put file using the queried protein name
                  save_output_to_file(fasta_data, filename)
              if input("Do you want to continue querying other sequences? (y/n): ").lower() != "y":
                  break
          else:
              print("No results found for the given protein name and organism. Please try again.")
              if input("Do you want to try again? (y/n): ").lower() != "y":
                  break
    except Exception as e:
        print(f"An error occurred: {e}")

#check whether the script is run as a master program,if is ,the variable '__name__' will be set to main and main function will be called, allowing other scripts to use the functions defined in this script, without executing the code in the main function.
if __name__ == "__main__":
    main()