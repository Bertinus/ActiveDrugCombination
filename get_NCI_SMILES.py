from urllib.request import urlopen
import pandas as pd
from tqdm import tqdm


def name_to_smiles(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles'
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return '-1'


compound_names = pd.read_csv("Data/NCI/ComboCompoundNames_all.txt", sep="\t", header=None)

# There is a parsing problem with the last 4 rows
for r in range(1613, 1617):
    compound_names.loc[r][1] = compound_names.loc[r][0][8:]
    compound_names.loc[r][0] = compound_names.loc[r][0][:6]

name_list = list(compound_names[1])

smiles_list = []

for name in tqdm(name_list):
    smiles_list.append(name_to_smiles(name))

compound_names['smiles'] = smiles_list

compound_names.to_csv("Data/NCI/ComboCompoundNames_all_with_smiles.csv", index=False)
