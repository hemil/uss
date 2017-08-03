import logging
import uuid

from django.core.management import BaseCommand
logger = logging.getLogger("enterprise")


class Command(BaseCommand):

    help = "Generate API Keys"

    def handle(self, *args, **kwargs):
        # assuming traffic not as high as
        key = uuid.uuid1().hex
        return key
