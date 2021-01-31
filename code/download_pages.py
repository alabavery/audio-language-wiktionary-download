import requests
import sys
import os
import time
import json

import cached
import paths

_BASE_WIKTIONARY = "https://en.wiktionary.org/wiki"


def download_pages(word_list, target_directory_path, cached_dir_path):
    downloads_path = paths.downloads_path(target_directory_path)
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

    cached_downloads, cached_errors = cached.get_cached(cached_dir_path)
    downloads_in_target_already, errors_in_target = cached.get_cached(
        target_directory_path
    )

    already_downloaded = [word for word in word_list if word in downloads_in_target_already]
    already_errored = [word for word in word_list if word in errors_in_target]
    to_do_nothing = already_downloaded + already_errored
    to_copy_over = [
        word for word in word_list if word in cached_downloads and word not in to_do_nothing
    ]
    to_reattempt_download = [
        word for word in word_list if word in cached_errors and word not in to_do_nothing
    ]
    to_attempt_download = [
        word for word in word_list if word not in to_do_nothing and word not in to_copy_over and word not in to_reattempt_download
    ]
    print("Will do nothing for {} words, since they are already downloaded in the target directory".format(len(already_downloaded)))
    print("Will do nothing for {} words, since they are already errored in the target directory".format(len(already_errored)))
    print("Will copy {} words from cache, since they are not in target".format(len(to_copy_over)))
    print("Will try download for {} words, since they are neither cached nor already downloaded".format(
        len(to_attempt_download)))
    print("Will RE-try download for {} words, since they are in cached errors but not in target directory errors".format(
        len(to_reattempt_download)), flush=True)


    errors_path=paths.errors_path(target_directory_path)
    new_errors = []

    for i, word in enumerate(word_list):
        if i % 200 == 0 and len(to_do_nothing) != len(word_list):
            _batch_log(word, i, new_errors)

        if word in to_do_nothing:
            pass
        elif word in to_copy_over:
            cached.copy_word(word, cached_dir_path, target_directory_path)
        else:
            time.sleep(0.33)
            is_success, content =_get_page(_BASE_WIKTIONARY, word)
            if not is_success:
                new_errors.append(word)
                # write errors to disk each time in case the process is interrupted
                with open(errors_path, 'w+') as f:
                    f.write(json.dumps(errors_in_target + new_errors))
            else:
                with open(os.path.join(downloads_path, "{word}.txt".format(word=word)), 'w+') as f:
                    f.write(content)

    print("Done! {}  errors encountered.".format(len(new_errors)))


def _get_page(language_base_url, word):
    try:
        res=requests.get(language_base_url +
                        "/{word}?action=raw".format(word=word))
        is_success=res.status_code == 200
    except Exception as e:
        is_success=False
    return (is_success, res.content.decode(res.encoding)) if is_success else (False, None)


def _batch_log(word, word_index, errors):
    print("----------------------------------------------------")
    print(
            "Completed {count} words. Next word: {word}".format(
            count=word_index, word=word
        )
    )
    print("{num} new errors so far".format(num=len(errors)))
    print("----------------------------------------------------", flush=True)
