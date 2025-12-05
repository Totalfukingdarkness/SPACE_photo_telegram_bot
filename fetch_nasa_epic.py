import requests
import datetime
import os
from environs import Env
from support_scripts import download_file


def fetch_nasa_epic(key):
    url_nasa = 'https://api.nasa.gov/EPIC/api/natural/'
    payload = {
        'api_key': key,
    }
    response = requests.get(url_nasa, params=payload)
    response.raise_for_status()
    url_contents = response.json()
    for number, url_content in enumerate(url_contents):
        name_image = url_content['image']
        date_time = url_content['date']
        date = datetime.datetime.fromisoformat(date_time)
        formatted_date = date.strftime('%Y/%m/%d')
        img_address = f'https://api.nasa.gov/EPIC/archive/natural/{formatted_date}/png/{name_image}.png'
        path = f'images/epic_{number}.png'
        download_file(img_address, path, payload)


def main():
    env = Env()
    env.read_env()
    dir_path = env.str('DIRECTORY_PATH', default='images')
    os.makedirs(dir_path, exist_ok=True)
    nasa_api_key = env.str('NASA_TOKEN')
    fetch_nasa_epic(nasa_api_key)


if __name__ == '__main__':
    main()
