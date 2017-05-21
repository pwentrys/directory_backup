import time
from multiprocessing import Pool, TimeoutError

import utils
from config import MAX_PROCESSES, DESTINATION, TARGETS, FILE_EXT, FILE_NAME_PREFIX

if MAX_PROCESSES > utils.cpu_count():
    MAX_PROCESSES = utils.cpu_count()

print('current pid: ' + str(utils.getpid()))

if __name__ == '__main__':
    def validate_target_loc():
        """
        Ensure everything exists.
        :return:
        """
        is_allow_continue = True
        is_file_found = False
        for path_item in path_array[1:]:
            for containing_file in utils.listdir_cwd():
                if containing_file == path_item:
                    is_file_found = True
                    break

            if is_file_found:
                utils.chdir(path_item)
                is_file_found = False
            else:
                print(f'NOT FOUND FILE: {path_item}')
                is_allow_continue = False

        return is_allow_continue


    file_locs = utils.get_all_file_locs(TARGETS)
    file_name = utils.create_filename(FILE_NAME_PREFIX, FILE_EXT)

    path_array = DESTINATION.split('\\')
    path_root = path_array[0]
    utils.chdir(path_root)

    utils.log_folders_destination_targets(DESTINATION, TARGETS, file_name)

    if validate_target_loc():
        with utils.zipfile.ZipFile(file_name, 'x', utils.zipfile.ZIP_LZMA, True) as backup_file:
            backup_file.close()

        # Starting pool with x workers.
        with Pool(processes=MAX_PROCESSES) as pool:
            # Launching multiple evaluations asynchronously *may* use more processes
            multiple_results = [pool.apply_async(utils.f, (i, file_name,)) for i in file_locs]
            print([res.get(timeout=160) for res in multiple_results])

            # Make a single worker sleep for 10 secs
            res = pool.apply_async(time.sleep, (10,))

            try:
                print(res.get(timeout=320))
            except TimeoutError:
                print('TIMEOUT')
