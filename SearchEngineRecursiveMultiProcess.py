import os
import json
from pathlib import Path
import multiprocessing
from multiprocessing import Pool
from multiprocessing.pool import Pool as p
import time
import psutil

root_dir = '/'
index = {}
num_cores = multiprocessing.cpu_count()
t0 = time.time()


def worker(main_process_id, path):
    if os.path.isdir(path) and not os.path.islink(path):
        create_index(main_process_id, path)
    else:
        path_in_str = str(path)
        if os.path.basename(path_in_str) in index:
            index[os.path.basename(path_in_str)].append(path_in_str)
        else:
            index[os.path.basename(path_in_str)] = [path_in_str]


def create_index(main_process_id, root):
    
    try:
        main_process = psutil.Process(main_process_id)
        children = main_process.children(recursive=True)
        active_processes = len(children) + 1 #plus parent
        base_dir = os.listdir(root)
        new_processes = len(base_dir) #length of classes processes will be created
     
        #parallel
        if num_cores > active_processes + new_processes:
            pool = MyPool(num_cores)
            for item in base_dir:
                path = os.path.join(root, item)
                print(path)
                pool.apply_async(worker, (path, main_process_id))
            pool.close()
            pool.join()
        else: #serial
            for item in base_dir:
                path = os.path.join(root, item)
                worker(main_process_id, path)

        
    except PermissionError:
        print('Permission on dir denied access')


class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.


class MyPool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(MyPool, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    process_id = os.getpid()
    try:
        create_index(process_id, root_dir)
        with open('index.json', 'w') as fp:
            json.dump(index, fp)
        t1 = time.time()
        print("TIME ElAPSED", t1-t0)
    except KeyboardInterrupt:
        with open('index.json', 'w') as fp:
            json.dump(index, fp)
        t1 = time.time()
        print("TIME ElAPSED", t1-t0)

