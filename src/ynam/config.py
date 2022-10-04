import json
from .parser import arg


secretsPath = arg('config_file_path')
keys = [
    'api_key',
    'username',
    'password',
    'account_id',
    'budget_id',
    'mfa_seed_token',
]


def _updateSecrets():
    # degenerate function on purpose. the filesystem is weird,
    # but it usually works out in the end, so we fail open.
    try:
        with open(secretsPath, 'r') as file:
            return json.load(file)
    except:
        return {}


def update(key, value):
    """
    Adds key:value pair to config
    Returns updated config
    """
    secrets = _updateSecrets()
    # don't overwrite non-blank value with blank value
    # if no value at all, add blank value.
    if value != '' or key not in secrets:
        secrets[key] = value
        with open(secretsPath, 'w+') as file:
            file.write(json.dumps(secrets, indent=2))
    return secrets


def valueOf(key):
    """
    finds value for given key, creates and returns blank value if none found
    """
    try:
        return _updateSecrets()[key]
    except KeyError:
        update(key, '')
        return valueOf(key)


def all():
    """
    returns entire raw config.
    """
    return _updateSecrets()


def newfile():
    """
    creates a new file with empty values.
    """
    for key in keys:
        update(key, '')
