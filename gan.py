import dnnlib
import legacy
import numpy as np
import PIL.Image
import torch

# Load pre-trained network
network_pkl = 'https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with dnnlib.util.open_url(network_pkl) as f:
    G = legacy.load_network_pkl(f)['G_ema'].to(device)  # type: ignore

# Generate synthetic images
z = torch.from_numpy(np.random.randn(1, G.z_dim)).to(device)
label = torch.zeros([1, G.c_dim], device=device)
img = G(z, label, truncation_psi=0.7, noise_mode='const')
img = (img * 127.5 + 128).clamp(0, 255).to(torch.uint8)
img = img.permute(0, 2, 3, 1)
PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save('synthetic_face.png')
