import os
import argparse
from random import shuffle
from time import sleep
from environs import env
from support_scripts import send_image


def send_all_images(tg_token, tg_chat_id):
    parse = argparse.ArgumentParser(description='''Отправляет все имеющиеся фото, по умолчанию, кажде 4 часа.''')
    parse.add_argument('-n', '--name', help='image name')
    args = parse.parse_args()
    seconds = env.int('TIME', default=14400)
    while True:
        if args.name is None:
            for dirpath, dirnames, filenames in os.walk('images'):
                shuffle(filenames)
                for file_name in filenames:
                    file_path = f'images/{file_name}'
                    send_image(tg_token, file_path, tg_chat_id)
                    sleep(seconds)
        else:
            file_path = f'images/{args.name}'
            send_image(tg_token, file_path, tg_chat_id)
            sleep(seconds)


def main():
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    os.makedirs('images', exist_ok=True)
    send_all_images(tg_token, tg_chat_id)


if __name__ == '__main__':
    main()