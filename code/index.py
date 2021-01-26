import sys
import os
import json

from download_pages import download_pages


def _get_word_list(word_list_directory_path):
    WORD_LIST_FILE_NAME = 'words.json'
    try:
        with open(os.path.join(word_list_directory_path, WORD_LIST_FILE_NAME), "r") as f:
            return [word.strip() for word in json.loads(f.read())]
    except FileNotFoundError:
        print("There must be a file called {fname} in the word list directory.".format(
            fname=WORD_LIST_FILE_NAME
        ))
        print("It must be a json array")
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Must pass word list path and target path arguments.  Passed arguments:", str(
            sys.argv[1:]))
        sys.exit()

    word_list_dir, target_dir = sys.argv[1:3]

    word_list = _get_word_list(word_list_dir)
    print("Found {num} words to download, beginning with '{first}' and ending in '{last}'".format(
        num=len(word_list), first=word_list[0], last=word_list[-1]))
    print("Beginning work", flush=True)
    download_pages(word_list, target_dir)
    print("Work done")
