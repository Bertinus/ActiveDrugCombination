import torch
from ML.datasets.drug_comb_db import DrugCombDBDataset
from ML.utils.utils import set_seed, save_results
import copy
import ML.utils. configuration as configuration
import numpy as np
import os
from ML.utils.acquisition import query, initialize_query_mask
from ML.utils.utils import train_valid_split

########################################################################################################################
# Epoch training and validation
########################################################################################################################


def train_epoch(model, optimizer, data, epoch, is_active=False, query_every_k_epochs=None, query_n_at_a_time=None):
    """
    :param is_active: Boolean
    :param query_every_k_epochs: query new drug pairs every <query_every_k_epochs> epochs
    :param n_samples: Set >1 if you want to get several sampled predictions to be used in the acquisition function
    :param query_n_at_a_time: Number of pairs to query at the same time
    :param acquisition: Acquisition function that will be used
    """
    model.train()

    optimizer.zero_grad()
    out = model.forward(data)

    if is_active and epoch % query_every_k_epochs == 0:
        # query new drug pairs
        data = query(out, data, query_n_at_a_time=query_n_at_a_time)

    if is_active:
        loss = model.loss(out, data.mask_queried, data.ground_truth_queried)
    else:
        loss = model.loss(out, data.mask_train, data.ground_truth_train)

    loss.backward()
    optimizer.step()

    loss = loss.detach()

    print('epoch {} Mean train loss: {:.4f}'.format(
        epoch, loss))

    return loss.tolist(), data


def evaluate_epoch(model, data, epoch):
    model.eval()

    with torch.no_grad():
        out = model.forward(data)
        loss = model.loss(out, data.mask_valid, data.ground_truth_valid)

    loss = loss.detach()

    print('epoch {} Mean valid loss: {:.4f}'.format(
        epoch, loss))

    return loss.tolist()


########################################################################################################################
# Main training loop
########################################################################################################################


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

    data = train_valid_split(data, train_size=0.8)

    is_active = cfg['active']
    if is_active:
        print("Active training")
        query_every_k_epochs = cfg['query_every_k_epochs']
        query_n_at_a_time = cfg['query_n_at_a_time']
        start_with_n_examples = cfg['start_with_n_examples']
        data = initialize_query_mask(data, start_with_n_examples)
    else:
        print("Regular training")
        query_every_k_epochs = None
        query_n_at_a_time = None

    best_valid_loss = np.inf
    best_model, best_epoch = None, None
    all_train_losses, all_valid_losses = [], []

    for epoch in range(n_epochs):

        train_loss, data = train_epoch(model=model, optimizer=optimizer, data=data, epoch=epoch, is_active=is_active,
                                       query_every_k_epochs=query_every_k_epochs, query_n_at_a_time=query_n_at_a_time)
        valid_loss = evaluate_epoch(model=model, data=data, epoch=epoch)

        if valid_loss < best_valid_loss:
            best_model = copy.deepcopy(model)
            best_epoch = epoch
            best_valid_loss = valid_loss

        all_train_losses.append(train_loss)
        all_valid_losses.append(valid_loss)

        print("queried so far", int(data.mask_queried.sum()))

    results = {"exp_name": exp_name,
               "exp_id": exp_id,
               "config": cfg,
               "seed": seed,
               "losses": {"train": all_train_losses, "valid": all_valid_losses},
               "best_epoch": best_epoch,
               "best_model": best_model,
               "last_model": model}

    save_results(results, output_dir)
