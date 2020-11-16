from django import forms

from .models import Settings


class SettingsForm(forms.ModelForm):

    class Meta:
         model = Settings
         fields = ('language', 'funMode', 'hideLastLogin')


class AddFriendForm(forms.Form):
    friendId = forms.IntegerField(label='Friend Id', required=False)
    friendName = forms.CharField(label='Friend Username', max_length=150, required=False)
    friendEmail = forms.EmailField(label='Friend eMail', required=False)

class CreateGroupForm(forms.Form):
    chatName = forms.CharField(label='Friend Username', max_length=150, required=False)
    # Namen der Freunde des users laden und als Checkboxen darstellen.
