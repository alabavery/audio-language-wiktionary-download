import os


def downloads_path(target_directory):
    return os.path.join(target_directory, 'downloads')


def errors_path(target_directory):
    return os.path.join(target_directory, 'errors.json')
