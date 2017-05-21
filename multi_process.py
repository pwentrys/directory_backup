import multiprocessing
import os


# TODO This is pretty functionless for now.
def __log__(title):
    """
    Debug log.
    :param title: Debug title
    :return:
    """
    print(f'{title}\nModule: {__name__}\nParent Process ID: {os.getppid()}\nProcess ID: {os.getpid()}')


def f(name):
    """
    Multiprocess item.
    :param name: Name of process
    :return:
    """
    __log__('Function F')
    print('Hello', name)


if __name__ == '__main__':
    __log__('main line')
    p = multiprocessing.Process(target=f, args=('bob',))
    p.start()
    p.join()
