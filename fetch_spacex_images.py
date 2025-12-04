import requests
import argparse
import os
from environs import Env
from support_scripts import download_file

env = Env()
env.read_env()


def fetch_spacex_last_launch(launch_id):
    url_spacex = 'https://api.spacexdata.com/v5/launches/{0}'.format(launch_id)
    response = requests.get(url_spacex)
    response.raise_for_status()
    departure_images = response.json()['links']['flickr']['original']
    for number, picture in enumerate(departure_images):
        path = 'images/spacex_{0}.jpeg'.format(number)
        download_file(picture, path)


def main():
    dir_path = env.str('DIRECTORY_PATH', default='images')
    os.makedirs(dir_path, exist_ok=True)
    parser = argparse.ArgumentParser(description='Загрузка изображений последнего запуска SpaceX.')
    parser.add_argument("--id", help="ID запуска (по умолчанию последний)", default="latest")
    args = parser.parse_args()
    fetch_spacex_last_launch(args.id)


if __name__ == '__main__':
    main()
