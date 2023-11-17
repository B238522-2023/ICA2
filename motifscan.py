#!/usr/bin/python3

import subprocess

command = [
    "patmatmotifs",
    "-full",
    "-sequence", "G6P.fasta",
    "-outfile", "G6P_motif.patmatmotifs"
]

result = subprocess.run(command, capture_output=True, text=True)


print(result.stdout)
if result.stderr:
    print("error:", result.stderr)

