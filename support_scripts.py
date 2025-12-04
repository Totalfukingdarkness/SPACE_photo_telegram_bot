import requests
from urllib.parse import urlparse, splitext


def determine_image_format(url):
    parsed_url = urlparse(url)
    _, extension = splitext(parsed_url.path)
    return extension


def download_file(url, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def send_image(bot, path, chat_id):
    with open(path, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)