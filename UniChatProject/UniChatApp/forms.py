from django import forms
from .threadlocals import get_current_user
from .models import Settings, Friendlist


class SettingsForm(forms.ModelForm):

    class Meta:
         model = Settings
         fields = ('language', 'funMode', 'hideLastLogin')


class AddFriendForm(forms.Form):
    friendId = forms.IntegerField(label='Friend Id', required=False)
    friendName = forms.CharField(label='Friend Username', max_length=150, required=False)
    friendEmail = forms.EmailField(label='Friend eMail', required=False)

class CreateGroupForm(forms.Form):
    currentUser = get_current_user()
    currentUserID = currentUser.id
    chatName = forms.CharField(label='Friend Username', max_length=150, required=False)
    addedFriends = forms.ModelMultipleChoiceField(queryset=Friendlist.objects.filter(creator=currentUserID))
