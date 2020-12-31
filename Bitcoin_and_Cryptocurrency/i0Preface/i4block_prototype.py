import string
import random
from pathlib import Path

# https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python



def create_pointer(prenode_mtime, prenode_filename):
    # print('#', prenode_mtime, type(prenode_mtime), type(prenode_filename))
    if prenode_mtime is None:
        prenode_mtime = '@@'
    if prenode_filename is None:
        prenode_filename = '@@@'
    return str(prenode_mtime) + '#sig#' + str(prenode_filename)

def main():
    file_list = list(Path('i4test_files').glob('*.*'))

    #     st_mtime
    # Time of most recent content modification expressed in seconds
    for idx, fname in enumerate(file_list):
        if idx > 0:
            # print(fname, '#', fname.stat().st_mtime)
            sig = create_pointer(file_list[idx-1].stat().st_mtime, file_list[idx-1])
        else:
            sig = create_pointer(None, None)
        print(sig)

if __name__ == "__main__":
    main()