# utilities
Useful scripts (Python v. 3).

## **Contacts**
Michele Berselli, <berselli.michele@gmail.com>

## query_ensembl_promoters.py
A script that allows to retrieve the promoter regions for a desired list of genes from ENSEMBL. Genes symbols should be provided as a column in a plain text file. The user can specify the number of bases upstream and downstream the TSS. The output is saved in a fasta file. Download errors are handled and reported in a log file if unsolvable (e.g. identifier not found).

### Usage
`query_ensembl_promoters.py [-h] -i INPUTFILE -p PROMOTERLENGTH [-d DOWNSTREAMLENGTH] -o OUTPUTFILE`

### Parameters
  - **-h**, **--help**
  - **-i**, **--inputfile** PATH/TO/INPUTFILE --> *input file with gene names*
  - **-p**, **--promoterlength** PROMOTERLENGTH --> *length of the promoter region, region upstream TSS*
  - **-d**, **--downstreamlength** DOWNSTREAMLENGTH --> *length of the region retrieved downstream TSS*
  - **-o**, **--outputfile** PATH/TO/OUTPUTFILE --> *output file to save results*

## rest_api.py
A simple library that provides objects and methods to work with REST api based on requests.

### Dependencies
The library requires *requests* and *json* libraries.

### Usage
To use the library simply `import rest_api as ra` into your code.

### Objects

#### Entry
Entry is a general object that accepts any number of attributes that are stored as strings.

  - **Entry(** *dictionary* **)** to initialize the object with the attributes and corresponding values passed as the dictionary.

      `entry = ra.Entry(dictionary)`

  - **header_to_tsv( )** method to return all attributes names in a tsv format.

      `entry.header_to_tsv()`

  - **values_to_tsv( )** method to return all attributes values in a tsv format.

      `entry.values_to_tsv()`

### Functions

  - **GET_json(** *url* **)** requests a json from the url and check for errors. If request was successful error is 0 and json in returned, otherwise error is 1 and no json is returned.

      `json, error = ra.GET_json(url)`

  - **dict_structure(** *dictionary*, *expand=False*, *levels=[0,-1]* **)** returns the structure of the keys for dictionary. *expand* allows to expand values that are lists of dictionaries and returns the structure of first dictionary. *levels* allows to specify the range of levels to return [min, max], [.., -1] removes maximum depth limit.

      `ra.dict_structure(dictionary, expand=False, levels=[0,-1])`
