import logging
import uuid
import os

from django.core.management import BaseCommand
from django.conf import settings

logger = logging.getLogger("enterprise")


class Command(BaseCommand):

    help = "Generate API Keys"

    def handle(self, *args, **kwargs):
        # assuming traffic not as high as
        key = uuid.uuid1().hex
        
        file_name = settings.FILE_DIR + "/" + "key_list.txt"
        if os.path.exists(file_name):
            file_mode = "a"     # append if already exists
        else:
            file_mode = "w"     # make a new file if not
        
        # Possible race condition
        with open(file_name, file_mode) as f:
            f.write(key + "\n")
        return key
