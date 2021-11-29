import os
import time
import json
from pathlib import Path

root_dir = '/'
index = {}

t0 = time.time()

def create_index():
    paths = Path('/').glob('**/*')
    for path in paths:
        try:
            # because path is object not string
            path_in_str = str(path)
            # Do thing with the path
            print(path_in_str)
            if os.path.isdir(path) and not os.path.islink(path):
                        pass
            else:
                #os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                path_in_str = str(path)
                if os.path.basename(path_in_str) in index:
                    index[os.path.basename(path_in_str)].append(path_in_str)
                else:
                    index[os.path.basename(path_in_str)] = [path_in_str]
        except PermissionError:
            print('Permission on dir denied access.')
        except FileNotFoundError:
            print('File Not Found, Moving On.')



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

