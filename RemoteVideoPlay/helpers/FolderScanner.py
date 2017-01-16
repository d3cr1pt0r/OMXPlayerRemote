import os
from RemoteVideoPlay import settings

def fillTreeDict(tree, file_path_array):
    if len(file_path_array) > 1:
        if len(file_path_array) == 2:
            if file_path_array[0] not in tree:
                tree[file_path_array[0]] = []
            tree[file_path_array[0]].append(file_path_array[1])
        else:
            if file_path_array[0] not in tree:
                tree[file_path_array[0]] = {}
            fillTreeDict(tree[file_path_array[0]], file_path_array[1:])

def getFolderTree(path):
    tree = {}

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_path_array = filter(None, file_path.split('/'))
            fillTreeDict(tree, file_path_array)

    return tree

def getFolderFiles(path):
    f = {}

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_name = os.path.basename(file_path)
            file_first_folder = file_path.replace(path, '').split('/')[0]
            file_ext = file_path.split('.')[-1]

            if file_ext in settings.SUPPORTED_EXT:
                if file_first_folder not in f:
                    f[file_first_folder] = []
                f[file_first_folder].append({ 'file_path': file_path, 'file_name': file_name })

    for key in f:
        f[key] = sorted(f[key])

    return f
