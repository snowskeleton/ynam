import json
import os
from dataclasses import dataclass
from json import JSONDecodeError

from .ynam_parser import arg


@dataclass
class Secrets():

    ynab_api_key: str = None
    ynab_account_id: str = None
    ynab_budget_id: str = None

    mint_username: str = None
    mint_password: str = None
    mint_mfa_seed: str = None


def loadSecrets():
    fileSecrets = {}
    path = arg('config_file')
    if os.path.exists(path):
        with open(path) as file:
            try:
                fileSecrets = json.load(file)
            except JSONDecodeError:
                print(f'Error reading {file.name}; assuming it to be empty')
                return {}

    for key in {
            k: v
            for k, v in vars(Secrets).items() if not k.startswith('_')
    }:
        if arg(key) is not None:
            fileSecrets[key] = arg(key)
    return fileSecrets


def updateStash(key, value):
    if value != '':
        secrets = {**loadSecrets()}
        secrets[key] = value
        with open(arg('config_file'), 'w+') as file:
            file.write(json.dumps(secrets, indent=2))


stash = Secrets(**loadSecrets())
