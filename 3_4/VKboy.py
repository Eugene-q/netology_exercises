import requests
from pprint import pprint
import random

VERSION = '5.65'
VK_METHOD = 'https://api.vk.com/method/'
USER_ID = 10000


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


def common_friends(user):
    user_friends_ids = friends_of(user)
    friends_of_all_ids = set(friends_of(user_friends_ids[0]))
    for friend_id in user_friends_ids:
        # print('friend id : ', friend_id)
        # print(get_users(friend_id))
        # print('all : ', friends_of_all_ids)
        # print('friends of friend : ', friends_of(friend_id))
        if get_users(friend_id)[0].get('deactivated'):
            continue
        intersected = set(friends_of(friend_id)).intersection(friends_of_all_ids)
        if not intersected:
            break
        # print('intercec : ', intersected)
        friends_of_all_ids = intersected
        # print('all : ', friends_of_all_ids)
        # print()
    return friends_of_all_ids


def get_users(user_ids, name_case='nom'):
    params = {
        'user_ids': user_ids,
        'name_case': name_case
    }
    return requests.get(''.join((VK_METHOD, 'users.get')), params).json()['response']


def user_generator():
    while True:
        user_id = random.randint(1, 300000000)
        print(user_id)
        user = get_users(user_id)[0]
        friends_num = friends_of(user_id, 'count')
        # print(user)
        if not (user.get('deactivated') or friends_num == 0 or friends_num > 200):
            break
    return user_id


def main():
    user = get_users(USER_ID, 'gen')[0]
    user_name = '{} {}'.format(user['first_name'], user['last_name'])

    print('Количество друзей {} - {}.'.format(user_name, friends_of(user['uid'], 'count')))
    print('Общие друзья всех его друзей:')
    user_common_friends_ids = common_friends(user['uid'])
    if not user_common_friends_ids:
        print('отсутствуют')
    else:
        friends = get_users(user_common_friends_ids)
        for friend in friends:
            print('{} {}'.format(friend['first_name'], friend['last_name']))


main()

