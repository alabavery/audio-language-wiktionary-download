import json
import os

import paths

def get_words_to_skip(target_dir):
    successfully_downloaded = [(lambda f: f.split('.')[0])(file_name) for file_name in os.listdir(paths.downloads_path(target_dir))]
    
    try:
        with open(paths.errors_path(target_dir), 'r') as f:
            errors = json.loads(f.read())
    except FileNotFoundError:
        errors = {}
    
    failed_downloads = list(errors.keys())
    return successfully_downloaded + failed_downloads