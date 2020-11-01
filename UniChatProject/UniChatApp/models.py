from django.contrib.auth.models import User
from django.db import models


# Available languages for Translation
# Fill it with admin
class Language(models.Model):
    iso = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=10)

    # for admin: return back a useful name
    def __str__(self):
        return self.name + ' (' + self.iso + ')'


# because we use the built-in django user object,
# we have to create a one-to-one-connection to a settings-table, that stores special settings value,
# that are not included in the built-in user object or are uniCh@t specific
class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    funMode = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)

    # for admin: return back the name of the linked user
    def __str__(self):
        return self.user.__str__()



