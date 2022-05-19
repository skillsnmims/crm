# chat/routing.py
from django.urls import re_path
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'ws/agent/$', consumers.AgentConsumer),
    url(r'ws/branch-admin/$', consumers.BranchAdminConsumer),
]

