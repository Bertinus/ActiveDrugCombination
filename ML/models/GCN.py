import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import ML.utils.register as register
from torch_geometric.utils import to_dense_adj
from torch.nn import Parameter


@register.setmodelname('GCN')
class GCN(torch.nn.Module):
    def __init__(self, num_node_features):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 16)
        self.conv2 = GCNConv(16, 16)

        self.predictor = Parameter(torch.randn((16, 16)))
        # self.predictor = Parameter(torch.randn((1026, 1026)))

        self.criterion = torch.nn.MSELoss()

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        # Predict synergy score for all possible pairs of drugs
        scores = x[:data.number_of_drugs].mm(self.predictor).mm(x[:data.number_of_drugs].T)

        return scores

    def loss(self, output, data):

        # Restrict ourselves to pairs for which we have ground truth
        mask = to_dense_adj(data.edge_index_ddi)[0]
        output *= mask

        ground_truth = to_dense_adj(data.edge_index_ddi, edge_attr=data.edge_attr_ddi)[0, :, :, 0].float()

        # Sanity check: restrict ourselves to the firs 50 drugs to see if we can overfit

        output = output[:50, :50]
        ground_truth = ground_truth[:50, :50]

        return self.criterion(output, ground_truth)


