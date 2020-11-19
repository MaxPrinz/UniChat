from django.contrib import admin
from .models import Language, Settings, Friendlist, Groupchat, ChatMessage

# Register your models here.
admin.site.register(Settings)
admin.site.register(Language)
admin.site.register(Friendlist)
admin.site.register(Groupchat)
admin.site.register(ChatMessage)