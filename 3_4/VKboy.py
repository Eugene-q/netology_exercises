import requests
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


VERSION = '5.65'
VK_METHOD = 'https://api.vk.com/method/'
USER_ID = 10002


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


def common_friends(user_id):
    user_friends_ids = friends_of(user_id)
    common_friends_ids = set(friends_of(user_friends_ids[0]))
    for friend_id in user_friends_ids:
        if get_users(friend_id)[0].get('deactivated'):
            continue
        friends_of_friend_ids = set(friends_of(friend_id))
        intersected = friends_of_friend_ids.intersection(common_friends_ids)
        if not intersected:
            break
        common_friends_ids = intersected
    return common_friends_ids


def build_graph(user_id):
    G = nx.Graph()
    user_edges = []
    user_friends_ids = friends_of(user_id)
    for friend_id in user_friends_ids:
        G.add_edge(user_id, friend_id)
        user_edges.append((user_id, friend_id))
        nodes = set(friends_of(friend_id)).intersection(user_friends_ids)
        G.add_edges_from([(friend_id, x) for x in nodes])

    pos = graphviz_layout(G, prog='twopi', args='')
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos, node_size=10, alpha=0.5, node_color="green", with_labels=False)
    nx.draw_networkx_nodes(G, pos, nodelist=[user_id], node_size=100, node_color='r')
    nx.draw_networkx_edges(G, pos, edgelist=user_edges, edge_color='red')
    plt.axis('equal')
    plt.savefig('friends_graph.png')
    # plt.show()


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
    build_graph(USER_ID)


main()
