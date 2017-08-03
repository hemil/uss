# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import json

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied

from modules.image_utilities import verify_key, save_file, get_image, get_image_list

logger = logging.getLogger("enterprise")


@api_view(["GET", "POST", "PATCH", "DELETE"])
def image_handler(request):
    if request.method == "GET":
        api_key = request.META.get("HTTP_API_KEY")
        verify_key(api_key)
        image_name = request.GET.get("image_name")

        if image_name:
            # Get one particular image
            image_data, image_extension = get_image(api_key, image_name)
            return HttpResponse(image_data, content_type="image/{image_extension}".format(
                image_extension=image_extension))
        else:
            # Get list of images
            image_list = get_image_list(api_key)
            return HttpResponse(json.dumps({
                "status": 1,
                "message": "",
                "error_code": 200,
                "data": image_list
            }), content_type="application/json", status=200)

    if request.method == "POST":
        api_key = request.META.get("HTTP_API_KEY")
        verify_key(api_key)
        image_file = request.FILES.get("image_file")
        save_file(api_key, image_file)
        return HttpResponse(json.dumps({
            "status": 1,
            "message": "Created file: {image_file}".format(image_file=image_file.name),
            "error_code": 201,
            "data": None
        }), content_type="application/json", status=201)
    try:
        return HttpResponse("The Wrath of Khan is on.", status=200)
    except Exception as e:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": "Exception: {e}".format(e=e),
            "error_code": 500,
            "data": None
        }), content_type="application/json", status=500)
