import requests

VERSION = '5.65'
VK_METHOD = 'https://api.vk.com/method/'
USER_ID = 10000


def friends_of(id, output='list'):
    params = {
        'user_id': id,
        'v': VERSION,
    }
    response = requests.get(''.join((VK_METHOD, 'friends.get')), params)
    if response.json().get('error'):
        return []
    elif output == 'count':
        return response.json()['response']['count']
    return response.json()['response']['items']


def common_friends(user):
    user_friends_ids = friends_of(user)
    common_friends_ids = set(friends_of(user_friends_ids[0]))
    for friend_id in user_friends_ids:
        if get_users(friend_id)[0].get('deactivated'):
            continue
        intersected = set(friends_of(friend_id)).intersection(common_friends_ids)
        if not intersected:
            break
        common_friends_ids = intersected
    return common_friends_ids


def get_users(user_ids, name_case='nom'):
    params = {
        'user_ids': user_ids,
        'name_case': name_case
    }
    return requests.get(''.join((VK_METHOD, 'users.get')), params).json()['response']


def main():
    user = get_users(USER_ID, 'gen')[0]
    user_name = '{} {}'.format(user['first_name'], user['last_name'])
    print('Количество друзей {} - {}.'.format(user_name, friends_of(user['uid'], 'count')))
    print('Общие друзья всех его друзей:')
    common_friends_of_friends_ids = common_friends(user['uid'])
    common_friends_of_friends = get_users(common_friends_of_friends_ids)
    for friend in common_friends_of_friends:
        print('{} {}'.format(friend['first_name'], friend['last_name']))


main()
