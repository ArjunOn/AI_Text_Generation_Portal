"""
Run sampling but decode tokens robustly: if the GPT-2 encoder can't decode a token id
we replace it with a placeholder token '<|UNK|>'. This helps when the trained model's
token ids extend beyond the encoder's expected range.

Usage (from project dir):
  .\.venv\Scripts\python.exe sample_safe.py --out_dir=out-custom --device=cpu --num_samples=3 --max_new_tokens=120
"""
import os
import argparse
from contextlib import nullcontext
import torch
import tiktoken
from model import GPTConfig, GPT

parser = argparse.ArgumentParser()
parser.add_argument('--out_dir', type=str, default='out')
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--num_samples', type=int, default=3)
parser.add_argument('--max_new_tokens', type=int, default=120)
parser.add_argument('--start', type=str, default='\n')
args = parser.parse_args()

ckpt_path = os.path.join(args.out_dir, 'ckpt.pt')
checkpoint = torch.load(ckpt_path, map_location=args.device)
gptconf = GPTConfig(**checkpoint['model_args'])
model = GPT(gptconf)
state_dict = checkpoint['model']
unwanted_prefix = '_orig_mod.'
for k,v in list(state_dict.items()):
    if k.startswith(unwanted_prefix):
        state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
model.load_state_dict(state_dict)
model.to(args.device)
model.eval()

# Prepare encoder — assume GPT-2 by default
enc = tiktoken.get_encoding('gpt2')
encode = lambda s: enc.encode(s, allowed_special={"<|endoftext|>"})

def safe_decode(token_ids):
    # try full decode first
    try:
        return enc.decode(token_ids)
    except Exception:
        parts = []
        for t in token_ids:
            try:
                parts.append(enc.decode([t]))
            except Exception:
                parts.append('<|UNK|>')
        return ''.join(parts)

# prepare prompt
start = args.start
if start.startswith('FILE:'):
    with open(start[5:], 'r', encoding='utf-8') as f:
        start = f.read()
start_ids = encode(start)
import torch
x = (torch.tensor(start_ids, dtype=torch.long, device=args.device)[None, ...])

with torch.no_grad():
    with nullcontext() if args.device == 'cpu' else torch.amp.autocast(device_type='cuda'):
        samples = []
        for k in range(args.num_samples):
            y = model.generate(x, args.max_new_tokens)
            token_ids = y[0].tolist()
            decoded = safe_decode(token_ids)
            samples.append(decoded)
            print(decoded)
            print('---------------')

        # also save to file for inspection
        out_dir = os.path.join(args.out_dir, 'samples')
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'generated_examples.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            for s in samples:
                f.write(s + '\n' + '---------------' + '\n')

        print(f"Wrote samples to {out_path}")
