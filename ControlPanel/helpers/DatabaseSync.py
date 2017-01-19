import os
from ControlPanel.models.Directory import Directory
from ControlPanel.models.File import File

def scanFolder(path, supported_extensions):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_path_relative = file_path.replace(path, '')
            file_name = os.path.basename(file_path)
            file_first_folder = file_path_relative.split('/')[0]
            file_ext = file_path.split('.')[-1]

            if file_ext in supported_extensions:
                syncFile(file_first_folder, file_name, file_path_relative)

def syncFile(directory_name, file_name, file_path):
    directory_model, directory_created = Directory.objects.get_or_create(name=directory_name)
    file_model, file_created = File.objects.get_or_create(directory=directory_model, path=file_path, name=file_name)

def setFileWatched(file_path, watched=True):
    try:
        file_model = File.objects.get(path=file_path)
        file_model.watched = watched
        file_model.save()

        if watched:
            directory_model = file_model.directory
            directory_model.last_watched_file = file_model
            directory_model.save()
    except File.DoesNotExist:
        print 'DatabaseSync->setFileWatched: not found (', file_path, ')'

def getFiles():
    return Directory.objects.all()
