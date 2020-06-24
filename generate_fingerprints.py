from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import pandas as pd

"""
rdkit and pytorch geometric are not compatible together. You should use a specific conda environment with rdkit, 
numpy and pandas install to run this script
"""


def get_fingerprint(smile, radius, nBits):
    if smile == 'none':
        return np.array([-1]*nBits)
    try:
        return np.array(AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smile), radius, nBits))
    except:
        return np.array([-1]*nBits)


if __name__ == '__main__':

    radius = 4
    nBits = 1024

    drug_chemical_info = pd.read_csv("Data/DrugComb/drug_chemical_info.csv", encoding='iso-8859-1')
    all_fp = drug_chemical_info['smilesString'].apply(lambda s: get_fingerprint(s, radius=radius, nBits=nBits))

    # Convert to dataframe
    all_fp = list(all_fp)
    all_fp = [list(fp) for fp in all_fp]
    all_fp = pd.DataFrame(all_fp, columns=["fp" + str(i) for i in range(nBits)])

    # Add fingerprints to drug info and save
    drug_chemical_info = pd.concat((drug_chemical_info, all_fp), axis=1)
    drug_chemical_info.to_csv("Data/DrugComb/drug_chemical_info_with_fingerprints.csv", index=None)
