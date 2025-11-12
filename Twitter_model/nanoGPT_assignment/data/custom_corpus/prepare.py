import os
import tiktoken
import numpy as np

# read local cleaned twitter corpus
input_file_path = os.path.join(os.path.dirname(__file__), 'cleaned_twitter_corpus.txt')
if not os.path.exists(input_file_path):
    raise FileNotFoundError(f"Expected input at {input_file_path}")

with open(input_file_path, 'r', encoding='utf-8') as f:
    data = f.read()

# optionally remove empty lines and join with newline to preserve tweet boundaries
# Here we treat the whole concatenated data as one sequence with newlines preserved
n = len(data)
train_data = data[:int(n*0.9)]
val_data = data[int(n*0.9):]

# encode with tiktoken gpt2 bpe
enc = tiktoken.get_encoding("gpt2")
train_ids = enc.encode_ordinary(train_data)
val_ids = enc.encode_ordinary(val_data)
print(f"train has {len(train_ids):,} tokens")
print(f"val has {len(val_ids):,} tokens")

# export to bin files
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_path = os.path.join(os.path.dirname(__file__), 'train.bin')
val_path = os.path.join(os.path.dirname(__file__), 'val.bin')
train_ids.tofile(train_path)
val_ids.tofile(val_path)

# build and save meta (stoi / itos) for the tokens present in the dataset
try:
    import pickle
    unique_ids = sorted(set(train_ids.tolist()) | set(val_ids.tolist()))
    itos = {}
    stoi = {}
    for tid in unique_ids:
        try:
            decoded = enc.decode([int(tid)])
        except Exception:
            decoded = '<|UNK|>'
        itos[int(tid)] = decoded
        stoi[decoded] = int(tid)
    meta = {'itos': itos, 'stoi': stoi, 'vocab_size': max(unique_ids) + 1}
    meta_path = os.path.join(os.path.dirname(__file__), 'meta.pkl')
    with open(meta_path, 'wb') as f:
        pickle.dump(meta, f)
    print(f'wrote train.bin, val.bin and meta.pkl (vocab_size ~ {meta["vocab_size"]})')
except Exception as e:
    print('warning: failed to write meta.pkl:', e)
