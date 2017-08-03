from __future__ import unicode_literals
import logging

from django.core.management import call_command
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError

from modules.utilities import verify_key, get_response

logger = logging.getLogger("enterprise")


@api_view(["POST", "PUT", "DELETE"])
def key_handler(request):
    if request.method == "POST":
        # For simplicity. On prod, put some auth on this or remove it completely and operate it from your aws machine
        generated_key = call_command('generate_key')
        return get_response(generated_key, message="New Key Generated", status_code=201)
    if request.method == "PUT":
        api_key = request.META.get("HTTP_API_KEY")
        verify_key(api_key)
        generated_key = call_command('regenerate_key', old_key=api_key)
        if generated_key:
            return get_response(generated_key, message="New Key Generated", status_code=201)
        else:
            raise ParseError("Old Key Details missing")
