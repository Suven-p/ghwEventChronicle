import json
import os
import datetime
from dotenv import load_dotenv
import requests

load_dotenv()


def get_oauth_token():
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": os.getenv("TWITCH_CLIENT_ID"),
            "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
            "grant_type": "client_credentials",
        },
    )
    return response.json()


def revoke_token(token):
    response = requests.post(
        "https://id.twitch.tv/oauth2/revoke",
        params={
            "client_id": os.getenv("TWITCH_CLIENT_ID"),
            "token": token,
        },
    )
    return response


def get_user_id(username, authorization):
    response = requests.get(
        f"https://api.twitch.tv/helix/users?login={username}",
        headers=authorization,
    )
    return response.json()['data'][0]['id']


def get_user_videos(user_id, authorization, limit=100):
    obtained = 0
    videos = []
    cursors = []
    cursor = None
    while obtained < limit:
        to_get = min(limit - obtained, 100)
        response = requests.get(
            'https://api.twitch.tv/helix/videos',
            params={
                'user_id': user_id,
                'first': to_get,
                'after': cursor,
            },
            headers=authorization
        )
        videos.extend(response.json()['data'])
        obtained += len(response.json()['data'])
        cursor = response.json()['pagination']['cursor']
        cursors.append(cursor)
        print(response.json()['data'][-1])
        print(response.json()['pagination'])
    print('Cursors are:', cursors)
    return videos


def main():
    token = get_oauth_token()["access_token"]
    authorization = {
        'Authorization': f'Bearer {token}',
        'Client-Id': os.getenv("TWITCH_CLIENT_ID"),
    }
    user_id = get_user_id("MLH", authorization)
    user_videos = get_user_videos(user_id, authorization, 200)
    with open("user_videos.json", "w") as f:
        json.dump(user_videos, f, indent=4)
    print("Revoking token...", revoke_token(token))


if __name__ == "__main__":
    main()
