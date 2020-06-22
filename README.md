# Predicting the effect of drug combinations: an Active Learning Approach


## Decagon and NCI data

We use data from DECAGON and NCI which is downloaded from: 
- http://snap.stanford.edu/decagon/ 
- https://wiki.nci.nih.gov/display/NCIDTPdata/NCI-ALMANAC

You can use the ```get_data.sh``` and ```unzip_data.sh``` scripts to download them

For the Decagon data, we retrieve the SMILES of the compound from https://pubchem.ncbi.nlm.nih.gov/pc_fetch/pc_fetch.cgi. 
We create a list of CIDs with the ````save_CID_list.py```` script and upload the list to PubChem. 
The resulting file is already provided in ```Data/Decagon/SMILES.txt```

For the NCI data, we retrieve SMILES using the ````get_NCI_SMILES.py```` script. The resulting file 
```Data/NCI/ComboCompoundNames_all_with_smiles.csv``` is already provided

## DRKG data

We use the Drug Repurposing Knowledge Graph from https://github.com/gnn4dr/DRKG

Run ```Utils.utils.py``` to download this data

## DrugComb data

We use data from ```http://drugcombdb.denglab.org/download```

Run ````get_drug_comb_data.py```` to download this data

Ressource to understand the different synergy scores: [link](https://www.researchgate.net/publication/282281738_Searching_for_Drug_Synergy_in_Complex_Dose-Response_Landscapes_Using_an_Interaction_Potency_Model/link/560a5b4208ae1396914bba65/download)

## Environment setup

Set up a conda environment for the project using the provided specification file:

```conda create --name myenv --file spec-file.txt```

