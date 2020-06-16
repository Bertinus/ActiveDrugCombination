"""
Script that saves all the CIDs present in the Decagon dataset and saves them in a file formated to be uploader at
https://pubchem.ncbi.nlm.nih.gov/pc_fetch/pc_fetch.cgi

The CID_list.txt file is uploaded to PubChem in order to retrieve the SMILES
SMILES are made available in the file SMILES.txt
"""
import pandas as pd

# Load Decagon data

mono_effect = pd.read_csv("Data/Decagon/bio-decagon-mono.csv")
combo_effect = pd.read_csv("Data/Decagon/bio-decagon-combo.csv")
drug_target = pd.read_csv("Data/Decagon/bio-decagon-targets.csv")
drug_target_all = pd.read_csv("Data/Decagon/bio-decagon-targets-all.csv")


# Retrieve all CIDs and save it as a list

CID_list = list(mono_effect["STITCH"])
CID_list.extend(list(combo_effect['STITCH 1']))
CID_list.extend(list(combo_effect['STITCH 2']))
CID_list.extend(list(drug_target['STITCH']))
CID_list.extend(list(drug_target_all['STITCH']))

with open("Data/CID_list.txt", 'w') as output:
    for row in set(CID_list):
        output.write(str(row)[3:] + '\n')
