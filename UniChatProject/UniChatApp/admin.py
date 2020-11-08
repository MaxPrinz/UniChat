from django.contrib import admin
from .models import Language, Settings, Friendlist

# Register your models here.
admin.site.register(Settings)
admin.site.register(Language)
admin.site.register(Friendlist)


