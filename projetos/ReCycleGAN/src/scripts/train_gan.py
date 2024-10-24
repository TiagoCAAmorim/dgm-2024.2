# pylint: disable=C0413,E0401
"""Trains and Tests CycleGAN"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.utils.run import init_cyclegan_train, train_cyclegan

def train(parameters):
    """Trains the CycleGAN model."""
    model, data_loaders = init_cyclegan_train(parameters)
    model = train_cyclegan(model, data_loaders, parameters)

if __name__ == '__main__':

    base_folder = Path(__file__).resolve().parent.parent.parent
    params = {
        'restart_path': None, #base_folder / 'no_sync/test_model_7/cycle_gan_epoch_9.pth', #None
        'parameters_path': None, #base_folder / 'no_sync/test_model_7/hyperparameters.json', #None

        'data_folder': base_folder / 'data/external/nexet',
        'csv_type': '_filtered',
        'out_folder': base_folder / 'no_sync/test_model_7',
        'use_cuda': True,
        'run_wnadb': False,
        'wandb_name': 'Test_Other',
        'print_memory': True,

        "num_epochs" : 15,
        "checkpoint_interval" : 3,
        "n_samples" : 4, #None => For testing only!!!

        'batch_size' : 64,
        'img_height': 256,
        'img_width': 256,

        'channels': 3, #3
        'n_features': 32, #64
        'n_residual_blocks': 2, #9
        'n_downsampling': 2, #2
        'norm_type': 'instance', #'instance' ('batch', 'instance' or 'none')
        'add_skip': True, #False

        'use_replay_buffer': True, #False
        'replay_buffer_size': 50, #50

        'vanilla_loss': False, #True
        'cycle_loss_weight': 10, #10
        'id_loss_weight': 5, #5
        'plp_loss_weight': 1, #5
        'plp_step': 16, #0
        'plp_beta': 0.99, #0.99

        'lr' : 0.0002, #0.0002
        'beta1' : 0.5,  #0.5
        'beta2' : 0.999, #0.999

        'step_size': 10, #20
        'gamma': 0.5, #0.5

        'amp': True, #False
    }

    train(params)
