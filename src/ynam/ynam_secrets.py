import json
import os
from dataclasses import dataclass
from json import JSONDecodeError

from .ynam_parser import arg, logger


@dataclass
class Secrets():

    ynab_api_key: str = None
    ynab_account_id: str = None
    ynab_budget_id: str = None

    mint_username: str = None
    mint_password: str = None
    mint_mfa_seed: str = None


def _loadSecrets() -> dict:
    fileSecrets = {}
    path = arg('secrets_file')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path) as file:
            try:
                fileSecrets = json.load(file)
            except JSONDecodeError:
                logger.warn(
                    f'Error reading {file.name}; assuming it to be empty')
                return {}

    for key in {
            k: v
            for k, v in vars(Secrets).items() if not k.startswith('_')
    }:
        if arg(key) is not None:
            fileSecrets[key] = arg(key)
    return fileSecrets


def updateStash(key, value) -> None:
    secrets = {**_loadSecrets()}

    if key not in secrets.keys():
        secrets[key] = value

    logger.debug(
        'Secrets prior to update:\n'
        f'{secrets}'
    )
    if value == '':
        logger.info(
            f'Empty value for key: {key}. Maintaining current value: {secrets[key]}')  # noqa
        return

    logger.debug(f'Updating key: {key} to value: {value}')
    secrets[key] = value
    with open(arg('secrets_file'), 'w+') as file:
        logger.debug('Persisting to disk...')
        file.write(json.dumps(secrets, indent=2))
    secrets = {**_loadSecrets()}
    logger.debug(
        'Secrets after update:\n'
        f'{secrets}'
    )


def get_stash() -> Secrets:
    return Secrets(**_loadSecrets())
