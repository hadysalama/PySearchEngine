import os
import time
import json

root_dir = '/'
index = {}

t0 = time.time()


def create_index(root_dir):
    try:

        base_dir = os.listdir(root_dir)

        for i in range(len(base_dir)):
            path = os.path.join(root_dir, base_dir[i])
            print(path)
            if os.path.isdir(path) and not os.path.islink(path):
                create_index(path)
            else:
                #os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                path_in_str = str(path)
                if os.path.basename(path_in_str) in index:
                    index[os.path.basename(path_in_str)].append(path_in_str)
                else:
                    index[os.path.basename(path_in_str)] = [path_in_str]
    
    except PermissionError:
        print('Permission on dir denied access')


def search_index():
    with open('index.json') as fp:
        index = json.load(fp)
    while True:
        file_name = input()
        if file_name in index:
            file_locations = index[file_name]
            for file in file_locations:
                print("FILE: " + file_name + "\t LOCATION" + file)
        else:
            print('No Results')

# try:
#     create_index(root_dir)
#     with open('index.json', 'w') as fp:
#         json.dump(index, fp)
#     t1 = time.time()
#     print("TIME ElAPSED", t1-t0)
# except KeyboardInterrupt:
#     with open('index.json', 'w') as fp:
#         json.dump(index, fp)
#     t1 = time.time()
#     print("TIME ElAPSED", t1-t0)

search_index()

