#!/usr/bin/python3
#Importing the subprocess module to execute external commands
import subprocess
import argparse
#Defining the function fasta_ncbi to execute the NCBI query and get the output in fasta format
def efetch_fasta_ncbi(protein_name, organism):
	print("Starting query from NCBI")
	try:
		#build a string called query to contain protein name and organism
		query = f"{protein_name} AND {organism}[ORGN]"
		#define the command of searching in NCBI as cmd
		cmd = f"esearch -db protein -query '{query}' | efetch -format fasta"
		#using subprocess run the command and capture its output and errors
		result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

		#check if the command excuted successfully,if not then raise an exception
		if result.returncode != 0:
			raise Exception(result.stderr)

		print("Finished query from NCBI")
		#return the standard output in fasta format
		return result.stdout
	except Exception as e:
		print("An error occurred in efetch_fasta_ncbi function")
		#If any error occurs, throw an exception
		raise

#define if the user's input is empty or not
def validate_input(input_str, input_type):
	#if the input is empty,then tell the user their input is empty and modify it
	if not input_str.strip():
		raise ValueError(f"{input_type} cannot be empty. Please enter a valid {input_type.lower()}.")



while True:
	try:
		#ask the user to input protein name
		protein_name = input("Enter the protein name:")
		#check if the protein name is valid
		validate_input(protein_name, "Protein name")
		#ask the user to input the organism name
		organism = input("Enter the organism name: ")
		#check if it is valid
		validate_input(organism, "Organism name")

		# Executing the query based on user input
		fasta_result = efetch_fasta_ncbi(protein_name, organism)
		#if not find in NCBI, raise the error
		if not fasta_result:
			raise ValueError("No results found for the given protein name and organism. Please try again.")

	# Printing the query results
		print(fasta_result)
		break  # if successfully queried exit the loop

	# Capture and print input errors of the user
	except Exception as e:
		# capture and print errors while obtaining data from NCBI
		print(f"An error occurred while fetching data: {e}")

		# ask the user if they want to try again or exit.
		retry = input("Do you want to try again? (yes/no): ").lower()
		if retry != "yes":
			break


