import torch
import numpy as np
import random
import os
import dill as pickle


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

