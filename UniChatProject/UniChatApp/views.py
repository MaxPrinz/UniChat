from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from .forms import SettingsForm, AddFriendForm, CreateGroupForm
from .functionsUser import getFriendOfUser, getUserOrNone
from .models import Settings, Friendlist


def index(request):
    return showChat(request)

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





def friendchat(request, friend_id):
    return showChat(request, friendChatId=friend_id)

def groupchat(request, group_id):
    return showChat(request, groupChatId=group_id)


def showChat(request, friendChatId = None, groupChatId = None):
    if not request.user.is_authenticated:
        return redirect("login")

    # set some variables
    chatname = "Global"
    chatId = -1
    chattype = "global"
    friend = None

    # load - if friendChatId is given - the friend
    if friendChatId:
        friend = getFriendOfUser(request.user, friendChatId)

    # load friend-chats if friend was given
    if friend:
        chatname = "Friend " + friend.username
        chatId = friend.id
        chattype = "friend"

    # load some global lists and show chat
    friendlist = Friendlist.objects.filter(creator=request.user)
    return render(request, "index.html", {'friendlist': friendlist,
                                          'chatname': chatname,
                                          'chatId': chatId,
                                          'chattype': chattype,
                                          })


# show form to add a new friend, includes processing variants (id, name or eMail given correct or wrong)
def addfriend(request):
    # make sure the current user is authenticated. If not go to login-screen
    if not request.user.is_authenticated:
        return redirect("login")

    errorMessage=None
    if request.method == "POST":
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend=None
            friendId=form.cleaned_data['friendId']
            friendName=form.cleaned_data['friendName']
            friendEmail=form.cleaned_data['friendEmail']

            # in case none of the following ifs matches, set friend id as default error message
            errorMessage = "Wrong friend id"
            if friendId is not None:
                # only friendId is evaluated, clean others if exist and use default error message
                friendName=""
                friendEmail=""

                # load possible friend if exist
                friend = getUserOrNone(user_id=friendId)

            if friendName != "":
                # only friendName is evaluated; friendId must be already None, clean other and set possible error message
                friendEmail=""
                errorMessage = "Wrong friend Name"

                # load possible friend if exist
                friend = getUserOrNone(user_name=friendName)

            if friendEmail != "":
                # only friendEmail is evaluated (others must already be cleaned), set possible error message
                errorMessage = "Wrong friend eMail"

                # load possible friend if exist
                friend = getUserOrNone(user_email=friendEmail)

            # check if user exist, is not current logged in user and is not an existing friend
            if friend and friend != request.user and not getFriendOfUser(request.user, friend.id):
                Friendlist.objects.create(creator=request.user, friend=friend)
                return redirect('index')
    else:
        form = AddFriendForm()

    return render(request, 'addfriend.html', {'form': form,
                                              'errorMessage': errorMessage})

def creategroup(request):
    # make sure the current user is authenticated. If not go to login-screen
    if not request.user.is_authenticated:
        return redirect("login")

    errorMessage=None
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():

            # Gruppe erschaffen und in DB abspeichern.
            # --> Form noch anpassen, dass alle Freunde geladen und ankreuzbar sind
            chatName = form.cleaned_data['chatName']
            # auslesesn welche Freunde angekreuzt wurden.
            addedFriends = form.cleaned_data['addedFriends']
            for i in addedFriends:
                # Für jeden Freund Verbindung zu GroupChat erstellen
                pass

    else:
        form = CreateGroupForm()

    return render(request, 'creategroup.html', {'form': form,
                                              'errorMessage': errorMessage})
