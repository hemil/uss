import logging
import uuid
import os

from django.core.management import BaseCommand
from django.conf import settings

logger = logging.getLogger("enterprise")


class Command(BaseCommand):
    help = "Regenerate API Key"

    def handle(self, *args, **kwargs):
        # assuming traffic not as high as
        print "in command"
        old_key = kwargs.get("old_key")
        if not old_key:
            return None
        new_key = uuid.uuid1().hex

        # Assuming all the old images need to be available to the new key
        old_path = settings.FILE_DIR + "/" + old_key
        new_path = settings.FILE_DIR + "/" + new_key

        os.rename(old_path, new_path)

        # Possible race condition
        with open(settings.FILE_DIR + "/" + "key_list.txt", "r") as f:
            data = f.read()
            data = data.replace(old_key, new_key)
        with open(settings.FILE_DIR + "/" + "key_list.txt", "w+") as f:
            f.write(data)
        return new_key
