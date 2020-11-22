from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),

    # different chat-views
    path('userchat/<int:friend_id>', views.friendchat, name='friendchat'),
    path('groupchat/<int:group_id>', views.groupchat, name='groupchat'),

    # add a new friend
    path('addfriend', views.addfriend, name='addfriend'),

    # create a new group
    path('creategroup', views.creategroup, name='creategroup'),

    # for accessing admin-functionality
    path('admin/', admin.site.urls),

    # for SignUp
    # see https://learndjango.com/tutorials/django-signup-tutorial
    path('accounts/', include('accounts.urls')),

    # for login/logout
    # see https://learndjango.com/tutorials/django-login-and-logout-tutorial
    path('accounts/', include('django.contrib.auth.urls')),

    #test
    path('test', views.test)
]
