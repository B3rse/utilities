# utilities
Useful scripts (Python v. 2.7).

## **Contacts**
Michele Berselli, <berselli.michele@gmail.com>

## query_ensembl_promoters.py
It is a script that allows to retrieve the promoter regions for a desired list of genes from ENSEMBL. Genes symbols should be provided as a column in a plain text file. The user can specify the number of bases upstream and downstream the TSS. The output is saved in a fasta file. Download errors are handled and reported in a log file if unsolvable (e.g. identifier not found). 

#### Usage 
	query_ensembl_promoters.py [-h] -i INPUTFILE -p PROMOTERLENGTH [-d DOWNSTREAMLENGTH] -o OUTPUTFILE

#### Parameters  
  - **-h**, **--help**            
  - **-i**, **--inputfile** PATH/TO/INPUTFILE --> *input file with gene names*
  - **-p**, **--promoterlength** PROMOTERLENGTH --> *length of the promoter region, region upstream TSS*
  - **-d**, **--downstreamlength** DOWNSTREAMLENGTH --> *length of the region retrieved downstream TSS*
  - **-o**, **--outputfile** PATH/TO/OUTPUTFILE --> *output file to save results*
