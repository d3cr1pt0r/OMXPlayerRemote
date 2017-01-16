from django.conf.urls import url
from django.contrib import admin

from RemoteVideoPlay.views import RemoteVideoPlayView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RemoteVideoPlayView.main),
    url(r'^playFile/', RemoteVideoPlayView.playFile),
    url(r'^killPlayer/', RemoteVideoPlayView.killPlayer),
    url(r'^sendShortcut/', RemoteVideoPlayView.sendShortcut),
]
