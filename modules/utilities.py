import json

from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied, ParseError


def get_response(data, status_code=200, message="", status=1, content_type="application/json"):
    return HttpResponse(json.dumps({
        "status": status,
        "message": message,
        "data": data
    }), content_type=content_type, status=status_code)


def verify_key(api_key):
    """
        Verifies if the api key is valid
        Ideally this would just do a search in the DB table with index, but since DB use is prohibited,
        using a file in the file system.
    Args:
        api_key: String.

    Returns:

    """
    if not api_key:
        raise PermissionDenied()
    key_file = settings.FILE_DIR + "/key_list.txt"
    try:
        with open(key_file, "r") as f:
            valid_keys = f.readlines()
            for valid_key in valid_keys:
                if valid_key.rstrip() == api_key.rstrip():
                    return
    except IOError:
        raise ParseError("No Keys exist. Please generate a key first.")
    raise PermissionDenied("API Key Invalid")
