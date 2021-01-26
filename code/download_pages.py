import requests
import sys
import os
import time
import json

import cached
import paths

_BASE_WIKTIONARY = "https://en.wiktionary.org/wiki"


def download_pages(word_list, target_directory_path, cached_dir_path):
    errors = {}
    downloads_path = paths.downloads_path(target_directory_path)
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

    words_to_copy = cached.get_words_to_copy(cached_dir_path)
    print(words_to_copy)

    errors_path = paths.errors_path(target_directory_path)
    print("saving words to:", downloads_path, flush=True)
    print("saving errors to:", errors_path, flush=True)

    for i, word in enumerate(word_list):
        if word in words_to_copy:
            cached.copy_word(word, cached_dir_path, target_directory_path)
            continue

        is_success, content = _get_page(_BASE_WIKTIONARY, word)
        if not is_success:
            errors[word] = content
            # write errors to disk each time in case the process is interrupted and main memory is lost
            with open(errors_path, 'w+') as f:
                f.write(json.dumps(errors))
        else:
            with open(os.path.join(downloads_path, "{word}.txt".format(word=word)), 'w+') as f:
                f.write(content)

        if i % 50 == 0:
            _batch_log(word, i, errors)

        time.sleep(0.33)

    print("Done! {num} errors total".format(num=len(errors.keys())))


def _get_page(language_base_url, word):
    res = requests.get(language_base_url +
                       "/{word}?action=raw".format(word=word))
    is_success = res.status_code == 200
    return is_success, res.content.decode(res.encoding) if is_success else res.reason


def _batch_log(word, word_index, errors):
    print("----------------------------------------------------")
    print("Completed {count} words. Last completed word: {word}".format(
        count=word_index+1, word=word))
    print("{num} errors so far".format(
        num=len(errors.keys()), flush=True))
    print("----------------------------------------------------")
