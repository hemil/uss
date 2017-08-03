# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from modules.image_utilities import save_image, get_image, get_image_list, patch_image, delete_image
from modules.utilities import verify_key, get_response

logger = logging.getLogger("enterprise")


@api_view(["GET", "POST", "PATCH", "DELETE"])
def image_handler(request):
    api_key = request.META.get("HTTP_API_KEY")
    verify_key(api_key)
    if request.method == "GET":
        image_name = request.GET.get("image_name")
        if image_name:
            # Get one particular image
            image_data, image_extension = get_image(api_key, image_name)
            return HttpResponse(image_data, content_type="image/{image_extension}".format(
                image_extension=image_extension))
        else:
            # Get list of images
            data = get_image_list(api_key)
            return get_response(data)

    elif request.method == "POST":
        # Assuming that it's not a partial update (though it should be, since it's PATCH).
        # As I don't think that partial updates of images are possible (tried it with a couple of local images)
        image_file = request.FILES.get("image_file")
        if not image_file:
            raise ValidationError("Image file needs to be sent")
        save_image(api_key, image_file)
        message = "Created file: {image_file}".format(image_file=image_file.name)
        return get_response(None, message=message, status_code=201)

    elif request.method == "PATCH":
        image_file = request.FILES.get("image_file")
        if not image_file:
            raise ValidationError("Image file needs to be sent")
        patch_image(api_key, image_file)
        message = "Updated file: {image_file}".format(image_file=image_file.name)
        return get_response(None, message=message, status_code=201)

    elif request.method == "DELETE":
        api_key = request.META.get("HTTP_API_KEY")
        verify_key(api_key)
        image_name = request.GET.get("image_file_name")
        if not image_name:
            raise ValidationError("Image file name needs to be sent")
        delete_image(api_key, image_name)
        message = "Deleted file: {image_file}".format(image_file=image_name)
        return get_response(None, message=message, status_code=200)
