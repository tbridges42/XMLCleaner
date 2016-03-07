import shutil
import os
import time
from os import walk


# get all files to be tested
def get_test_files():
    files = []
    now = time.time()
    today = now - 60*60**3
    for (dirpath, dirnames, filenames) in walk(os.path.dirname(os.path.abspath(__file__))):
        for (filename) in filenames:
            if filename.endswith('.xml') and os.path.getmtime(dirpath + os.sep + filename) > today:
                print(filename)
                files.append(dirpath + os.sep + filename)
    return files


def main():
    files = get_test_files()
    for file in files:
        os.remove(file)


if __name__ == "__main__":
    main()
