import urllib.parse, requests
from requests.exceptions import HTTPError, RequestException
import validators
import os

def identify_input_filetype(input):
    _, file_extension = os.path.splitext(input)
    if file_extension.lower() == '.jpg':
        return "image/jpg"
    elif file_extension.lower() == '.jpeg':
        return "image/jpeg" 
    elif file_extension.lower() == '.png':
        return "image/png"
    elif file_extension.lower() == '.gif':
        return "image/gif"
    elif file_extension.lower() == '.mp4':
        return "video/mp4"
    elif file_extension.lower() == '.avi':
        return "video/avi"
    elif file_extension.lower() == '.mov':
        return "video/mov"
    elif file_extension.lower() == '.mkv':
        return "video/mkv"
    else:
        return None

def get_image_info_safe(input):
    try:
        if validators.url(input):
            image_info = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(input))).json()
            return image_info
        else:
            image_info = requests.post("https://api.trace.moe/search", data=open(input, "rb"),
                                       headers={"Content-Type": identify_input_filetype(input)}).json()
            return image_info
    except HTTPError as HE:
        print("There was an HTTP error:", HE)
        return None
    except RequestException as RE:
        print("There was an error during request:", RE)
        return None


def most_similar_info(input):
    return get_image_info_safe(input)["result"][0]


def cut_blackborder(input):
    try:
        if validators.url(input):
            image_info = requests.get("https://api.trace.moe/search?cutBorders&url={}".format(urllib.parse.quote_plus(input))).json()
            return image_info
        else:
            image_info = requests.post("https://api.trace.moe/search?cutBorders", data=open(input, "rb"),
                                       headers={"Content-Type": identify_input_filetype(input)}).json()
            return image_info
    except HTTPError as HE:
        print("There was an HTTP error:", HE)
        return None
    except RequestException as RE:
        print("There was an error during request:", RE)
        return None


def most_similar_info2(input):
    return cut_blackborder(input)["result"][0]

