from urllib.parse import urlencode
import requests
import networkx as nx
import pprint
import time
import json
import sys
import os


USER_ID = 'tim_leary'

SERVICE_KEY = '11403f8811403f8811403f886f111d4ac51114011403f88483602710fc57cbbd4d427c2'
APP_ID = '6124877'
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.67'
VK_METHOD = 'https://api.vk.com/method/'

# auth_data = {
#     'client_id' : APP_ID,
#     'response_type': 'token',
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'scope' : 'friends, status, groups',
#     'v' : VERSION,
# }
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))


TOKEN = 'e59f93e65f498f277491940f9f3e51b5a87d1d79b73373481ad2407837a1549a20fca0ea245a1647ef0a8'

class ShowWork:
    def __init__(self):
        self.points_num = 1

    def work(self):
        for i in range(self.points_num):
            print('.', end='')
        print('\r')
        self.points_num = self.points_num % 10
        self.points_num  = self.points_num  + 1


show = ShowWork()

def friends_of(user_id, output='list'):
    params = {
        'user_id': user_id,
        'v': VERSION,
    }
    response = requests.get(''.join((VK_METHOD, 'friends.get')), params)
    show.work()
    if response.json().get('error'):
        return []
    elif output == 'count':
        return response.json()['response']['count']
    return response.json()['response']['items']


def groups_of(user_id, output='list'):
    params = {
        'user_id': user_id,
        'access_token': TOKEN,
        'count': '10',
        'v': VERSION
    }
    response = {'error': {'error_code': 6}}
    try:
        while response['error']['error_code'] == 6:
            response = requests.get(''.join((VK_METHOD, 'groups.get')), params)
            time.sleep(0.05)
            show.work()
        return []
    except (KeyError, TypeError):
        if output == 'count':
            return response.json()['response']['count']
        return response.json()['response']['items']


def unique_groups_of(user_id):
    unique_groups_of_user_ids = set(groups_of(user_id))
    user_friends_ids = friends_of(user_id)
    for friend_id in user_friends_ids:
        if get_users(friend_id)[0].get('deactivated'):
            continue
        groups_of_friend_ids = set(groups_of(friend_id))
        unique_groups_of_user_ids = unique_groups_of_user_ids.difference(groups_of_friend_ids)
        if not unique_groups_of_user_ids:
            break
    return unique_groups_of_user_ids


def get_users(user_ids, name_case='nom'):
    params = {
        'user_ids': user_ids,
        'name_case': name_case
    }
    show.work()
    return requests.get(''.join((VK_METHOD, 'users.get')), params).json()["response"]


def get_group(group_id):
    params = {
        'access_token': TOKEN,
        'group_ids': group_id,
        'fields': [
            'members_count',
        ],
        'v': VERSION,
    }
    response = {'error': {'error_code': 6}}
    try:
        while response['error']['error_code'] == 6:
            response = requests.get(''.join((VK_METHOD, 'groups.getById')), params).json()
            time.sleep(0.05)
            show.work()
    except KeyError:
        return response['response']


def main():
    user = get_users(USER_ID)[0]
    user_name = '{} {}'.format(user['first_name'], user['last_name'])
    print('Количество групп, в которых состоит {} - {}.'.format(
                                            user_name, groups_of(user['uid'], 'count')))
    print('Группы, в которых нет ни одного из его друзей:')
    unique_groups_ids = unique_groups_of(user['uid'])
    with open(os.path.join(os.getcwd(), 'secret_groups.json'), 'w+', encoding='utf-8') as f:
        for group_id in unique_groups_ids:
            group = (get_group(group_id))
            print('Id: {}  название: {}  количество участников: {}'.format(
                                                group[0]['id'], group[0]['name'], group[0]['members_count']))
            json.dump(group, f, indent=1, ensure_ascii=False)


main()
