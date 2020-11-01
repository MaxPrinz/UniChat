from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),

    path('admin/', admin.site.urls),

    # for SignUp
    # see https://learndjango.com/tutorials/django-signup-tutorial
    path('accounts/', include('accounts.urls')),

    # for login/logout
    # see https://learndjango.com/tutorials/django-login-and-logout-tutorial
    path('accounts/', include('django.contrib.auth.urls')),
]
