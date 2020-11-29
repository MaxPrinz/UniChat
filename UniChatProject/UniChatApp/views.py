from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import SettingsForm, AddFriendForm, CreateGroupForm
from .functionsUser import getFriendOfUser, getUserOrNone, getFriendlistOrNone, hasUserValidSettings
from .models import Settings, Friendlist, Groupchat, ChatMessage
from .simpleGoogleTranslate import simpleGoogleTranslate
import os, datetime

# Create your views here.

def index(request):
    return showChat(request)


def settingsView(request):
    # make sure the current user is authenticated. If not go to login-screen
    if not request.user.is_authenticated:
        return redirect("login")

    # find the settings linked with user
    # if no linked settings item exist, create an empty one
    user = request.user
    if hasUserValidSettings(user):
        settings = Settings.objects.get(pk=user)
    else:
        settings = Settings.objects.create(user=user)

    # normal settings-form-prcessing
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=settings)
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


def showChat(request, friendChatId=None, groupChatId=None):
    if not request.user.is_authenticated:
        return redirect("login")

    # go to settings if user has currently no settings set
    if not hasUserValidSettings(request.user):
        return redirect("settings")


    # set some variables
    chatname = "Global"
    chatId = -1
    chattype = "global"
    friend = None
    group = None
    chatMessages = []
    currentChatImagePath = ""
    friendList = None

    # load - if friendChatId is given - the friend
    if friendChatId:
        friend = getFriendOfUser(request.user, friendChatId)

    # load friend-chats if friend was given
    if friend:
        chatname = "Friend " + friend.username
        chatId = friend.id
        chattype = "friend"
        friendList = getFriendlistOrNone(creator=request.user, friend=friend)
        currentChatImagePath = '/uniChat/media/profile/' + str(friend.id)
        if friendList:
            chatMessages = ChatMessage.objects.filter(linkedFriendList=friendList)

    if groupChatId:
        group = Groupchat.objects.get(id=groupChatId)

    if group:
        chatname = group.title
        chattype = "group"
        chatMessages = ChatMessage.objects.filter(linkedGroupchat=groupChatId)
        currentChatImagePath = 'https://cdn3.iconfinder.com/data/icons/speech-bubble-2/100/Group-512.png'

    if friend == None and group == None:
        chattype = "global"
        chatMessages = ChatMessage.objects.filter(linkedGroupchat=None).filter(linkedFriendList=None)
        currentChatImagePath = 'https://lh3.googleusercontent.com/proxy/HUpbM9Z9oxElsb-8vIwsHmDbHVvCpcO5Pq4SfgO0bTu-MoTJhNEYC56XV_zhA5Xxb20matIF2UxJUG35tMordhcWiwVq7vRFQwKJgLZIdUM_p7q0bVZQk8V8ryQoJfN4wokZpNtWPJAKMz3xh34'

    # load some global lists and show chat
    friendlistQuery = Friendlist.objects.filter(Q(creator=request.user) | Q(friend=request.user))
    friendlist = []

    # create displayName-field with a useful name for template
    for oneEntry in friendlistQuery:
        if oneEntry.creator == request.user:
            oneEntry.displayName = oneEntry.friend.username
            oneEntry.idForLink = oneEntry.friend.id
            oneEntry.imagePath = '/uniChat/media/profile/' + str(oneEntry.friend.id)
        else:
            oneEntry.displayName = oneEntry.creator.username
            oneEntry.idForLink = oneEntry.creator.id
            oneEntry.imagePath = '/uniChat/media/profile/' + str(oneEntry.creator.id)

        friendlist.append(oneEntry)

    if request.method == "POST":
            creator = request.user
            createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            language = request.user.settings.language
            message = str(request.POST.get("MessageText"))
            ChatMessage.objects.create(creator=creator, createdAt=createdAt, language=language, message=message,
                                       linkedFriendList= friendList, linkedGroupchat= group)


    # load all groupchats where the current user is part of (distinct because duplicates got created)
    groupchatlist = Groupchat.objects.filter(Q(member=request.user) | Q(creator=request.user)).distinct

    # Translation of messages into the language defined in the settings
    #load target language
    targetLanguage = request.user.settings.language.iso
    messagesTranlation = []
    for oneEntry in chatMessages:
        if oneEntry.language.iso != targetLanguage:
            translatedText = simpleGoogleTranslate(f"{oneEntry.message}", oneEntry.language.iso, targetLanguage)
            oneEntry.message = translatedText
        if oneEntry.creator != request.user:
            oneEntry.ProfileImagePath = '/uniChat/media/profile/' + str(oneEntry.creator.id)

    # testtext=simpleGoogleTranslate(" Hallo du da   ", "de", "en")
    # print(testtext)

    return render(request, "index.html", {'friendlist': friendlist,
                                          'groupchatlist': groupchatlist,
                                          'chatname': chatname,
                                          'chatId': chatId,
                                          'currentChatImagePath': currentChatImagePath,
                                          'chattype': chattype,
                                          'chatMessages': chatMessages,
                                                     })


# show form to add a new friend, includes processing variants (id, name or eMail given correct or wrong)
def addfriend(request):
    # make sure the current user is authenticated. If not go to login-screen
    if not request.user.is_authenticated:
        return redirect("login")

    errorMessage = None
    if request.method == "POST":
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend = None
            friendId = form.cleaned_data['friendId']
            friendName = form.cleaned_data['friendName']
            friendEmail = form.cleaned_data['friendEmail']

            # in case none of the following ifs matches, set friend id as default error message
            errorMessage = "Wrong friend id"
            if friendId is not None:
                # only friendId is evaluated, clean others if exist and use default error message
                friendName = ""
                friendEmail = ""

                # load possible friend if exist
                friend = getUserOrNone(user_id=friendId)

            if friendName != "":
                # only friendName is evaluated; friendId must be already None, clean other and set possible error message
                friendEmail = ""
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

    # TODO: Show also friends where the current user is the friend and the friend created friendlist-entry
    friends = Friendlist.objects.filter(creator=request.user)


    # create chat in database
    if request.method == "POST":

        form = CreateGroupForm(request.POST, instance=Groupchat.objects.create(creator=request.user))

        if form.is_valid():
            group = form.save()
            return redirect('index')
    else:
        form = CreateGroupForm()

    return render(request, 'creategroup.html', {'form': form,
                                                'friends': friends})
def test(request):
    return render(request, 'messenger_template.html')


def showProfilePicture(request, user_id):
    file = open(os.path.join(settings.MEDIA_ROOT, "profile", str(user_id)), "rb")
    data = bytes(file.read())
    response = HttpResponse(data, content_type='image/jpeg')
    return response
