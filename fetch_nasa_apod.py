import requests
import os
from environs import env
from support_scripts import displays_image_format, download_file


def fetch_nasa_apod(key):
    url_nasa = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': key,
        'count': 30,
        'thumbs': False,
    }
    response = requests.get(url_nasa, params=payload)
    response.raise_for_status()
    url_contents = response.json()
    image_adresses = []
    for url_content in url_contents:
        if 'video' in url_content['media_type']:
            continue
        img_url = url_content['url']
        image_adresses.append(img_url)
    for number, image in enumerate(image_adresses):
        path = f'images/nasa_apod_{number}{displays_image_format(image)}'
        download_file(image, path)


def main():
    env.read_env()
    dir_path = env.str('DIRECTORY_PATH', default='images')
    os.makedirs(dir_path, exist_ok=True)
    nasa_api_key = env.str('NASA_API')
    fetch_nasa_apod(nasa_api_key)


if __name__ == '__main__':
    main()