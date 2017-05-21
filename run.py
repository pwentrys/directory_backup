import os
import zipfile

import utils
from config import DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

foundFile = False
allowToContinue = True
file_name = utils.create_filename(FILE_NAME_PREFIX, FILE_EXT)

path_array = DESTINATION.split('\\')
path = path_array[0]
utils.chdir(path)
line_break = '\\'

utils.log_folders_destination_targets(DESTINATION, TARGETS, file_name)

if __name__ == '__main__':
    for path in path_array[1:]:
        file_list = utils.get_all_file_locs(TARGETS)
        for containing_file in file_list:
            if containing_file == path:
                foundFile = True
                break

        if foundFile:
            utils.chdir(path)
            foundFile = False
        else:
            print(f'NOT FOUND FILE: {path}')
            allowToContinue = False

    if allowToContinue:
        with zipfile.ZipFile(file_name, 'x', zipfile.ZIP_LZMA, True) as backup_file:
            for target in TARGETS:
                utils.chdir(target)
                fileArray = []
                for root, dirs, files in os.walk(target):
                    for f in files:
                        backup_file.write(os.path.join(root, f))
            backup_file.close()
    else:
        print('ERROR - QUITTING RUN')
