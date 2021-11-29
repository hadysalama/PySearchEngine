import os
import time
import json
from pathlib import Path
import multiprocessing
from multiprocessing import Pool

root_dir = '/'
index = {}
num_cores = multiprocessing.cpu_count()
t0 = time.time()


def worker(path):
    # because path is object not string
    path_in_str = str(path)
    # Do thing with the path
    print(path_in_str)
    if os.path.isfile(path):
        if os.path.basename(path_in_str) in index:
            index[os.path.basename(path_in_str)].append(path_in_str)
        else:
            index[os.path.basename(path_in_str)] = [path_in_str]


def create_index():
    try:
        paths = Path('/').glob('**/*')
        pool = Pool()

        def paths_gen():
            try:
                return paths
            except FileNotFoundError:
                print('File Not Found, Moving On.')
                return 0

        for path in paths_gen():
            pool.apply_async(worker, (path,))

    except PermissionError:
        print('Permission on dir denied access.')


if __name__ == '__main__':
    try:
        create_index()
        with open('index.json', 'w') as fp:
            json.dump(index, fp)
        t1 = time.time()
        print("TIME ElAPSED", t1-t0)
    except KeyboardInterrupt:
        with open('index.json', 'w') as fp:
            json.dump(index, fp)
        t1 = time.time()
        print("TIME ElAPSED", t1-t0)
