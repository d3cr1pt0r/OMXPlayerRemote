from django.conf.urls import url, include
from django.contrib import admin

from ControlPanel import urls as ControlPanelUrls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^control-panel/', include(ControlPanelUrls)),
]
