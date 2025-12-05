import os
import argparse
from random import choice
from environs import Env
from support_scripts import send_image
from telegram import Bot


def main():
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    tg_bot = Bot(token=tg_token)
    dir_path = env.str('DIRECTORY_PATH', default='images')
    os.makedirs(dir_path, exist_ok=True)
    parse = argparse.ArgumentParser(description='''Отправляет случайное фото.
                                                Чтобы отправить определенное фото,
                                                укажите в аргументе название файла''')
    parse.add_argument("-n", "--name", help="Имя конкретного изображения для отправки")
    args = parse.parse_args()
    if args.name is None:
        path = dir_path
        files = os.listdir(path)
        random_files = choice(files)
        file_path = f'{path}{random_files}'
    else:
        file_path = f'images/{args.name}'
    send_image(tg_bot, file_path, tg_chat_id)


if __name__ == '__main__':
    main()