# custom training config for cleaned twitter corpus
out_dir = 'out-custom'
eval_interval = 250
eval_iters = 200
log_interval = 10

always_save_checkpoint = False

wandb_log = False
wandb_project = 'custom-gpt'
wandb_run_name = 'custom-gpt-run'

# set dataset folder name (folder under data/)
dataset = 'custom_corpus'
gradient_accumulation_steps = 1
batch_size = 64
block_size = 256

# small model for experimentation
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.2

learning_rate = 1e-3
max_iters = 5000
lr_decay_iters = 5000
min_lr = 1e-4
beta2 = 0.99

warmup_iters = 100
