import datetime
import os
import zipfile

from config import DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

foundFile = False
allowToContinue = True
utcnow = datetime.datetime.utcnow()
utcnow_formatted = datetime.datetime.strftime(utcnow, '_%Y%m%d_%H%M%S')
file_name = FILE_NAME_PREFIX + utcnow_formatted + '.' + FILE_EXT


def changeDir(name):
    os.chdir(name)


def filesInCurrentDir():
    return os.listdir(os.getcwd())


path_array = DESTINATION.split('\\')
path = path_array[0]
changeDir(path)
line_break = '\\'
_012 = '{0}{1}: {2}'

print(_012
      .format(line_break, 'Backup Folder', DESTINATION))
print(_012
      .format(line_break, 'Targets', str(len(TARGETS))))
print(_012
      .format(line_break, 'Archive Name', file_name))

if __name__ == '__main__':
    for path in path_array[1:]:
        for containing_file in filesInCurrentDir():
            if containing_file == path:
                foundFile = True
                break

        if foundFile:
            changeDir(path)
            foundFile = False
        else:
            print('NOT FOUND FILE: ' + path)
            allowToContinue = False

    if allowToContinue:
        with zipfile.ZipFile(file_name, 'x', zipfile.ZIP_LZMA, True) as backup_file:
            for target in TARGETS:
                changeDir(target)
                fileArray = []
                for root, dirs, files in os.walk(target):
                    for f in files:
                        backup_file.write(os.path.join(root, f))

    else:
        print('ERROR - QUITTING RUN')
    backup_file.close()
