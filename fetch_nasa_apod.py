import requests
import os
from environs import Env
from support_scripts import download_file, determine_image_format

env = Env()
env.read_env()


def fetch_nasa_apod(api_key):
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    payload = {
            'api_key': api_key,
            'image_count': 30,
            'thumbs': False}
    try:
        response = requests.get(url_nasa, params=payload)
        response.raise_for_status()
        contents = response.json()
        image_urls = extract_image_urls(contents)
        save_images(image_urls)
    except requests.RequestException as err:
        print(f"Ошибка подключения к API: {err}")


def extract_image_urls(contents):
    return [
        item['url'] for item in contents
        if item['media_type'] == 'image'
    ]


def save_images(image_urls):
    directory = env.str("DIRECTORY_PATH", default="images")
    os.makedirs(directory, exist_ok=True)
    for index, url in enumerate(image_urls):
        file_path = f"{directory}/nasa_apod_{index}{determine_image_format(url)}"
        download_file(url, file_path)


def main():
    nasa_api_key = env.str("NASA_TOKEN_API")
    fetch_nasa_apod(nasa_api_key)


if __name__ == "__main__":
    main()
