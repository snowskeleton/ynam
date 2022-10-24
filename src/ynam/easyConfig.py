# from os import path as ospath
# import json


# class Configer():

#     def __init__(self, name):
#         self.secretsPath = name
#         if not ospath.exists(self.secretsPath):
#             with open(self.secretsPath, 'w') as newfile:
#                 newfile.write('')

#     def secretsDump(self):
#         """
#         for ease of use
#         """
#         try:
#             with open(self.secretsPath, 'r') as file:
#                 return json.load(file)
#         except:
#             return {}

#     def update(self, key, value):
#         """
#       Adds key:value pair to config
#       Returns updated config
#       """
#         secrets = self.secretsDump()
#         # don't overwrite non-blank value with blank value
#         # if no value at all, add blank value.
#         if value != '' or key not in secrets:
#             secrets[key] = value
#             with open(self.secretsPath, 'w+') as file:
#                 file.write(json.dumps(secrets, indent=2))
#         return secrets

#     def valueOf(self, key):
#         """
#         returns saved value for given key
#         """
#         return self.secretsDump()[key]
