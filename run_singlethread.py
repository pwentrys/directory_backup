import datetime
import os
import zipfile

from config import DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

print('\nBackup Folder: ' + DESTINATION)
print('\nTargets: ' + str(len(TARGETS)))
print('Cur Dir: ' + os.getcwd())

path_array = DESTINATION.split('\\')
path = path_array[0]
os.chdir(path)
print('Cur Dir: ' + os.getcwd())
foundFile = False
allowToContinue = True
utcnow = datetime.datetime.utcnow()
utcnow_formatted = datetime.datetime.strftime(utcnow, '_%Y%m%d_%H%M%S')
file_name = FILE_NAME_PREFIX + utcnow_formatted + '.' + FILE_EXT
print('FINAL FILE NAME: ')
print(file_name)

for path in path_array[1:]:
    for containing_file in os.listdir(os.getcwd()):
        if containing_file == path:
            foundFile = True
            print('FOUND fOLDER')
            break

    if foundFile:
        print(str(foundFile))
        os.chdir(path)
        print('Cur Dir: ' + os.getcwd())
        foundFile = False
    else:
        print('NOT FOUND FILE')
        allowToContinue = False

if allowToContinue:
    with zipfile.ZipFile(file_name, 'x', zipfile.ZIP_LZMA, True) as backup_file:
        for target in TARGETS:
            os.chdir(target)
            for root, dirs, files in os.walk(target):
                for f in files:
                    backup_file.write(os.path.join(root, f))

    backup_file.close()

else:
    print('ERROR - QUITTING RUN')
