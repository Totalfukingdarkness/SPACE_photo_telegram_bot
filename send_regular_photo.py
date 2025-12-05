import os
from pathlib import Path
from random import shuffle
from time import sleep
from environs import env
from support_scripts import send_image
from telegram.error import NetworkError
from telegram import Bot


def send_all_images(tg_token, tg_chat_id, seconds, file_paths):
    while True:
        for file_path in file_paths:
            try:
                send_image(tg_token, file_path, tg_chat_id)
                sleep(seconds)
            except NetworkError:
                sleep(10)
        shuffle(file_paths)


def create_file_paths(path):
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file_name in filenames:
            file_path = Path(dirpath) / file_name
            file_paths.append(file_path)
        return file_paths


def main():
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    seconds = env.int('TIME', default=14400)
    dir_path = env.str('DIRECTORY_PATH', default='images')
    tg_bot = Bot(token=tg_token)
    Path(dir_path).mkdir(exist_ok=True)
    file_paths = create_file_paths(dir_path)
    send_all_images(tg_bot, tg_chat_id, seconds, file_paths)


if __name__ == '__main__':
    main()