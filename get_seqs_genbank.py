#!/usr/bin/env python

"""
Retrieve mitochondrial sequence data from GenBank
based on a user-provided species list. Data are
from the mitochondrial genome with genes that contain
cytochrome in gene name. Maximum threshold of 50
sequences per species. For species above this threshold, 
50 sequences will be selected at random. Species-specific 
data sets in fasta format will be placed in new folder.

usage:
    python get_seqs_genbank.py speciesList.txt
"""

import os
import sys
import time
import random
import shutil
import datetime
from Bio import SeqIO
from Bio import Entrez

def get_species_list(file):
    """get list of selected species"""
    with open(file, "r") as infile:
        return [i.strip() for i in infile]

def get_genbank_handle(species):
    """retrieve genbank record IDs for species"""
    handle = Entrez.esearch(
            db = "nucleotide",
            term = "{0}[Orgn] AND {1} AND {2}".format(species, 
                                                      "cytochrome[All Fields]",
                                                      "mitochondrion[filter]"),
            retmax = "10000",
            idtype = "acc")
    return Entrez.read(handle)

def get_sequences(IDs, Nseqs):
    """get COI sequences from genbank"""
    # randomly subsample sequences if species has more
    if len(IDs) > Nseqs:
        to_get = random.sample(IDs, Nseqs)
    else:
        to_get = IDs

    handle = Entrez.efetch(db = "nucleotide",
            id = to_get,
            rettype = "gb",
            retmode = "text")

    # return GenBank ID, description, and COI sequence
    return {record.id:[record.description, record.seq]
            for record in SeqIO.parse(handle, "genbank") 
            if record.seq.defined is not False}

def write_to_fasta_file(species, seqs):
    """write sequences to fasta file"""
    fname = species.replace(" ", "_") + ".fa"
    with open(fname, "w") as out:
        for k, v in sorted(seqs.items()):
            out.write(">{0} {1}\n{2}\n".format(k, v[0], v[1]))
    return fname

def write_to_file(species, Ntotal, Nsampled, file):
    """write sampling information to file"""
    with open("sampling_info.txt", file) as out:
        out.write("{0}\t{1}\t{2}\n".format(species, Ntotal, Nsampled))

def main():
    if len(sys.argv) != 2:
        print("python get_seqs_genbank.py speciesList")
        sys.exit()

    # get species list for NCBI search
    spList = get_species_list(sys.argv[1])

    # provide your email for NCBI
    Entrez.email = "YourEmail@example.com"

    # make folder for resulting fasta files
    if os.path.exists("./fasta"):
        print("fasta folder already exists")
        sys.exit()
    os.mkdir("./fasta")

    # write header to new sampling info file
    write_to_file("Species", "Ntotal_GenBank", "Nsampled_GenBank", "w")

    # get COI data for each species
    for idx, i in enumerate(spList):
        print("{0}\t{1} of {2}\t{3}".format(datetime.datetime.now(), 
                                       idx + 1, 
                                       len(spList), 
                                       i))
        record = get_genbank_handle(i)

        # make sure taxon has at least two sequences
        if int(record["Count"]) < 2:
            continue

        # set max number of sequences [N = 50]
        seqs = get_sequences(record["IdList"], 50)
        outF = write_to_fasta_file(i, seqs)
        shutil.move(outF, "./fasta")

        # append COI count for species to file
        write_to_file(i, len(record["IdList"]), len(seqs), "a")

        # add time delay to not overload NCBI server
        time.sleep(3)
  
if __name__ == '__main__':
    main()
