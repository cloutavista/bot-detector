import csv
import os
from queue import Queue

import requests


def get_posts_for_username(username, n=1000):
    req = {
        "Username": username,
        "ReaderPublicKeyBase58Check": "",
        "LastPostHashHex": "",
        "NumToFetch": n,
        "MediaRequired": False
    }
    return requests.post('https://api.bitclout.com/get-posts-for-public-key', json=req).json().get('Posts', [])


def get_posts_for_public_key(public_key, n=100):
    req = {
        "PublicKeyBase58Check": public_key,
        "Username": "",
        "ReaderPublicKeyBase58Check": "",
        "LastPostHashHex": "",
        "NumToFetch": n,
        "MediaRequired": False
    }
    return requests.post('https://api.bitclout.com/get-posts-for-public-key', json=req).json().get('Posts', [])


def get_single_post(post_hash):
    req = {
        "PostHashHex": post_hash,
        "ReaderPublicKeyBase58Check": "",
        "FetchParents": True,
        "CommentOffset": 0,
        "CommentLimit": 200,
        "AddGlobalFeedBool": False
    }
    return requests.post('https://api.bitclout.com/get-single-post', json=req).json()['PostFound']


def is_duplicate(text, user_id, users_to_collect=None):
    '''
    curl 'https://cloutavista.com/posts?text=%D7%93%D7%99%D7%A9%D7%9A%D7%9D%D7%A6&size=10&page=1'  
    '''
    posts = requests.get(
        f"https://cloutavista.com/posts?text=\"{text}\"&size=50").json()['data']
    sorted_by_time = sorted(posts, key=lambda post: post['published_at'])
    if not sorted_by_time:
        return False
    original = sorted_by_time[0]
    if users_to_collect is not None:
        users_to_collect.extend(
            [{
                "public_key": p['ProfileEntryResponse']['PublicKeyBase58Check'],
                "username": p['ProfileEntryResponse']['Username']
            } for p in sorted_by_time[1:]])
    # print(f"post has {len(sorted_by_time)} copies")
    return original['ProfileEntryResponse']['PublicKeyBase58Check'] != user_id


def build():
    # collect initial seed of users
    if not os.path.exists('users.csv'):
        diamondhands_posts = get_posts_for_username(
            'diamondhands')
        users = []
        for post in diamondhands_posts:
            post_with_comments = get_single_post(post['PostHashHex'])
            for comment in post_with_comments.get('Comments', []) or []:
                users.append({
                    "public_key": comment['ProfileEntryResponse']['PublicKeyBase58Check'],
                    "username": comment['ProfileEntryResponse']['Username']
                })
        seen = set()
        users = [x for x in users if x['username']
                 not in seen and not seen.add(x['username'])]
        with open('users.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)

    # for each user collect timeline
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
        # users = [s.strip() for s in f.readlines()]
    bots = []
    non_bots = []
    seen = set()
    queue = Queue()
    for user in users:
        if user['username'] not in seen:
            seen.add(user['username'])
            queue.put(user)
    while not queue.empty():
        user = queue.get()
        total, copies = 0, 0
        # for each post in timeline, search on cloutavista
        posts = get_posts_for_public_key(user['public_key'], n=10)
        if posts is None:
            continue
        for post in posts:
            new_users = []
            try:
                is_copy = is_duplicate(
                    post['Body'], user['public_key'], new_users)
                if new_users:
                    for new_user in new_users:
                        if new_user['username'] not in seen:
                            seen.add(new_user['username'])
                            queue.put(new_user)
                            print(f"added {new_user['username']}")
                total += 1
                if is_copy:
                    copies += 1
            except:
                continue
        # count number of clouts who are replicas (copies of other clout) and the percentage of copies
        print(
            f"user {user['username']} have {copies} duplicates out of {total} clouts")
        if copies > .5 * total:
            bots.append(user)
        elif copies <= .1 * total:
            non_bots.append(user)
        if bots and len(bots) % 10 == 0:
            with open('bots.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=bots[0].keys())
                writer.writerows(bots)
        if non_bots and len(non_bots) % 10 == 0:
            with open('non_bots.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=non_bots[0].keys())
                writer.writerows(non_bots)
    if bots:
        with open('bots.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=bots[0].keys())
            writer.writeheader()
            writer.writerows(bots)
    if non_bots:
        with open('non_bots.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=non_bots[0].keys())
            writer.writeheader()
            writer.writerows(non_bots)


build()
