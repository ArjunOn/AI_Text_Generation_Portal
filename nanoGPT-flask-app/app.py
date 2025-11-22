from flask import Flask, jsonify, send_from_directory, request
import subprocess
import sys
import os
import re

app = Flask(__name__, static_folder='.', static_url_path='')


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


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/generate')
def generate():
    # dataset param: 'movies' or 'twitter'
    dataset = request.args.get('dataset', 'movies')
    max_new_tokens = request.args.get('max_new_tokens', '120')
    temperature = request.args.get('temperature', None)
    # Map dataset to out dir names - adjust if your checkpoint dirs differ
    out_dirs = {
        'movies': 'out_movies',
        'movies_v2': 'out_movies_clean_v2',
        'twitter': 'out_twitter',
    }
    out_dir = out_dirs.get(dataset, 'out_movies')

    # Build command using the same Python interpreter running the Flask app
    cmd = [sys.executable, 'sample.py', f'--out_dir={out_dir}', '--device=cpu', f'--num_samples=1', f'--max_new_tokens={max_new_tokens}', '--dtype=float32']
    # add temperature if provided
    if temperature is not None:
        cmd.append(f'--temperature={temperature}')

    # Run sample.py and capture stdout
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd(), timeout=120)
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
