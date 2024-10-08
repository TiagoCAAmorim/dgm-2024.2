from basemodel import BaseModel
from networks import Generator, Discriminator, CycleGANLoss
import torch
import torch.nn as nn

class CycleGAN(BaseModel):
    def __init__(self, input_nc, output_nc, lr=0.0002, beta1=0.5, beta2=0.999, device='cpu'):
        """
        Initializes the CycleGAN model, optimizers, and losses.
        """
        super(CycleGAN, self).__init__(device)

        # Initialize generators and discriminators
        self.gen_AtoB = Generator(input_nc, output_nc).to(self.device)
        self.gen_BtoA = Generator(input_nc, output_nc).to(self.device)
        self.dis_A = Discriminator(input_nc).to(self.device)
        self.dis_B = Discriminator(input_nc).to(self.device)
        
        # Define losses
        self.adversarial_loss = CycleGANLoss().to(self.device)
        self.cycle_loss = nn.L1Loss().to(self.device)
        self.identity_loss = nn.L1Loss().to(self.device)

        # Setup optimizers using the BaseModel's helper function
        self.optimizer_G = self.setup_optimizers(
            list(self.gen_AtoB.parameters()) + list(self.gen_BtoA.parameters()), lr, beta1, beta2
        )
        self.optimizer_D_A = self.setup_optimizers(self.dis_A.parameters(), lr, beta1, beta2)
        self.optimizer_D_B = self.setup_optimizers(self.dis_B.parameters(), lr, beta1, beta2)

    def forward(self, real_A, real_B):
        """
        Forward pass for both generators.
        """
        fake_B = self.gen_AtoB(real_A)
        fake_A = self.gen_BtoA(real_B)
        recovered_A = self.gen_BtoA(fake_B)
        recovered_B = self.gen_AtoB(fake_A)
        return fake_B, fake_A, recovered_A, recovered_B

    def compute_loss(self, real_A, real_B):
        """
        Computes the total loss for generators and discriminators using CycleGANLoss for adversarial loss.
        """
        fake_B, fake_A, recovered_A, recovered_B = self.forward(real_A, real_B)
        
        # Identity loss
        loss_identity_A = self.identity_loss(self.gen_BtoA(real_A), real_A)
        loss_identity_B = self.identity_loss(self.gen_AtoB(real_B), real_B)

        # GAN loss using CycleGANLoss
        loss_G_AtoB = self.adversarial_loss(self.dis_B(fake_B), target_is_real=True)
        loss_G_BtoA = self.adversarial_loss(self.dis_A(fake_A), target_is_real=True)

        # Cycle-consistency loss
        loss_cycle_A = self.cycle_loss(recovered_A, real_A)
        loss_cycle_B = self.cycle_loss(recovered_B, real_B)

        # Total generator loss
        loss_G = (loss_G_AtoB + loss_G_BtoA) + 10 * (loss_cycle_A + loss_cycle_B) + 5 * (loss_identity_A + loss_identity_B)

        # Discriminator A loss (real vs fake)
        loss_real_A = self.adversarial_loss(self.dis_A(real_A), target_is_real=True)
        loss_fake_A = self.adversarial_loss(self.dis_A(fake_A.detach()), target_is_real=False)
        loss_D_A = (loss_real_A + loss_fake_A) * 0.5

        # Discriminator B loss (real vs fake)
        loss_real_B = self.adversarial_loss(self.dis_B(real_B), target_is_real=True)
        loss_fake_B = self.adversarial_loss(self.dis_B(fake_B.detach()), target_is_real=False)
        loss_D_B = (loss_real_B + loss_fake_B) * 0.5
        
        return loss_G, loss_D_A, loss_D_B

    def optimize(self, real_A, real_B):
        """
        Perform one optimization step for the generators and discriminators.
        """
        loss_G, loss_D_A, loss_D_B = self.compute_loss(real_A, real_B)

        # Optimize Generators
        self.optimizer_G.zero_grad()
        loss_G.backward()
        self.optimizer_G.step()

        # Optimize Discriminator A
        self.optimizer_D_A.zero_grad()
        loss_D_A.backward()
        self.optimizer_D_A.step()

        # Optimize Discriminator B
        self.optimizer_D_B.zero_grad()
        loss_D_B.backward()
        self.optimizer_D_B.step()

        return loss_G.item(), loss_D_A.item(), loss_D_B.item()
    
    def save_model(self, epoch, path='cycle_gan_model.pth'):
        """
        Save the current model state.
        
        Args:
        - epoch: Current epoch number.
        - path: Path to save the model.
        """
        torch.save({
            'epoch': epoch,
            'gen_AtoB_state_dict': self.gen_AtoB.state_dict(),
            'gen_BtoA_state_dict': self.gen_BtoA.state_dict(),
            'dis_A_state_dict': self.dis_A.state_dict(),
            'dis_B_state_dict': self.dis_B.state_dict(),
            'optimizer_G_state_dict': self.optimizer_G.state_dict(),
            'optimizer_D_A_state_dict': self.optimizer_D_A.state_dict(),
            'optimizer_D_B_state_dict': self.optimizer_D_B.state_dict(),
        }, path)

    def load_model(self, path):
        """
        Load a saved model state.
        
        Args:
        - path: Path to the saved model.
        """
        checkpoint = torch.load(path)
        self.gen_AtoB.load_state_dict(checkpoint['gen_AtoB_state_dict'])
        self.gen_BtoA.load_state_dict(checkpoint['gen_BtoA_state_dict'])
        self.dis_A.load_state_dict(checkpoint['dis_A_state_dict'])
        self.dis_B.load_state_dict(checkpoint['dis_B_state_dict'])
        self.optimizer_G.load_state_dict(checkpoint['optimizer_G_state_dict'])
        self.optimizer_D_A.load_state_dict(checkpoint['optimizer_D_A_state_dict'])
        self.optimizer_D_B.load_state_dict(checkpoint['optimizer_D_B_state_dict'])
