#!/usr/bin/python3
import os# import the os module to interact with the operating system.
import subprocess#Importing the subprocess module to execute external commands

# extract the first line of each suquence, for further analysis
def extract_species_and_sequences(fasta_data):
    species_dict = {}#create an empty dictionary to store species information and sequence data
    current_species = ""
    sequence_id = ""
    sequence_data = ""
    for line in fasta_data.split('\n'):#find each line begin with '>'
        if line.startswith('>'):
            if sequence_id and sequence_data:#add the found sequenceid and data to current species
                species_dict.setdefault(current_species, []).append((sequence_id, sequence_data))
            sequence_id = line.split()[0][1:]#Splits the string line into Spaces to form a list,extract and remove the first character of the sequence ID -- '>'
            species_parts = line.split('[')#split with '[' as separator
            current_species = species_parts[1].split(']')[0] if len(species_parts) > 1 else "Unknown"
            sequence_data = ""#reset sequence data for receiving new sequence data
        else:
            sequence_data += line#add the contents without '>' line to current sequence
    #process the last sequence (if any) and add it under the current species
    if sequence_id and sequence_data:
        species_dict.setdefault(current_species, []).append((sequence_id, sequence_data))
    return species_dict#returns a dictionary containing species information and sequence data

#define a function that takes as input a dictionary containing species information and sequence data
def user_select_species(species_dict):
    species_list = list(species_dict.keys())#get the names of all species and store them in a list
    print("Available species:")
    for i, species in enumerate(species_list, start=1):
        print(f"{i}. {species}")#print the number and name of each species

    #let the user to enter the selected species and give an example
    #parse the selection and converts it to a list of integers
    selected_indices = input("Select species by number (e.g., 2,5,7): ")
    selected_indices = [int(idx.strip()) - 1 for idx in selected_indices.split(',')]
    #get the species name according to the index selected by the user
    selected_species = [species_list[i] for i in selected_indices]
    selected_sequences = []#creates an empty list to store all the sequences selected by the user
    #add all sequences under that species to the list of selected sequences
    for species in selected_species:
        selected_sequences.extend(species_dict[species])
    return selected_species, selected_sequences
    
#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
#build a string called query to contain protein name and Organism
#define the command of searching in NCBI as cmd, using NCBI's E-utilities
#using subprocess run the command and capture its output and errors
def efetch_fasta_ncbi(protein_name, Organism, strict):
    print("Starting querying from NCBI")
    if strict:
        query = f"{protein_name}[Protein] AND {Organism}[Organism] NOT PARTIAL"
    else:
        query = f"{protein_name} AND {Organism}"   
    cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    #check if the command excuted successfully,if not then raise an exception
    if result.returncode != 0:
        print("An error occurred in efetch_fasta_ncbi function")
        return None
    print("Finished querying from NCBI")#tell the user their query is finish
    fasta_data = result.stdout
    
    
    # Split the output into individual sequences
    sequences = result.stdout.split('>')[1:]  # Splitting and removing the first empty string
    limited_sequences = sequences[:1000]  # Limiting to the first 1000 sequences
    fasta_data = '>' + '>'.join(limited_sequences)  # Re-joining the sequences into fasta format
    
    return result.stdout# return the standard output in fasta format
    
#count the sequence nuber of the output and return it to 'fasta_data'
def count_sequences_in_fasta(fasta_data):
    return fasta_data.count('>')

#show the user's input on the screen to confirm
def get_user_inputs():#create an infinite loop,execute code until encounter a return statement
    while True:
        protein_name = input("Enter the protein name: ").strip()
        taxon_group = input("Enter the Organism: ").strip()#check if the input is empty
        strict_search = input("Do you want a strict search? (y/n): ").lower().strip()
    
        if not protein_name or not taxon_group:
            print("Your input cannot be empty. Please enter a valid protein name.")
            continue
        #print the user's input on the screen to confirm
        print(f"Your protein name is: '{protein_name}'")
        print(f"Your taxon group is: '{taxon_group}'")
        if input("Do you confirm your inputs? (y/n): ").lower() == "y":
            return protein_name, taxon_group,strict_search == 'y'
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
        "-i", input_fasta, 
        "-o", output_fasta,
        "--force",# Overwrite an existing output file
        "--auto",# Choose the most appropriate strategy and parameters automatically
        "--threads", "64"#using 64 threads to raise the speed
    ]
    subprocess.run(clustalo_command, check=True)# Run the Clustal Omega command
    return output_fasta

#Plot conservation of a sequence alignment using 'plotco'
def run_plotcon(input_fasta, output_dir):
    output_file = os.path.join(output_dir, "plotcon_output")
    if os.path.exists(output_file):
        print(f"Warning: '{output_file}' already exists. Please remove or rename it before running this script.")
        return output_file
    plotcon_command1 = [
        "plotcon",
        "-sequence", input_fasta,
        "-graph", "png",#define the format of the output graph into 'png'
        "-winsize", "4",#define the winsize into 4 in default
        "-goutfile", output_file,
    ]
    plotcon_command2 = [
    "plotcon",
    "-sequence", input_fasta,
    "-graph", "x11",# display the generated graph directly in an X11 window
    "-winsize", "4"
    ]
    subprocess.run(plotcon_command1, check=True)#generate 2 plots, one for save and one for output
    subprocess.run(plotcon_command2, check=True)
    print(f"Plotcon output generated: {output_file}")
    return output_file    
    
