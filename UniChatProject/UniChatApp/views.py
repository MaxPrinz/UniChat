from django.shortcuts import render, redirect


# Create your views here.
from .forms import SettingsForm
from .models import Settings


def index(request):
    return render(request, "index.html")


def settings(request):
    # make sure the current user is authenticated. If not go to login-screen
    if not request.user.is_authenticated:
        return redirect("login")

    # find the settings linked with user
    # if no linked settings item exist, create an empty one
    user = request.user
    try:
        settings = Settings.objects.get(pk=user)
    except Settings.DoesNotExist:
        settings = Settings.objects.create(user=user)

    # normal settings-form-prcessing
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.save()
            return redirect('index')
    else:
        form = SettingsForm(instance=settings)

    return render(request, 'settings.html', {'form': form})
