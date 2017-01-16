import json

from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from RemoteVideoPlay.helpers import FolderScanner
from RemoteVideoPlay.helpers import OMXPlayer
from RemoteVideoPlay import settings

def main(request):
    OMXPlayer.checkForPipe(settings.PIPE_PATH)

    folder_files = FolderScanner.getFolderFiles(settings.TORRENT_DIR)

    template = loader.get_template('main.html')
    context = RequestContext(request, {
        'folder_files': folder_files,
    })

    return HttpResponse(template.render(context))

@csrf_exempt
def playFile(request):
    if 'file_path' not in request.POST:
        return JsonResponse({'success': False, 'message': '"file_path" missing in POST data'})

    file_path = request.POST.get('file_path', '')

    if not OMXPlayer.playFile(file_path, settings.OMX_PATH, settings.PIPE_PATH):
        return JsonResponse({'success': False, 'message': 'OMXPlayer failed to play file: ' + file_path})

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
