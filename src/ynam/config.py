import json
import os


secretsPath = os.path.expanduser("~/.ynamrc")
keys = [
    'api_key',
    'username',
    'password',
    'account_id',
    'budget_id',
]


def _updateSecrets():
    try:
        with open(secretsPath, 'r+') as file:
            return json.load(file)
    except:
        return {}


def update(key, value):
    secrets = _updateSecrets()
    # don't overwrite non-blank value with blank value
    # if no value at all, add blank value.
    if value != '' or not secrets[key]:
        secrets[key] = value
        with open(secretsPath, 'w+') as file:
            file.write(json.dumps(secrets, indent=2))
    return secrets


def valueOf(key):
    secrets = _updateSecrets()
    try:
        return secrets[key]
    except KeyError:
        update(key, '')
        return valueOf(key)


def all():
    return _updateSecrets()


def newfile():
    for key in keys:
        update(key, '')
