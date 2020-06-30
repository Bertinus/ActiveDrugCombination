import torch
import numpy as np
import random
import os
import dill as pickle
from torch_geometric.utils import to_dense_adj
from sklearn.model_selection import train_test_split


def expand_to_right_shape(m, target_shape):
    """
    :param m: tensor to be reshaped
    :param target_shape:
    :return: tensor of shape (target_shape, target_shape) with zeros added
    """
    output = torch.zeros((target_shape, target_shape))
    output[:m.shape[0], :m.shape[1]] = m

    return output


def save_results(results, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save best model
    output_name = "best_model_{}.pth.tar".format(results["exp_id"])
    torch.save(results["best_model"].state_dict(), os.path.join(output_dir, output_name))

    # Save last model
    output_name = "last_model_{}.pth.tar".format(results["exp_id"])
    torch.save(results["last_model"].state_dict(), os.path.join(output_dir, output_name))

    # Save the rest of the results dictionary
    del results["best_model"]
    del results["last_model"]
    output_name = "results_{}.pkl".format(results["exp_id"])
    with open(os.path.join(output_dir, output_name), 'wb') as f:
        pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)


def set_seed(seed, cuda=False):
    """
    Fix the seed for numpy, python random, and pytorch.
    """
    print('pytorch/random seed: {}'.format(seed))

    # Numpy, python, pytorch (cpu), pytorch (gpu).
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    if cuda:
        torch.cuda.manual_seed_all(seed)


def train_valid_split(data, train_size=0.8):
    """
    Adds four attributes to data:
        mask_train,
        mask_valid,
        ground_truth_train,
        ground_truth_valid
    """

    # Split edge indices and attributes
    index_train, index_valid, attr_train, attr_valid = train_test_split(data.edge_index_ddi.T,
                                                                        data.edge_attr_ddi,
                                                                        train_size=train_size,
                                                                        shuffle=True)

    index_train, index_valid = index_train.T, index_valid.T

    # Create masks (adjacency matrix wrt edges in each split)
    mask_train = to_dense_adj(index_train)[0]
    mask_valid = to_dense_adj(index_valid)[0]

    # Create ground truths. Note: here we restrict ourselves to the first synergy score
    ground_truth_train = to_dense_adj(index_train, edge_attr=attr_train)[0, :, :, 3].float()
    ground_truth_valid = to_dense_adj(index_valid, edge_attr=attr_valid)[0, :, :, 3].float()

    # Add train and valid indices to data object
    data.index_train = index_train
    data.index_valid = index_valid
    data.attr_train = attr_train
    data.attr_valid = attr_valid

    # Add mask and ground_truth attributes to data object
    data.mask_train = mask_train
    data.mask_valid = mask_valid
    data.ground_truth_train = ground_truth_train
    data.ground_truth_valid = ground_truth_valid

    return data


