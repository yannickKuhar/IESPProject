from threading import Thread, Lock, current_thread
from queue import Queue

l = []


def worker(q: Queue, lock):

    while True:

        val = q.get()

        print(f'in {current_thread().name} got {val}')

        for k in range(val + 1, val + 5):
            q.put(k)

        q.task_done()


if __name__ == '__main__':
    q = Queue()

    n = 10

    for i in range(1, 15):
        q.put(i)

    for i in range(n):
        t = Thread(target=worker, args=(q, Lock()))
        t.daemon = True
        t.start()

    q.join()

    print('end main')