import torch
from ML.datasets.drug_comb_db import DrugCombDBDataset
from ML.utils.utils import set_seed, save_results
import copy
import ML.utils. configuration as configuration
import numpy as np
import os


def train_epoch(model, optimizer, data, epoch):
    model.train()

    optimizer.zero_grad()
    out = model.forward(data)
    loss = model.loss(out, data)

    loss.backward()
    optimizer.step()

    loss = loss.detach()

    print('epoch {} Mean train loss: {:.4f}'.format(
        epoch, loss))

    return loss.tolist()


def evaluate_epoch(model, data, epoch):
    model.eval()

    with torch.no_grad():
        out = model.forward(data)
        loss = model.loss(out, data)

    loss = loss.detach()

    print('epoch {} Mean valid loss: {:.4f}'.format(
        epoch, loss))

    return loss.tolist()


def train(cfg):

    exp_name = cfg['experiment_name']
    seed = cfg['seed']
    exp_id = cfg['exp_id']
    n_epochs = cfg['n_epochs']
    output_dir = os.path.join('results', cfg['experiment_name'])
    set_seed(seed)

    dataset = DrugCombDBDataset()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    data = dataset[0].to(device)
    model = configuration.setup_model(cfg)

    optimizer = configuration.setup_optimizer(cfg)(model.parameters())

    best_valid_loss = np.inf
    best_model, best_epoch = None, None
    all_train_losses, all_valid_losses = [], []

    for epoch in range(n_epochs):

        train_loss = train_epoch(model=model, optimizer=optimizer, data=data, epoch=epoch)

        valid_loss = evaluate_epoch(model=model, data=data, epoch=epoch)

        if valid_loss < best_valid_loss:
            best_model = copy.deepcopy(model)
            best_epoch = epoch
            best_valid_loss = valid_loss

        all_train_losses.append(train_loss)
        all_valid_losses.append(valid_loss)

    results = {"exp_name": exp_name,
               "exp_id": exp_id,
               "config": cfg,
               "seed": seed,
               "losses": {"train": all_train_losses, "valid": all_valid_losses},
               "best_epoch": best_epoch,
               "best_model": best_model,
               "last_model": model}

    save_results(results, output_dir)
