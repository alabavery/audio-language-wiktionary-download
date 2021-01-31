import json
import os
import shutil

import paths


def get_cached(cached_dir):
    successfully_downloaded = [(lambda f: f.split('.')[0])(file_name) for file_name in os.listdir(paths.downloads_path(cached_dir))]
    try:
        with open(paths.errors_path(cached_dir), 'r') as f:
            errors = json.loads(f.read())
    except FileNotFoundError:
        errors = []
    
    return successfully_downloaded, errors


def copy_word(word, cached_dir, target_dir):
    sub_path = os.path.join(paths.downloads_path(""), "{}.txt".format(word))
    source_path = os.path.join(cached_dir, sub_path)
    target_path = os.path.join(target_dir, sub_path)
    shutil.copyfile(source_path, target_path)
