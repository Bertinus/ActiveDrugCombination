import torch
from torch_geometric.data import Data
import pandas as pd
import numpy as np


def load_original_data():
    """
    Load the original DrugCombDB dataset into a torch geometric Data object
    :return: a torch_geometric.data.Data object

    x: node feature matrix: the last column indicates whether a node is a drug or not
        (shape [num_nodes, num_node_features])

    edge_index: edges between drug-drug, drug-protein and protein-protein
        (shape [2, num_edges])

    edge_attr: edge feature matrix containing 4 synergy scores ('ZIP', 'Bliss', 'Loewe', 'HSA') for drug-drug edges,
    zero otherwise
        (shape [num_edges, num_edge_features])
    """
    print("Loading original data, only happens the first time")

    # Load dataframes
    drug_chemical_info_with_fp = pd.read_csv("Data/DrugComb/drug_chemical_info_with_fingerprints.csv")
    drugcomb_scored = pd.read_csv("Data/DrugComb/drugcombs_scored.csv")
    drug_protein_link = pd.read_csv("Data/DrugComb/drug_protein_links.tsv", sep="\t")
    protein_protein_interactions = pd.read_csv("Data/DrugComb/protein_protein_links.txt", sep=' ')

    ####################################################################################################################
    # Build node feature matrix
    ####################################################################################################################
    drug_chemical_info_with_fp['has_fp'] = drug_chemical_info_with_fp['fp0'].apply(lambda fp: fp != -1)
    drug_chemical_info_with_fp['is_drug'] = 1
    drug_chemical_info_with_fp = drug_chemical_info_with_fp.rename(columns={'drugName': 'name'})

    print("Number of drugs", len(drug_chemical_info_with_fp))

    # Retrieve all protein names
    all_proteins = set(protein_protein_interactions['protein1']). \
        union(set(protein_protein_interactions['protein2'])).union(set(drug_protein_link['protein']))
    protein_nodes = pd.DataFrame(all_proteins, columns=['name'])
    protein_nodes['is_drug'] = 0
    protein_nodes['has_fp'] = False

    print("Number of proteins", len(protein_nodes))

    nodes = pd.concat((drug_chemical_info_with_fp, protein_nodes), ignore_index=True, sort=False)
    nodes = nodes.fillna(-1)
    x = nodes.drop(['cIds', 'drugNameOfficial', 'molecularWeight', 'smilesString', 'name'], axis=1)
    x = x.to_numpy().astype(np.int)

    ####################################################################################################################
    # Build edge index
    ####################################################################################################################

    # Dictionaries to retrieve indices
    ##################################################
    cid_to_idx_dict = {nodes.at[i, 'cIds']: i for i in range(len(nodes))}
    name_to_idx_dict = {nodes.at[i, 'name']: i for i in range(len(nodes))}

    # PPI
    ##################################################
    protein_protein_interactions['idx_prot1'] = protein_protein_interactions['protein1'].apply(
        lambda s: name_to_idx_dict[s])
    protein_protein_interactions['idx_prot2'] = protein_protein_interactions['protein2'].apply(
        lambda s: name_to_idx_dict[s])

    edge_index_ppi = protein_protein_interactions[['idx_prot1', 'idx_prot2']].to_numpy().T
    edge_attr_ppi = np.zeros((edge_index_ppi.shape[1], 4))

    print("Number of Prot-Prot Interactions", edge_index_ppi.shape[1])

    # Drug Protein interaction
    ##################################################
    drug_protein_link['idx_chemical'] = drug_protein_link['chemical'].\
        apply(lambda s: cid_to_idx_dict[s] if s in cid_to_idx_dict.keys() else -1)
    drug_protein_link['idx_prot'] = drug_protein_link['protein'].apply(lambda s: name_to_idx_dict[s])

    edge_index_dpi = drug_protein_link[drug_protein_link['idx_chemical'] != -1][['idx_chemical', 'idx_prot']].\
        to_numpy().T
    edge_attr_dpi = np.zeros((edge_index_dpi.shape[1], 4))

    print("Number of Drug-Prot Interactions", edge_index_dpi.shape[1])

    # Drug Synergy scores
    ##################################################
    drugcomb_scored['idx_Drug1'] = drugcomb_scored['Drug1'].apply(
        lambda s: name_to_idx_dict[s] if s in name_to_idx_dict.keys() else -1)
    drugcomb_scored['idx_Drug2'] = drugcomb_scored['Drug2'].apply(
        lambda s: name_to_idx_dict[s] if s in name_to_idx_dict.keys() else -1)

    # Remove measures that have been performed several times.
    drug_drug_edges = drugcomb_scored[drugcomb_scored[['idx_Drug1', 'idx_Drug2']].duplicated() == False]
    # Remove measures for which there is no information about one of the drugs
    drug_drug_edges = drug_drug_edges[drug_drug_edges['idx_Drug1'] != -1]
    drug_drug_edges = drug_drug_edges[drug_drug_edges['idx_Drug2'] != -1]

    edge_index_ddi = drug_drug_edges[['idx_Drug1', 'idx_Drug2']].to_numpy().T
    edge_attr_ddi = drug_drug_edges[['ZIP', 'Bliss', 'Loewe', 'HSA']].to_numpy()

    print("Number of Drug-Drug Interactions", edge_index_ddi.shape[1])

    # Aggregate different edges
    ##################################################
    edge_index = np.concatenate((edge_index_ppi, edge_index_dpi, edge_index_ddi), axis=1)
    edge_attr = np.concatenate((edge_attr_ppi, edge_attr_dpi, edge_attr_ddi), axis=0)
    # Edges are directed, we need to feed them both ways
    edge_index = np.concatenate((edge_index, edge_index[::-1, :]), axis=1)
    edge_attr = np.concatenate((edge_attr, edge_attr), axis=0)

    return Data(x=torch.tensor(x, dtype=torch.float),
                edge_index=torch.tensor(edge_index, dtype=torch.long),
                edge_attr=edge_attr)
