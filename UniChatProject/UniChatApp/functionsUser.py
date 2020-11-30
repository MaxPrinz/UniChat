# useful functions for User-Management and User-Handling
from django.contrib.auth.models import User

from .models import Friendlist, Settings, Groupchat


# returns a user-object or None, if user not exits
# at least one of the parameters user_id, user_name or user_email should be given
def getUserOrNone(user_id=None, user_name=None, user_email=None):
    try:
        if user_id:
            return User.objects.get(id=user_id)
        if user_name:
            return User.objects.get(username=user_name)
        if user_email:
            return User.objects.get(email=user_email)
    except User.DoesNotExist:
        return None

    # no if matched, return none
    return None


# checks if the friend_id is a really friend of the given user
def getFriendOfUser(user, friend_id):
    # check if friend exist
    friend=getUserOrNone(user_id=friend_id)
    if not friend:
        return None

    # check if friend is really a friend
    friendlistEntry = getFriendlistOrNone(creator=user, friend=friend)
    if not friendlistEntry:
        return None

    # all good, the two are friends, return the friend
    return friend


# gets the given friendlist-entry or none, if not found
def getFriendlistOrNone(creator, friend):
    try:
        friendlistEntry = Friendlist.objects.get(creator=creator, friend=friend)
    except Friendlist.DoesNotExist:
        # second try: exchange friend and creator
        try:
            friendlistEntry = Friendlist.objects.get(creator=friend, friend=creator)
        except Friendlist.DoesNotExist:
            return None
    return friendlistEntry


# check if the given user has a valid settings object
def hasUserValidSettings(user):
    try:
        settings = Settings.objects.get(pk=user)
    except Settings.DoesNotExist:
        return False
    return True


# get the groupchat, if user is member
def getGroupchatUserIsMemberOrNone(user, group_id):
    try:
        group = Groupchat.objects.get(pk=group_id)
    except Groupchat.DoesNotExist:
        return None

    # if user was creator, he is a member
    if group.creator == user:
        return group

    # is user in member-list?
    if user in group.member.all():
        return group

    # if we are here, user not found in groupchat nor created it
    return None
