# useful functions for User-Management and User-Handling


# set filename for imageField
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def profilePicture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile/{0}'.format(instance.user.id)


# needed for imageField, see https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name
# needed to overwrite profile-image
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

