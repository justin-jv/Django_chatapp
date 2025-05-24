# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]

# chatproject/routing.py
from django.urls import re_path
from chatapp.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
]
