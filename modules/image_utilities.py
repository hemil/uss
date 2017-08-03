import os
import errno

from StringIO import StringIO

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework.exceptions import ParseError, NotFound


def save_image(api_key, image_file):
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

    # PIL compression only for jpeg and ong
    # makes it slow
    # possibly: save it normally and then shoot an event which will asynchronously compress it/upload it to cloud
    buff = StringIO()
    buff.write(image_file.read())
    buff.seek(0)
    pil_image = Image.open(buff)
    pil_image.save(file_path, optimize=True, quality=95)

    # direct save for other formats
    # file_content = ContentFile(image_file.read())
    # with open(file_path, "wb+") as f:
    #     for chunk in file_content.chunks():
    #         f.write(chunk)


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


def delete_image(api_key, image_name):
    """
        Deletes and image file
    Args:
        api_key: string.
        image_name: string
    """
    file_path = settings.FILE_DIR + "/" + api_key + "/" + image_name
    if not os.path.isfile(file_path):
        raise NotFound("No such image exists.")
    os.remove(file_path)