#define a funciton using foe motif scan
def motif_scan_for_each_sequence(selected_sequences, output_dir):
    for sequence_id, sequence in selected_sequences:
        process_sequence(sequence_id, sequence, output_dir)

#define the function to run patmatmptifs
def process_sequence(sequence_id, sequence, output_dir):
    output_motif = os.path.join(output_dir, f"motif_scan_{sequence_id}.txt")
    motifscan_command = [
        "patmatmotifs",
        "-full",
        "-sequence", "stdin",#input the parsed sequence for motif scan
        "-outfile", output_motif
    ]
    print(f"Starting motif scan for {sequence_id}")

    motif_scan_result = subprocess.run(motifscan_command, input= sequence, text=True, capture_output=True)

    if motif_scan_result.returncode != 0:
        print(f"Error in patmatmotifs for {sequence_id}:", motif_scan_result.stderr)
    else:
        if motif_scan_result.stderr:
            print(f"Messages from patmatmotifs for {sequence_id}:", motif_scan_result.stderr)
        print(f"Patmatmotifs for {sequence_id} completed successfully.")
        print(motif_scan_result.stdout)

#add some other EMBOSS commands
#using extractalign to extract the aligned sequeces
def extract_aligned_sequences(input_fasta, output_dir):
    # Specifies the path to the output file
    output_fasta = os.path.join(output_dir, "extracted_aligned_sequences.fasta")

    #Define extractalign commands and parameter
    extractalign_command = [
        "extractalign",
        "-sequence", input_fasta,
        "-outseq", output_fasta,
    ]

    #Run the extractalign command
    subprocess.run(extractalign_command, check=True)
    print(f"Extracted aligned sequences saved to {output_fasta}")



#define a main function 
#define the protein and taxon group according to the user's input
def main():
    try:#add an error trapping to check the code
        while True:
            protein_name, Organism, strict = get_user_inputs()
            print("User inputs received.")

            fasta_data = efetch_fasta_ncbi(protein_name, Organism, strict)
            if fasta_data:
                sequence_count = count_sequences_in_fasta(fasta_data)
                print(f"Number of sequences found: {sequence_count}")
                
               # Save the raw query data to a file named after the protein
                raw_fasta_filename = f"{protein_name.replace(' ', '_')}.fasta"
                save_output_to_file(fasta_data, raw_fasta_filename)
                
                #If the user wants to refine the species, use the user-selected sequence
                restrict_species = input("Do you want to refine sequences by species? (y/n): ").lower().strip()
                selected_species_str = ""  # Default value for species string
                #If the user choose Yes, only process the selected species
                if restrict_species == 'y':
                    species_dict = extract_species_and_sequences(fasta_data)
                    print(species_dict)
                    selected_species, selected_sequences = user_select_species(species_dict)
                    selected_species_str = '_'.join(selected_species).replace(' ', '_')
                else:
                    #if user choose 'n',process all the sequences
                    #Converts fasta data to a format suitable for modular scanning
                    all_sequences = fasta_data.split('>')
                    selected_sequences = [(seq.split('\n', 1)[0], '\n'.join(seq.split('\n', 1)[1:])) for seq in all_sequences if seq.strip()]
                    
                output_dir = create_output_dir(f"{protein_name.replace(' ', '_')}_{selected_species_str}_output")
                
                #Save the processed sequence to a file
                fasta_filename = os.path.join(output_dir, "processed_sequences.fasta")
                fasta_data_to_analyze = '\n'.join(['>' + id+"\n" + seq for id, seq in selected_sequences])
                save_output_to_file(fasta_data_to_analyze, fasta_filename)
                print("FASTA data saved to file.")

                #run clustalo and plotcon
                aligned_fasta = run_clustalo(fasta_filename, output_dir)
                plotcon_output = run_plotcon(aligned_fasta, output_dir)

                #run motif scan function
                motif_scan_for_each_sequence(selected_sequences, output_dir)
                
                # Asks the user whether to extract aligned sequences
                extract_align = input("Do you want to extract aligned sequences? (y/n): ").lower().strip()
                if extract_align == 'y': #Calls the function that extracts the alignment sequence
                    extract_aligned_sequences(aligned_fasta, output_dir)                

            if input("Do you want to continue querying other sequences? (y/n): ").lower() != "y":
                print("Exiting the program.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")       
        
#check whether the script is run as a master program,if is ,the variable '__name__' will be set to main and main function will be called, allowing other scripts to use the functions defined in this script, without executing the code in the main function.
main()