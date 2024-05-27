#!/usr/bin/env python3
from flask import Flask, send_from_directory, abort
from pathlib import Path

# Conditional import based on the running context (module or script)
try:
    from paios.backend.blueprint import create_and_register_backend
except ImportError:
    from backend.blueprint import create_and_register_backend

app = Flask(__name__)

frontend_dir = Path(__file__).resolve().parent / 'frontend' / 'dist'

@app.route('/')
def serve_index():
    return send_from_directory(frontend_dir, 'index.html')

# Register the backend blueprint at /api
create_and_register_backend(app, '/api/v1')

@app.route('/<path:subpath>')
def serve_frontend(subpath):
    # Resolve the full path and ensure it is within the frontend_dir
    try:
        full_path = (frontend_dir / subpath).resolve()
        if not full_path.is_relative_to(frontend_dir):
            raise ValueError("Attempted path traversal attack")
    except Exception:
        abort(404)

    if full_path.exists() and full_path.is_file():
        return send_from_directory(frontend_dir, subpath)
    else:
        return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=3080, debug=True)
