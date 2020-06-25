import torch
from torch_geometric.data import InMemoryDataset
from ML.utils import load_original_data


class DrugCombDBDataset(InMemoryDataset):

    def __init__(self, root="Data", transform=None, pre_transform=None):
        self.name = "".lower()
        super(DrugCombDBDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return 'data.pt'

    def download(self):
        pass

    def process(self):
        data = load_original_data()
        data = data if self.pre_transform is None else self.pre_transform(data)
        data, slices = self.collate([data])
        torch.save((data, slices), self.processed_paths[0])

    def __repr__(self):
        return '{}{}()'.format(self.__class__.__name__, self.name.capitalize())


if __name__ == '__main__':
    ds = DrugCombDBDataset()
