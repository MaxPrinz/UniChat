from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings

from .models import Groupchat, Settings


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

class ContactForm(forms.Form):
        from_email = forms.EmailField()
        firstName = forms.CharField()
        lastName = forms.CharField()
        phone = forms.CharField()
        subject = forms.CharField(required=True, max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'forms-control'}))
        message = forms.CharField(widget=forms.Textarea(attrs={'class': 'forms-control'}), required=True, )

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['firstName'] = forms.CharField(max_length=50, initial=user.first_name)
            self.fields['lastName'] = forms.CharField(max_length=50, initial=user.last_name)
            self.fields['from_email'] = forms.EmailField(required=True, initial=user.email)

class ContactFormNotLogin(forms.Form):
    from_email = forms.EmailField(required=True,
                                  widget=forms.EmailInput(attrs={'class': 'forms-control'}))
    firstName = forms.CharField(max_length=50, initial="Max",
                                widget=forms.TextInput(attrs={'class': 'forms-control'}))
    lastName = forms.CharField(max_length=50, initial="Mustermann",
                               widget=forms.TextInput(attrs={'class': 'forms-control'}))
    subject = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'forms-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'forms-control'}), required=True, )
    phone = forms.CharField()
    captcha = ReCaptchaField(public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY, widget=ReCaptchaV2Checkbox)
