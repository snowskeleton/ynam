import json
import os


secretsPath = os.path.expanduser("~") + "/.ynam/secrets.json"
keys = [
    'api_key',
    'username',
    'password',
    'account_id',
    'budget_id',
]


def _updateSecrets():
    with open(secretsPath, 'r+') as file:
        return json.load(file)


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
    if key in keys:
        return secrets[f'{key}']
    return '--no value found--'


def all():
    return secrets


def newfile():
    for key in keys:
        update(key, '')
