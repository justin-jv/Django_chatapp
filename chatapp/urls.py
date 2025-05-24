from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chats/', views.chat_home, name='chat_home'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_chat, name='group_chat'),
    path('chat/<str:username>/', views.chat_view, name='chat_detail'),
]
