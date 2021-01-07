import sys
from download_pages import download_pages


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Must pass word list path and target path arguments.  Passed arguments:", str(sys.argv[1:]))
        sys.exit()

    print("Beginning work", flush=True)
    download_pages(sys.argv[1], sys.argv[2])
    print("Work done")
