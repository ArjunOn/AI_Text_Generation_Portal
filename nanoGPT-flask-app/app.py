from flask import Flask, jsonify, send_from_directory, request
import subprocess
import sys
import os
import re
import random
from pathlib import Path

app = Flask(__name__, static_folder='.', static_url_path='')

# Ensure a central logs folder exists (we store flask logs under myNanoGPT/logs)
logs_dir = Path(__file__).resolve().parents[1] / 'myNanoGPT' / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)

import logging
file_handler = logging.FileHandler(str(logs_dir / 'flask.log'))
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
logging.getLogger().addHandler(file_handler)


def extract_generated_text(raw: str) -> str:
    """Extract the generated sample(s) from sample.py stdout.
    sample.py prints generated text blocks followed by lines of dashes ("---------------").
    This function returns the concatenation of those blocks, cleaned up.
    """
    # Normalize newlines
    s = raw.replace('\r\n', '\n')
    # Remove common PyTorch warnings and configurator prints (lines that start with 'Overriding' or contain 'UserWarning')
    lines = [l for l in s.split('\n') if not (l.startswith('Overriding:') or 'UserWarning' in l or l.strip().startswith('python.exe') or l.strip().startswith('number of parameters:'))]
    s = '\n'.join(lines)
    # Split on the separator used in sample.py
    parts = [p.strip() for p in re.split(r'-{3,}', s) if p.strip()]
    if not parts:
        # fallback: return last large chunk
        chunks = [p.strip() for p in s.split('\n\n') if p.strip()]
        return chunks[-1] if chunks else s
    # Prefer parts that contain alphabetic characters
    good = [p for p in parts if re.search('[A-Za-z]', p)]
    return '\n\n'.join(good) if good else parts[-1]


def sanitize_output(text: str) -> str:
    """Post-process generated text to remove isolated noisy symbols and collapse punctuation.
    This does not change model weights but makes UI output more readable while we improve data.
    """
    # normalize newlines
    s = text.replace('\r\n', '\n')
    # remove isolated runs of symbols like @, $, %, ^, * when they appear as standalone tokens
    s = re.sub(r"\b[@$%^&*~]{1,}\b", ' ', s)
    # remove caret clusters and other repeated symbol runs
    s = re.sub(r"[\^]{2,}", ' ', s)
    # remove isolated single punctuation tokens between spaces (e.g. ' @ ' or ' $ ')
    s = re.sub(r'(?<=\s)[^\w\s](?=\s)', ' ', s)
    # collapse multiple punctuation like '!!' or '??' to a single char
    s = re.sub(r'([!?.]){2,}', r'\1', s)
    # collapse multiple spaces/newlines
    s = re.sub(r'[ \t\f\v]+', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    # trim
    return s.strip()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/checkpoints')
def list_checkpoints():
    """List all available checkpoint directories in myNanoGPT."""
    repo_root = Path(__file__).resolve().parents[1]
    mynano_dir = repo_root / 'myNanoGPT'
    checkpoints = sorted([p.name for p in mynano_dir.glob('out_*') if p.is_dir() and (p / 'ckpt.pt').exists()])
    return jsonify({'checkpoints': checkpoints})


@app.route('/generate')
def generate():
    # Accept either 'dataset' (legacy) or 'checkpoint' (new)
    dataset = request.args.get('dataset', None)
    checkpoint = request.args.get('checkpoint', None)
    max_new_tokens = request.args.get('max_new_tokens', '120')
    temperature = request.args.get('temperature', None)
    
    # Determine which out_dir to use
    if checkpoint:
        out_dir = checkpoint
    elif dataset:
        # Legacy dataset mapping
        out_dirs = {
            'movies': 'out_movies',
            'movies_v2': 'out_movies_clean_v2',
            'twitter': 'out_twitter',
        }
        out_dir = out_dirs.get(dataset, 'out_movies')
    else:
        out_dir = 'out_movies'

    # Run sample.py from the myNanoGPT folder (we keep the model and scripts there)
    repo_root = Path(__file__).resolve().parents[1]
    mynano_dir = repo_root / 'myNanoGPT'
    sample_script = mynano_dir / 'sample.py'
    if not sample_script.exists():
        return jsonify({'output': '', 'error': f'sample.py not found at {sample_script}'}), 500

    # Build command using the same Python interpreter running the Flask app
    cmd = [sys.executable, str(sample_script), f'--out_dir={out_dir}', '--device=cpu', f'--num_samples=1', f'--max_new_tokens={max_new_tokens}', '--dtype=float32']
    # add temperature if provided
    if temperature is not None:
        cmd.append(f'--temperature={temperature}')
    # use a random seed each time so we get different outputs on multiple calls
    random_seed = random.randint(0, 2**31 - 1)
    cmd.append(f'--seed={random_seed}')

    # Ensure the requested out_dir exists and has a checkpoint
    out_dir_path = mynano_dir / out_dir
    if not out_dir_path.exists() or not out_dir_path.is_dir():
        available = sorted([p.name for p in mynano_dir.glob('out_*') if p.is_dir()])
        return jsonify({'output': '', 'error': f'Checkpoint directory "{out_dir}" not found. Available checkpoints: {available}'}), 400
    ckpt_file = out_dir_path / 'ckpt.pt'
    if not ckpt_file.exists():
        return jsonify({'output': '', 'error': f'No checkpoint (ckpt.pt) found in {out_dir_path}. Available files: {list(out_dir_path.iterdir())}'}), 400

    # Run sample.py and capture stdout; set cwd to myNanoGPT so relative imports/files resolve
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(mynano_dir), timeout=300)
        stdout = proc.stdout
        stderr = proc.stderr
        if proc.returncode != 0:
            # return error details (sanitized)
            return jsonify({'output': '', 'error': f'sample.py exited with code {proc.returncode}', 'stderr': stderr}), 500
        text = extract_generated_text(stdout)
        return jsonify({'output': text})
    except subprocess.TimeoutExpired:
        return jsonify({'output': '', 'error': 'sample.py timed out'}), 500
    except Exception as e:
        return jsonify({'output': '', 'error': str(e)}), 500


if __name__ == '__main__':
    # Run on all interfaces by default for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
