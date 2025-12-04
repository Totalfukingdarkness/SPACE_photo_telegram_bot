import os
import argparse
from random import shuffle
from time import sleep
from environs import Env
from telegram import Bot
from support_scripts import send_image

env = Env()
env.read_env()


def send_all_images(bot, tg_chat_id):
    parser = argparse.ArgumentParser(description="Отправляет все доступные фото.")
    parser.add_argument("-n", "--name", help="Имя конкретного изображения для отправки")
    args = parser.parse_args()
    seconds = env.int("TIME", default=14400)
    while True:
        if args.name is None:
            for dirpath, dirnames, filenames in os.walk(env.str("DIRECTORY_PATH", default="images")):
                shuffle(filenames)
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if not os.path.exists(file_path):
                        print(f"Файл '{filename}' не найден!")
                        continue
                    send_image(bot, file_path, tg_chat_id)
                    sleep(seconds)
        else:
            file_path = os.path.join(env.str("DIRECTORY_PATH", default="images"), args.name)
            if not os.path.exists(file_path):
                print(f"Файл '{args.name}' не найден!")
                break
            send_image(bot, file_path, tg_chat_id)
            sleep(seconds)


def main():
    tg_token = env.str("TG_TOKEN")
    tg_chat_id = env.str("TG_CHAT_ID")
    dir_path = env.str("DIRECTORY_PATH", default="images")
    os.makedirs(dir_path, exist_ok=True)

    bot = Bot(token=tg_token)
    send_all_images(bot, tg_chat_id)


if __name__ == "__main__":
    main()
