from __future__ import unicode_literals
import logging
import json

from django.http import HttpResponse
from django.core.management import call_command
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError

from modules.utilities import verify_key

logger = logging.getLogger("enterprise")


@api_view(["POST", "PUT", "DELETE"])
def key_handler(request):
    if request.method == "POST":
        generated_key = call_command('generate_key')
        return HttpResponse(json.dumps({
                "status": 1,
                "message": "New Key Generated",
                "error_code": 201,
                "data": generated_key
            }), content_type="application/json", status=201)
    if request.method == "PUT":
        api_key = request.META.get("HTTP_API_KEY")
        verify_key(api_key)
        generated_key = call_command('regenerate_key', old_key=api_key)
        if generated_key:
            return HttpResponse(json.dumps({
                    "status": 1,
                    "message": "New Key Generated",
                    "error_code": 201,
                    "data": generated_key
                }), content_type="application/json", status=201)
        else:
            raise ParseError("Old Key Details missing")
