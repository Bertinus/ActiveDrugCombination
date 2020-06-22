# Effect of drug combination prediction using Active Learning

## Data

The data we use is downloaded from: 
- http://snap.stanford.edu/decagon/ 
- https://wiki.nci.nih.gov/display/NCIDTPdata/NCI-ALMANAC

you can use the ```get_data.sh``` and ```unzip_data.sh``` scripts to download them

SMILES have been downloaded from from https://pubchem.ncbi.nlm.nih.gov/pc_fetch/pc_fetch.cgi after creating a 
list of all CIDs with ````save_CID_list.py````

## Environment setup

Set up a conda environment for the project using the provided specification file:

```conda create --name myenv --file spec-file.txt```

