from django import forms
from .models import Settings, Friendlist, Groupchat


class SettingsForm(forms.ModelForm):

    class Meta:
         model = Settings
         fields = ('image', 'language', 'funMode', 'hideLastLogin')


class AddFriendForm(forms.Form):
    friendId = forms.IntegerField(label='Friend Id', required=False)
    friendName = forms.CharField(label='Friend Username', max_length=150, required=False)
    friendEmail = forms.EmailField(label='Friend eMail', required=False)

class CreateGroupForm(forms.ModelForm):
    class Meta:
         model = Groupchat
         fields = ('title', 'member')
