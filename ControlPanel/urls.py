from django.conf.urls import url

from ControlPanel.views import ControlPanelView

urlpatterns = [
    url(r'^$', ControlPanelView.main),
    url(r'^playFile/', ControlPanelView.playFile),
    url(r'^killPlayer/', ControlPanelView.killPlayer),
    url(r'^sendShortcut/', ControlPanelView.sendShortcut),
]
