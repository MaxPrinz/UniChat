from django.contrib.auth.models import User
from django.db import models
from .functionsImage import profilePicture_path, OverwriteStorage


# Available languages for Translation
# fill it with admin-function
class Language(models.Model):
    iso = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=10)

    # for admin: return back a useful name
    def __str__(self):
        return str(self.name) + ' (' + self.iso + ')'



# because we use the built-in django user object,
# we have to create a one-to-one-connection to a settings-table, that stores special settings value,
# that are not included in the built-in user object or are uniCh@t specific
class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    funMode = models.BooleanField(default=False)
    hideLastLogin = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=profilePicture_path, storage=OverwriteStorage())

    # for admin: return back the name of the linked user
    def __str__(self):
        return str(self.user)


# List of friends from creator-user
class Friendlist(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    # for admin: return back a useful name
    def __str__(self):
        return str(self.creator) + ' with Friend ' + str(self.friend)

# Groupchat created by one user
class Groupchat(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    member = models.ManyToManyField(User, related_name='+')

    # for admin: return back a useful name
    def __str__(self):
        return str(self.creator) + ": " + str(self.title)

# Individual chat message
class ChatMessage(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    linkedFriendList = models.ForeignKey(Friendlist, on_delete=models.CASCADE, blank=True, null=True)
    linkedGroupchat = models.ForeignKey(Groupchat, on_delete=models.CASCADE, blank=True, null=True)
    createdAt = models.DateTimeField()
    message = models.CharField(max_length=1000)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    # TODO: Add useful name for admin  <-- what is meant by that?


