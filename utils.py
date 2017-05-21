import datetime
import zipfile
from os import chdir, getpid, getcwd, listdir, walk, path


def listdir_cwd():
    """
    Lazy listdir for cwd.
    :return:
    """
    return listdir(getcwd())


def f(x, fn):
    """
    Le Zip
    :param x:
    :param fn:
    :return:
    """
    with zipfile.ZipFile.open(fn, 'a', zipfile.ZIP_LZMA, True) as file:
        file.write(x)
    file.close()
    print(f'{getpid()}: {x}')
    return x


def utc_now_to_file_str():
    """
    Format UTC now to _YYYYmmdd_HHMMSS
    :return:
    """
    return datetime.datetime.strftime(datetime.datetime.utcnow(), '_%Y%m%d_%H%M%S')


def create_filename(prefix, extension):
    """
    Create filename to be used.
    :param prefix:
    :param extension:
    :return:
    """
    return f'{prefix}{utc_now_to_file_str()}.{extension}'


def log_folders_destination_targets(dest, targets, filename):
    """
    Log Folders, destination, and targets.
    :param dest:
    :param targets:
    :param filename:
    :return:
    """
    print(f'\n Destination Folder: {dest}'
          f'\n Targets: {str(len(targets))}'
          f'\n File: {filename}')


def get_all_file_locs(targets):
    """
    Gets all file locations.
    :return:
    """
    file_list = []
    for target in targets:
        chdir(target)
        for root, dirs, files in walk(target):
            for file in files:
                file_list.append(path.join(root, file))
    return file_list
