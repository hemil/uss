import os
import errno

from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework.exceptions import PermissionDenied, ParseError, NotFound


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


def save_file(api_key, image_file):
    # TODO compress files
    """
        Saves image file to the disk as DB use is forbidden. Creates API key folder if it doesn't exist.
    Args:
        api_key: String
        image_file: Django InMemoryUploadedFile from request
    """
    folder_path = settings.FILE_DIR + "/" + api_key
    file_path = folder_path + "/" + image_file.name.replace(" ", "_")

    if image_file.name.split(".")[-1] not in ["jpeg", "jpg", "png"]:
        raise ParseError("Only jpg, jpeg and png formats allowed.")

    # Create folder if it doesn't exist and handle the race condition where the folder is created in between checking
    # it exists and creating it
    try:
        os.makedirs(folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    file_content = ContentFile(image_file.read())
    with open(file_path, "wb+") as f:
        for chunk in file_content.chunks():
            f.write(chunk)


def get_image(api_key, image_name):
    """
        Returns image to be returned
    Args:
        api_key:
        image_name:

    Returns:
        image_data: binary image data
        image_extension: extension of the image file

    """
    file_path = settings.FILE_DIR + "/" + api_key + "/" + image_name
    if not os.path.isfile(file_path):
        raise NotFound("No such image exists.")
    with open(file_path, "rb") as f:
        image_data = f.read()
    image_extension = image_name.split(".")[-1].lower()
    return image_data, image_extension


def get_image_list(api_key):

    """
        Utility function for get image list. Scans disk folder as DB Use is prohibited. Else a direct search based on
        Foreign Key would result in this.
    Args:
        api_key: String.

    Returns:
        files: List of image names
    """
    folder_path = settings.FILE_DIR + "/" + api_key
    files = []
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        for file_name in filenames:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                files.append(file_name)
    return files
