import json
import os
from dataclasses import dataclass

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
    if os.path.exists(arg('config_file_path')):
        with open(arg('config_file_path'), 'r') as file:
            fileSecrets = json.load(file)

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
        with open(arg('config_file_path'), 'w+') as file:
            file.write(json.dumps(secrets, indent=2))


stash = Secrets(**loadSecrets())
