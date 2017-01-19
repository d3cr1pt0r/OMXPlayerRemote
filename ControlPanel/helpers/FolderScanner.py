import os
from RemoteVideoPlay import settings
from ControlPanel.helpers import DatabaseSync

def getFolderFiles(path):
    f = {}

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_path_relative = file_path.replace(path, '')
            file_name = os.path.basename(file_path)
            file_first_folder = file_path_relative.split('/')[0]
            file_ext = file_path.split('.')[-1]

            if file_ext in settings.SUPPORTED_EXT:
                if file_first_folder not in f:
                    f[file_first_folder] = []

                DatabaseSync.syncFile(file_first_folder, file_name, file_path_relative)
                f[file_first_folder].append({ 'file_path': file_path, 'file_name': file_name })

    for key in f:
        f[key] = sorted(f[key])

    return f
