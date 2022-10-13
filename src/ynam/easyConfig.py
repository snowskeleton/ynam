import os
import json

keys = [
    'api_key',
    'username',
    'password',
    'account_id',
    'budget_id',
    'mfa_seed_token',
]


class Configer():

    def __init__(self, name):
        self.name = name
        self.secretsPath = os.path.expanduser(f'~/.{self.name}')

    def newfile(self):
        with open(self.secretsPath) as newfile:
            newfile.write()

    def secretsDump(self):
        """
      for ease of use
      """
        with open(self.secretsPath, 'r') as file:
            return json.load(file)

    def get(self, key):
        pass

    def put(self, key):
        pass

    def update(self, key, value):
        """
      Adds key:value pair to config
      Returns updated config
      """
        secrets = self.secretsDump()
        # don't overwrite non-blank value with blank value
        # if no value at all, add blank value.
        if value != '' or key not in secrets:
            secrets[key] = value
            with open(self.secretsPath, 'w+') as file:
                file.write(json.dumps(secrets, indent=2))
        return secrets

    def valueOf(self, key):
        """
        returns saved value for given key
        """
        return self.secretsDump()[key]
