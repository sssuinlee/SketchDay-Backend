import torch
from torch import nn
import torch.nn.functional as F

# KoBART
from transformers import PreTrainedTokenizerFast
from tokenizers import SentencePieceBPETokenizer
from transformers import BartForConditionalGeneration
# StableDiffusion
from diffusers import DiffusionPipeline

# Load KoBART summarize pretrained model
def tokenizer():
    tokenizer = PreTrainedTokenizerFast.from_pretrained('../models/kobart-summarization')
    return tokenizer

def get_kobart_model():
    model = BartForConditionalGeneration.from_pretrained('../models/kobart-summarization')
    model.eval()
    return model

# Load openjourney pretrained model
def get_diffusion_model():
    pipeline = DiffusionPipeline.from_pretrained("../models/prompthero-openjourney", local_files_only=True)
    return pipeline

device = 'cuda'
if torch.backends.mps.is_available():
	device = 'mps'
        
device = torch.device(device)

def summarize(text):
    model = get_model()
    tokenizer = tokenizer()
    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + \
        raw_input_ids + [tokenizer.eos_token_id]
    summary_ids = model.generate(torch.tensor([input_ids]),
                                    max_length=256,
                                    early_stopping=True,
                                    repetition_penalty=2.0)
    result = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
    return result

def generate_image(prompt):
    pipeline = pipeline.to(device)
    image = pipeline(prompt, guidance_scale=9, num_inference_steps=25).images[0]
    return image