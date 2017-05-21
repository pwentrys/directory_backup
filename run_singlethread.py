import os
import zipfile

import utils
from config import DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

utils.log_folders_destination_targets(DESTINATION, TARGETS, os.getcwd())

path_array = DESTINATION.split('\\')
path = path_array[0]
os.chdir(path)
print(f'CUR DIR: {os.getcwd()}')
is_file_found = False
is_allow_continue = True
file_name = utils.create_filename(FILE_NAME_PREFIX, FILE_EXT)
print(f'FINAL FILE NAME: {file_name}')

for path in path_array[1:]:
    for containing_file in os.listdir(os.getcwd()):
        if containing_file == path:
            is_file_found = True
            break

    if is_file_found:
        os.chdir(path)
        is_file_found = False
    else:
        is_allow_continue = False

if is_allow_continue:
    with zipfile.ZipFile(file_name, 'x', zipfile.ZIP_LZMA, True) as backup_file:
        for target in TARGETS:
            os.chdir(target)
            for root, dirs, files in os.walk(target):
                for f in files:
                    backup_file.write(os.path.join(root, f))
        backup_file.close()

else:
    print('ERROR - QUITTING RUN')
