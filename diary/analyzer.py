import torch
from torch import nn
import torch.nn.functional as F

# StableDiffusion
from diffusers import DiffusionPipeline

# Load openjourney pretrained model
def get_diffusion_model():
    pipeline = DiffusionPipeline.from_pretrained("../models/prompthero-openjourney", local_files_only=True)
    return pipeline

device = 'cuda'
if torch.backends.mps.is_available():
	device = 'mps'
        
device = torch.device(device)

def generate_image(prompt):
    pipeline = pipeline.to(device)
    image = pipeline(prompt, guidance_scale=9, num_inference_steps=25).images[0]
    return image