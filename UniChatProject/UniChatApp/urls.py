from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settingsView, name='settings'),

    # different chat-views
    path('userchat/<int:friend_id>', views.friendchat, name='friendchat'),
    path('groupchat/<int:group_id>', views.groupchat, name='groupchat'),

    # chat-content for ajax-load friendchat
    path('ajax/getUserchatMessages/<int:friend_id>', views.ajaxfriendchat, name='ajaxfriendchat'),

    # chat-content for ajax-load groupchat
    path('ajax/getGroupchatMessages/<int:group_id>', views.ajaxgroupchat, name='ajaxgroupchat'),

    # chat-content for ajax-load globalchat
    path('ajax/getGlobalMessages', views.ajaxglobalchat, name='ajaxglobalchat'),

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

    # to display user-image
    # see https://djangocentral.com/uploading-images-with-django/
    path('media/profile/<int:user_id>', views.showProfilePicture, name='profilePicture'),

    #test
    path('test', views.test)
]
