import requests as re
from tools.config import config

def get_token() -> str:
    client_id = config['credential']['client_id']
    client_secret = config['credential']['client_secret']
    res = re.post(
        url="https://id.twitch.tv/oauth2/token",
        data={
            "client_id":client_id,
            "client_secret":client_secret,
            "grant_type":"client_credentials",
            "scopes": 'chat%3Aread%20chat%3Aedit'
        }
    )
    return res.json().get('access_token')

def validate_token(token):
    res = re.get(
        url='https://id.twitch.tv/oauth2/validate',
        headers={"Authorization": f"OAuth {token}"}
    )
    print(res)

if __name__ == '__main__':
    validate_token(get_token())
    