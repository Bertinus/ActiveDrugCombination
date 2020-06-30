import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import ML.utils.register as register
from torch.nn import Parameter


@register.setmodelname('GCN')
class GCN(torch.nn.Module):
    def __init__(self, num_node_features):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 16)
        self.conv2 = GCNConv(16, 16)

        self.predictor = Parameter(torch.randn((16, 16)))

        self.criterion = torch.nn.MSELoss()

    def forward(self, data):
        """
        :param n_samples: Set >1 if you want to perform several passes
        :return:
        """
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        # Predict synergy score for all possible pairs of drugs
        scores = x[:data.number_of_drugs].mm(self.predictor).mm(x[:data.number_of_drugs].T)

        return scores

    def loss(self, output, mask, ground_truth):

        # Restrict ourselves to pairs for which we have ground truth
        output *= mask

        # Sanity check: restrict ourselves to the firs 50 drugs to see if we can overfit
        # output = output[:50, :50]
        # ground_truth = ground_truth[:50, :50]

        # We normalize by the number of non zero values
        return 1/mask.sum() * self.criterion(output, ground_truth)


@register.setmodelname('Monte_Carlo_GCN')
class MonteCarloGCN(torch.nn.Module):
    def __init__(self, num_node_features, n_samples):
        """
        GCN that will perform n_samples forward passes (only in the predictor)

        :param num_node_features: dimension of node attributes in the dataset
        :param n_samples: number of samples to be drawn for each pass
        """
        super(MonteCarloGCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 16)
        self.conv2 = GCNConv(16, 16)

        self.predictor = Parameter(torch.randn((16, 16)))
        # self.predictor = Parameter(torch.randn((1026, 1026)))

        self.n_samples = n_samples
        self.criterion = torch.nn.MSELoss()

    def forward(self, data):
        """
        :param n_samples: Set >1 if you want to perform several passes
        :return: scores: tensor of shape [n_samples, n_drugs, n_drugs]
        """
        if not self.training:  # If the model is in eval mode, only forward once
            return self.single_pass_forward(data)

        # Predict scores n_samples times
        list_of_scores = [self.single_pass_forward(data)
                          for _ in range(self.n_samples)]

        # Concatenate
        list_of_scores = [score[None, :, :] for score in list_of_scores]
        scores = torch.cat(list_of_scores)

        return scores

    def single_pass_forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        # Predict scores n_samples times
        return x[:data.number_of_drugs].mm(self.predictor).mm(x[:data.number_of_drugs].T)

    def loss(self, output, mask, ground_truth):

        # Restrict ourselves to pairs for which we have ground truth
        output *= mask

        if not self.training:  # If the model is in eval mode, do not normalize with n_samples
            return 1/mask.sum() * self.criterion(output, ground_truth)

        # We normalize by the number of non zero values and number of samples
        return 1/mask.sum() * 1/self.n_samples * self.criterion(output, ground_truth)





