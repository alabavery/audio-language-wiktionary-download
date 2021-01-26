import json
import os
import shutil

import paths

def get_words_to_copy(cached_dir):
    successfully_downloaded = [(lambda f: f.split('.')[0])(file_name) for file_name in os.listdir(paths.downloads_path(cached_dir))]
    return successfully_downloaded
    # try:
    #     with open(paths.errors_path(target_dir), 'r') as f:
    #         errors = json.loads(f.read())
    # except FileNotFoundError:
    #     errors = {}
    
    # failed_downloads = list(errors.keys())
    # return successfully_downloaded + failed_downloads

def copy_word(word, cached_dir, target_dir):
    sub_path = os.path.join(paths.downloads_path(""), "{}.txt".format(word))
    source_path = os.path.join(cached_dir, sub_path)
    target_path = os.path.join(target_dir, sub_path)
    if source_path == target_path:
        return
    print("Copying {} from cached".format(word))
    shutil.copyfile(os.path.join(cached_dir, sub_path), os.path.join(target_dir, sub_path))
