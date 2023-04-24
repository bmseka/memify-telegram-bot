import requests
import bs4
import telebot
import time
import logging
import pickle
import signal
import sys
import os
from tqdm import trange

bot = telebot.TeleBot('YOUR_TOKEN')

def get_html(url):
    response = requests.get(url)
    return response.text

def get_images(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    images = []
    descriptions = []
    divs = soup.find_all('div', class_='infinite-item card')
    for div in divs:
        img = div.find('img')
        if img:
            images.append(img['src'])
            try:
                descriptions.append(img['alt'])
            except KeyError:
                descriptions.append('')
    return images, descriptions

def send_images(images, descriptions):
    for i in range(len(images)):
        bot.send_photo('@YOUR_CHANNEL', images[i], descriptions[i])
        logging.info(f'Sent image {i+1} of {len(new_images)} to @YOUR_CHANNEL')
        save_last_images([images[i]])
        for i in trange(60, 0, -1):
        # делаем паузу в 1 секунду
            time.sleep(1)

def save_last_images(images):
    last_images = load_last_images()
    images = last_images + images
    with open('last_images.pickle', 'wb') as f:
        pickle.dump(images, f)

def load_last_images():
    if not os.path.exists('last_images.pickle'):
        with open('last_images.pickle', 'wb') as f:
            pickle.dump([], f)
    with open('last_images.pickle', 'rb') as f:
        return pickle.load(f)

def check_new_images(images):
    last_images = load_last_images()
    new_images = []
    new_descriptions = []
    for i in range(len(images)):
        if images[i] not in last_images:
            new_images.append(images[i])
            new_descriptions.append(descriptions[i])
    return new_images, new_descriptions

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

signal.signal(signal.SIGINT, signal_handler)

url = 'https://memify.ru/'

while True:
    html = get_html(url)
    logging.info(f'Got HTML from {url}')
    images, descriptions = get_images(html)
    logging.info(f'Found {len(images)} images on the site')
    new_images, new_descriptions = check_new_images(images)
    logging.info(f'Found {len(new_images)} new images to send')
    if new_images:
        send_images(new_images, new_descriptions)
        logging.info(f'Sent {len(new_images)} images to @YOUR_CHANNEL)
    for i in trange(300, 0, -1):
        # делаем паузу в 1 секунду
        time.sleep(1)
