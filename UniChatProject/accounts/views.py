# accounts/views.py
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


# see https://overiq.com/django-1-10/django-creating-users-using-usercreationform/
def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': f})
