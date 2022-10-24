from dataclasses import dataclass
import json
from .parser import arg


@dataclass
class Secrets():
    api_key: str = ''
    username: str = ''
    password: str = ''
    account_id: str = ''
    budget_id: str = ''
    mfa_seed_token: str = ''


def loadSecrets():
    try:
        with open(arg('config_file_path'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def updateStash(key, value):
    if value != '':
        secrets = {**loadSecrets()}
        secrets[key] = value
        with open(arg('config_file_path'), 'w+') as file:
            file.write(json.dumps(secrets, indent=2))


stash = Secrets(**loadSecrets())
