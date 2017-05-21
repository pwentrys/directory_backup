import datetime
import os
import time
import zipfile
from multiprocessing import Pool, TimeoutError

from config import MAX_PROCESSES, DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

if MAX_PROCESSES > os.cpu_count():
    MAX_PROCESSES = os.cpu_count()


def changeDir(name):
    os.chdir(name)


def filesInCurrentDir():
    return os.listdir(os.getcwd())


def f(x, fn):
    with zipfile.ZipFile.open(fn, 'a', zipfile.ZIP_LZMA, True) as file:
        file.write(x)
    file.close()
    print(str(os.getpid()) + ': ' + x)
    return x


print('current pid: ' + str(os.getpid()))

if __name__ == '__main__':
    def DefinePresets():
        utcnow = datetime.datetime.utcnow()
        utcnow_formatted = datetime.datetime.strftime(utcnow, '_%Y%m%d_%H%M%S')
        file_name = FILE_NAME_PREFIX + utcnow_formatted + '.' + FILE_EXT
        return file_name


    def CheckIfValidTargetLocation():
        allowToContinue = True
        foundFile = False
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

        return allowToContinue


    def GetAllFileLocations():
        for target in TARGETS:
            changeDir(target)
            fileArray = []
            for root, dirs, files in os.walk(target):
                for f in files:
                    fileArray.append(os.path.join(root, f))
        return fileArray


    file_name = DefinePresets()

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

    if CheckIfValidTargetLocation():
        with zipfile.ZipFile(file_name, 'x', zipfile.ZIP_LZMA, True) as backup_file:
            backup_file.close()

        # start 4 worker processes
        with Pool(processes=MAX_PROCESSES) as pool:
            # launching multiple evaluations asynchronously *may* use more processes
            multiple_results = [pool.apply_async(f, (i, file_name,)) for i in GetAllFileLocations()]
            print([res.get(timeout=160) for res in multiple_results])

            # make a single worker sleep for 10 secs
            res = pool.apply_async(time.sleep, (10,))

            try:
                print(res.get(timeout=320))
            except TimeoutError:
                print("TIMEOUT")

            print("For the moment, the pool remains available for more work")

        # exiting the 'with'-block has stopped the pool
        print("Now the pool is closed and no longer available")

        # backup_file.close()
