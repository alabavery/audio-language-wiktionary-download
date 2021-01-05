import requests
import sys
import os
import time
import json

_BASE_WIKTIONARY = "https://{language_abbrev}.wiktionary.org/wiki"
_LANGUAGE_ABBREVS = { "spanish": "en" }
_WORD_LIST_FILE_NAME = 'words.json'
_DOWNLOADS_DIRECTORY_NAME = 'downloads'
_ERROR_FILE = 'errors.json'


def download_pages(language, word_list_directory_path, target_directory_path):
    language_abbrev = _LANGUAGE_ABBREVS.get(language)
    if not language_abbrev:
        print("invalid langage", language)
        sys.exit()
    base_language_url = _BASE_WIKTIONARY.format(language_abbrev=language_abbrev)
    print("base_language_url: {base_language_url}".format(base_language_url=base_language_url), flush=True)
    
    word_list = _get_word_list(word_list_directory_path)
    print("Found {num} words to download, beginning with '{first}' and ending in '{last}'".format(num=len(word_list), first=word_list[0], last=word_list[-1]))

    errors = {}
    downloads_path = os.path.join(target_directory_path, _DOWNLOADS_DIRECTORY_NAME)
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)
    errors_path = os.path.join(target_directory_path, _ERROR_FILE)
    print("saving words to:", downloads_path, flush=True)
    print("saving errors to:", errors_path, flush=True)
    for i, word in enumerate(word_list):
        is_success, content = _get_page(base_language_url, word)
        if not is_success:
            errors[word] = content
        else:
            with open(os.path.join(downloads_path, "{word}.txt".format(word=word)), 'w+') as f:
                f.write(content)

        if i % 50 == 0:
            print("Completed {i} words. Last completed word: {word}".format(i=i, word=word), flush=True)
        time.sleep(0.33)

    print("{num} errors".format(num=len(errors.keys())))
    with open(errors_path, 'w+') as f:
        f.write(json.dumps(errors))


def _get_page(language_base_url, word):
    res = requests.get(language_base_url + "/{word}?action=raw".format(word=word))
    is_success = res.status_code == 200
    return is_success, res.content.decode(res.encoding) if is_success else res.reason


def _get_word_list(word_list_directory_path):
    try:
        with open(os.path.join(word_list_directory_path, _WORD_LIST_FILE_NAME), "r") as f:
            return [word.strip() for word in json.loads(f.read())]
    except FileNotFoundError:
        print("There must be a file called {fname} in the word list directory.".format(fname=_WORD_LIST_FILE_NAME))
        print("It must be a json array")
        sys.exit()