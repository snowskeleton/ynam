import json
import os
from pathlib import Path


secretsPath = os.path.expanduser("~") + "/.ynam/secrets.json"
keys = [
    'api_key',
    'username',
    'password',
    'account_id',
    'budget_id',
]
file = Path(os.path.expanduser('~/.ynam')).mkdir(parents=True, exist_ok=True)


def _updateSecrets():
    # try:
    with open(secretsPath, 'r+') as file:
        return json.load(file)
    # except:
    #     return {}


def update(key, value):
    secrets = _updateSecrets()
    # don't overwrite non-blank value with blank value
    # if no value at all, add blank value.
    if value != '' or not secrets[key]:
        secrets[key] = value
        with open(secretsPath, 'w+') as file:
            file.write(json.dumps(secrets))
    return secrets


def valueOf(key):
    secrets = _updateSecrets()
    return secrets[key] if secrets[key] else ''


def all():
    return _updateSecrets()


def newfile():
    for key in keys:
        update(key, '')
