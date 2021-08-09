### This script will be responsible for pulling all relevant data and saving it to a csv ###
import eventlet
eventlet.monkey_patch()
from time import time
import pandas as pd
import json
requests = eventlet.import_patched('requests')
import requests
from tqdm import tqdm


NODE_HOST = "https://api.bitclout.com"


def get_single_profile(username):
    # get a single profile based on username
    payload = {
        "Username": username        
    }
    endpoint = f"{NODE_HOST}/get-single-profile"
    response = requests.post(endpoint, json=payload).json()    
    profile = response['Profile']    
    payload['GetEntriesFollowingUsername']=True
    endpoint = f"{NODE_HOST}/get-follows-stateless"
    response = requests.post(endpoint, json=payload).json()            
    profile['NumFollowers'] = response['NumFollowers']
    payload['GetEntriesFollowingUsername'] = False
    response = requests.post(endpoint, json=payload).json()    
    profile['NumFollowing'] = response['NumFollowers']
    return profile


def get_profiles(payload=None):
    # get a bunch of profiles
    if payload is None:
        payload = {}
    endpoint = f"{NODE_HOST}/get-profiles"
    response = requests.post(endpoint, json=payload)
    return response.json()


def get_user_list(timeout=30, fetch=10000):
    # save a list of users to disk
    start = time()
    usernames = set()
    prev_length = len(usernames)
    try_again = False
    res = get_profiles({"NumToFetch": fetch})
    next_key = res['NextPublicKey']
    n_req = 1
    for p in res['ProfilesFound']:
        usernames.add(p['Username'])
    while len(usernames) > prev_length or try_again:
        res = get_profiles({"PublicKeyBase58Check": next_key,
                            "NumToFetch": fetch})
        next_key = res['NextPublicKey']
        if not next_key:
            next_key = res['ProfilesFound'][-1]['PublicKeyBase58Check']
            try_again = True
        else:
            try_again = False
        if isinstance(res, int):
            print(res)
            break
        prev_length = len(usernames)
        for p in res['ProfilesFound']:
            usernames.add(p['Username'])
        n_req += 1
        if n_req % 5 == 0:
            print(n_req, len(usernames))
        if time() - start > timeout:
            break
    print(len(usernames))
    with open('user_list.txt', 'w') as f:
        f.write("\n".join(usernames))


# get a few hundred random users
# get_user_list(timeout=15, fetch=10)
# save all bot data as json

def get_user(username, users):
    try:          
        user = get_single_profile(username)
        if not user:
            return
        print(username, user['Username'])
        users.append(user)
    except Exception as e:
        # pass
        print(e)


pool = eventlet.GreenPool(size=30)

for fname in ['my_bots', 'my_non_bots']:
    df = pd.read_csv(f'../{fname}.csv', names=['key', 'username'])
    users = []
    for u in df.username.values:                
        pool.spawn(get_user, u, users)        
    pool.waitall()
    with open(f'../{fname}.json', 'w') as f:
        json.dump(users, f)
