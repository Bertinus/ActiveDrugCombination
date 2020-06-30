from sklearn.model_selection import train_test_split
from torch_geometric.utils import to_dense_adj
from ML.utils.utils import expand_to_right_shape
import torch
from torch.nn.functional import relu


########################################################################################################################
# Initialization
########################################################################################################################

def initialize_query_mask(data, start_with_n_examples):
    # Split edge indices and attributes
    index_queried, index_to_be_queried, attr_queried, attr_to_be_queried = \
        train_test_split(data.index_train.T, data.attr_train, train_size=start_with_n_examples, shuffle=True)

    index_queried, index_to_be_queried = index_queried.T, index_to_be_queried.T

    # Add lists to data object
    data.index_queried = index_queried
    data.index_to_be_queried = index_to_be_queried
    data.attr_queried = attr_queried
    data.attr_to_be_queried = attr_to_be_queried

    # Compute mask and ground_truth
    mask_queried = to_dense_adj(index_queried)[0]
    mask_to_be_queried = to_dense_adj(index_to_be_queried)[0]

    ground_truth_queried = to_dense_adj(index_queried, edge_attr=attr_queried)[0, :, :, 0].float()
    ground_truth_to_be_queried = to_dense_adj(index_to_be_queried, edge_attr=attr_to_be_queried)[0, :, :, 0].float()

    # Make sure that the masks have the right dimension
    mask_queried = expand_to_right_shape(mask_queried, data.number_of_drugs)
    mask_to_be_queried = expand_to_right_shape(mask_to_be_queried, data.number_of_drugs)
    ground_truth_queried = expand_to_right_shape(ground_truth_queried, data.number_of_drugs)
    ground_truth_to_be_queried = expand_to_right_shape(ground_truth_to_be_queried, data.number_of_drugs)

    # Add mask and ground_truth to data object
    data.mask_queried = mask_queried
    data.mask_to_be_queried = mask_to_be_queried
    data.ground_truth_queried = ground_truth_queried
    data.ground_truth_to_be_queried = ground_truth_to_be_queried

    return data

########################################################################################################################
# Acquisition methods
########################################################################################################################


def expected_improvement(output, data):
    s_max = data.ground_truth_queried.max()
    output = relu(output - s_max)
    return output.sum(dim=0)


def random_acquisition(output, data):
    return torch.randn((output.shape[1], output.shape[2]))


########################################################################################################################
# Query
########################################################################################################################


def query(output, data, acquisition=expected_improvement, query_n_at_a_time=1):

    # All acquisition scores among all drug pairs
    acquisition_scores = acquisition(output, data)

    # Restrict ourselves to pairs to be queried. We set the scores of pairs that are not to be queried to -1
    acquisition_scores *= data.mask_to_be_queried
    acquisition_scores += -1 + data.mask_to_be_queried

    for _ in range(query_n_at_a_time):
        # Choose pair to query
        idx_queried_pair = torch.argmax(acquisition_scores)
        # retrieve original 2D index
        idx_queried_pair = (idx_queried_pair / acquisition_scores.shape[0],
                            idx_queried_pair % acquisition_scores.shape[0])

        # Update masks and ground_truth
        data.mask_to_be_queried[idx_queried_pair[0], idx_queried_pair[1]] = 0
        data.mask_queried[idx_queried_pair[0], idx_queried_pair[1]] = 1
        data.ground_truth_queried[idx_queried_pair[0], idx_queried_pair[1]] = \
            data.ground_truth_to_be_queried[idx_queried_pair[0], idx_queried_pair[1]]
        data.ground_truth_to_be_queried[idx_queried_pair[0], idx_queried_pair[1]] = 0

        acquisition_scores[idx_queried_pair[0], idx_queried_pair[1]] = -1

    return data


