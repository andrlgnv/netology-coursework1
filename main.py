import requests
import os
import json
import time
from tqdm import tqdm
from pprint import pprint

VK_USER_ID = input('Введите ID пользователя: ')
VK_TOKEN = input('Введите token VK: ')
url = 'https://api.vk.com/method/photos.get'

YA_TOKEN = input('Введите token Yandex: ')
url_upload_photo = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
params_create_folder = {'path': 'coursework1'}
ya_headers = {'Content-Type': 'application/json',
                  'Authorization': YA_TOKEN}


def get_photo_data():
    api = requests.get(url, params={
        'v': '5.131',
        'owner_id': VK_USER_ID,
        'access_token': VK_TOKEN,
        'album_id': 'profile',
        'extended': 1
    })
    return api.json()

def get_photo():
    photo = []
    data = get_photo_data()['response']['items']
    for i in data:
        photo.append({'name': i['likes']['count'], 'url': i['sizes'][-1]['url'], 'size': i['sizes'][-1]['type'], 'date': i['date']})
    return photo

def write_json():
    with open('results', 'w') as outfile:
        for i in get_photo():
            json.dump(i, outfile, ensure_ascii=False, indent=2)

def create_folder(url_create_folder, params_create_folder, ya_headers):
    requests.put(url_create_folder, params=params_create_folder, headers=ya_headers)

def upload_photo():
    res = get_photo()
    names = []
    counter = 0
    for i in tqdm(res, desc='Photos uploading', unit=' photo'):
        name = str(i['name'])
        if name in names:
            seconds = i['date']
            spl = time.ctime(seconds).split()
            upload_date = f'{spl[2]}_{spl[1]}_{spl[4]}'
            name = name + '_' + upload_date
        names.append(name)
        params_upl_photo = {
            'path': f'coursework1/{name}.jpg',
            'url': i['url']
        }
        response = requests.post(url_upload_photo, params=params_upl_photo, headers=ya_headers)
        counter += 1
    print(f'Uploaded {counter} photos.')

def main():
    create_folder(url_create_folder, params_create_folder, ya_headers)
    upload_photo()
    write_json()

if __name__ == '__main__':
    main()