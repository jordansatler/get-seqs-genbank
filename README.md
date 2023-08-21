# Get GenBank Sequences

This script will retrieve mitochondrial sequence data from GenBank based on a user-provided species list. Data are from the mitochondrial genome with genes that contain cytochrome in gene name. Script targets cytochrome oxidase-subunit I (in addition to other genes) because this is the primary barcoding gene. Maximum threshold of 50 sequences per species. For species above this threshold, 50 sequences will be selected at random. Species-specific data sets in fasta format will be placed in new folder.  

At the command line, one will enter their species list and their email address.


usage:  
```python
    python get_seqs_genbank.py speciesList.txt your.email@email.com
```

***
The species list file has each species on its own line:

Anopheles melas  
Bactrocera depressa  
Drosophila pseudoobscura  
Ovis canadensis  
Sceloporus undulatus  
...
***
