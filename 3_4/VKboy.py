import requests
from pprint import pprint
import random

SERVICE_KEY = 'f6e4ed81f6e4ed81f6e4ed8133f6b82985ff6e4f6e4ed81afa2bb93663a2d6752706624'
APP_ID = '6079492'
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.65'
VK_METHOD = 'https://api.vk.com/method/'
MINE = 3026449


def friends_of(id, output='list'):
    params = {
        'user_id': id,
        'v': VERSION,
    }
    response = requests.get(''.join((VK_METHOD, 'friends.get')), params)
    # print(response.json())
    if response.json().get('error'):
        return []
    elif output == 'count':
        return response.json()['response']['count']
    return response.json()['response']['items']


def common_friends(user, min_common=1):
    user_friends_ids = set(friends_of(user))
    friends_of_all_ids = user_friends_ids
    for friend_id in user_friends_ids:
        intersected = set(friends_of(friend_id)).intersection(friends_of_all_ids)
        if len(intersected) >= min_common:
            friends_of_all_ids = intersected
    return friends_of_all_ids


def get_users(user_ids, name_case='nom'):
    params = {
        'user_ids': user_ids,
        'name_case': name_case
    }
    return requests.get(''.join((VK_METHOD, 'users.get')), params).json()['response']


def user_generator():
    while True:
        user_id = random.randint(10000, 300000000)
        print(user_id)
        user = get_users(user_id)[0]
        # print(user)
        if not (user.get('deactivated') or friends_of(user_id, 'count') == 0):
            break
    return user_id


def main():
    user = get_users(user_generator(), 'gen')[0]
    user_name = '{} {}'.format(user['first_name'], user['last_name'])
    print('Количество друзей {} - {}.'.format(user_name, friends_of(user['uid'], 'count')))
    print('Общие друзья его и всех его друзей:')
    user_common_friends_ids = common_friends(user['uid'])
    if not user_common_friends_ids:
        print('отсутствуют')
    else:
        friends = get_users(user_common_friends_ids)
        for friend in friends:
            print('{} {}'.format(friend['first_name'], friend['last_name']))


main()

