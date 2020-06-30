# Predicting the effect of drug combinations: an Active Learning Approach

## DrugComb data

We use data from ```http://drugcombdb.denglab.org/download```

Original paper: [link](https://academic.oup.com/nar/article/48/D1/D871/5609522)

Run ````get_drug_comb_data.py```` to download this data

Ressource to understand the different synergy scores: [link](https://www.researchgate.net/publication/282281738_Searching_for_Drug_Synergy_in_Complex_Dose-Response_Landscapes_Using_an_Interaction_Potency_Model/link/560a5b4208ae1396914bba65/download)

## Environment setup

Set up a conda environment for the project using the provided specification file:

```conda create --name myenv --file spec-file.txt```

Note: if you want to generate the fingerprints again using ```generate_fingerprints.py```, you should use another conda environment with ```rdkit``` installed (rdkit is not provided in the specification file)


## Running the pipeline

From the ````ActiveDrugCombination```` directory, run:  

````python ML/main.py --config config/test.yml````

You can edit the configuration file to change the model you use, the optimizer parameters and other general parameters.

## Results visualization

You can use the the notebook `````Notebooks/Result_Exploration.ipynb`````. 

Just change the ````experiment_name```` and ````experiment ID```` 
in the first cell of the notebook (you should choose those parameters in the config file before running the pipeline)