import os
import multiprocessing
from multiprocessing import Pool
from multiprocessing.pool import Pool as p
import time

index = {}
num_cores = multiprocessing.cpu_count()
t0 = time.time()

if __name__ == '__main__':
    pool = Pool()
    # for i in range(10000):
    #     pool.map(print, 'Hello World')

    for i in range(100000):
        pool.apply_async(print, ('Hello World',))
        
    t1 = time.time()
    print(t1-t0)