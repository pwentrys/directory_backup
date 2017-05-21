import os
import threading

TOTAL = 0
THREAD_LOCK = threading.Lock()
print(f'CPUs: {os.cpu_count()}')


class CountThread(threading.Thread):
    def run(self):
        print(f'Active Threads: {threading.active_count()}')
        global TOTAL
        for i in range(100000):
            THREAD_LOCK.acquire()
            TOTAL = TOTAL + 1
            THREAD_LOCK.release()
        print(f'{TOTAL}\n')


a = CountThread()
b = CountThread()
a.start()
b.start()
