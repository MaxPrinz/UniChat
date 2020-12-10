import requests
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from sendgrid import Mail, SendGridAPIClient

from .forms import ContactForm, ContactFormNotLogin

# We created an unilichat@gmail.com account for sendgrid and recaptcha
# simple sendgrid call to send emails

# Attention: to get this working, you have to set up SENDGRIDIP in settings.py better as environment variable RECAPTCHA_PUBLIC_KEY,
# RECAPTCHA_PRIVATE_KEY, and EMAIL_HOST_PASSWORD in settings_local.py.

# Method from views displaying map and contact form
# If user is logged in, name, last name, and email will automatically be filled in. If user is not logged in all fields are empty and recaptcha will be activated. User is required to fill out all fields and the recaptcha.
def contactMap(request):

    successMail = False
    recaptchaFailed = False
    recaptch = False
    # find the settings linked with user
    # if no linked settings item exist
    if request.method == 'GET':
        # if user is logged in, fields are automatically filled in.
        if not request.user.is_authenticated:
            form = ContactFormNotLogin()
            recaptch = True
        else:
            form = ContactForm(request.user)
    else: # post function executed when the user clicks send.
        if not request.user.is_authenticated:
            recaptch = True
            form = ContactFormNotLogin(request.POST)
            #Recaptcha check for users that are not logged in
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if not result['success']:
                recaptchaFailed=True
        else:
            form =  ContactForm(request.user,request.POST)
        if form.is_valid(): #when all mandatory fields have been filled out
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message ={
                'first_Name':form.cleaned_data['firstName'],
                'name':form.cleaned_data['lastName'],
                'subject':form.cleaned_data['subject'],
                'text':form.cleaned_data['message'],
                'tel':form.cleaned_data['phone'],
                'mail':form.cleaned_data['from_email']
            } #collects information from the form to pass to email

            htmlcontend = get_template('emailTamplate.html').render(message) #formats/creates email
            message = Mail(
                from_email='unilichat@gmail.com',
                to_emails=["ninambulling@gmail.com"],

                subject=subject,

                html_content=htmlcontend)

            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            response = sg.send(message)
            successMail = True
    return render(request, 'mapContact.html', {'form': form, "recaptcha":recaptch,'successMail':successMail,'recaptchaFailed':recaptchaFailed })

