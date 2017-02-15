import json, os

from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from ControlPanel.helpers import OMXPlayer
from ControlPanel.helpers import DatabaseSync
from RemoteVideoPlay import settings

def main(request):
    OMXPlayer.checkForPipe(settings.PIPE_PATH)

    DatabaseSync.scanFolder(settings.TORRENT_DIR, settings.SUPPORTED_EXT)
    directories = DatabaseSync.getFiles()

    template = loader.get_template('main.html')
    context = RequestContext(request, {
        'directories': directories,
    })

    print os.system('echo'+'"$USER"')

    return HttpResponse(template.render(context))

@csrf_exempt
def playFile(request):
    if 'file_path' not in request.POST:
        return JsonResponse({'success': False, 'message': '"file_path" missing in POST data'})

    file_path = request.POST.get('file_path', '')
    full_path = settings.TORRENT_DIR + file_path

    if not OMXPlayer.playFile(full_path, settings.OMX_PATH, settings.PIPE_PATH):
        return JsonResponse({'success': False, 'message': 'OMXPlayer failed to play file: ' + file_path})

    DatabaseSync.setFileWatched(file_path, watched=True)

    return JsonResponse({'success': True, 'message': 'Request sent to OS'})

@csrf_exempt
def killPlayer(request):
    OMXPlayer.killPlayer()
    return JsonResponse({'success': True, 'message': 'Request sent to OS'})

@csrf_exempt
def sendShortcut(request):
    if 'key' not in request.POST:
        return JsonResponse({'success': False, 'message': '"key" missing in POST data'})

    key = request.POST.get('key', '')

    if not OMXPlayer.sendKey(key, settings.PIPE_PATH):
        return JsonResponse({'success': False, 'message': 'OMXPlayer failed to send key: ' + key})

    return JsonResponse({'success': True, 'message': 'Request sent to OS'})
