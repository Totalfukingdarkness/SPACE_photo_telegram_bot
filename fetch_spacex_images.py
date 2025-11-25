import requests
import argparse
import os
from support_scripts import download_file


def fetch_spacex_last_launch(args):
    url_spacex = 'https://api.spacexdata.com/v5/launches/{0}'.format(args)
    response = requests.get(url_spacex)
    response.raise_for_status()
    departure_images = response.json()['links']['flickr']['original']
    for number, picture in enumerate(departure_images):
        path = 'images/spacex_{0}.jpeg'.format(number)
        download_file(picture, path)


def main():
    os.makedirs('images', exist_ok=True)
    parser = argparse.ArgumentParser(description='''Default is latest lauches''')
    parser.add_argument('--id', help='ID', default='latest')
    args = parser.parse_args()
    fetch_spacex_last_launch(args.id)


if __name__ == '__main__':
    main()
