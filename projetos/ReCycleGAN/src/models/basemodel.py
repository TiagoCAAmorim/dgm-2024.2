"""Module with BaseModel class."""
from abc import ABC, abstractmethod
from torch import optim

class BaseModel(ABC):
    """Generic class for models."""
    def __init__(self, device='cpu'):
        """
        Initialize the BaseModel.
        Args:
        - device: 'cuda' or 'cpu'.
        """
        self.device = device

    @abstractmethod
    def forward(self, *inputs):
        """
        Abstract method for forwarding inputs through the model.
        """

    @abstractmethod
    def compute_loss(self, *inputs):
        """
        Abstract method for computing losses during training.
        """

    @abstractmethod
    def optimize(self, *inputs):
        """
        Abstract method for optimizing the model during training.
        """

    @abstractmethod
    def save_model(self, path):
        """
        Save the current model state.
        """
        # torch.save(self.state_dict(), path)

    @abstractmethod
    def load_model(self, path):
        """
        Load a saved model state.
        """
        # self.load_state_dict(torch.load(path))

    def setup_optimizers(self, model_params, lr=0.0002, beta1=0.5, beta2=0.999):
        """
        Setup optimizers for the model with default learning rate and betas.
        """
        return optim.Adam(model_params, lr=lr, betas=(beta1, beta2))
