import base64
import json

import pyperclip

with open("dokploy/docker-compose-16.yml", "r") as f:
    compose = f.read()

with open("dokploy/template-16.toml", "r") as f:
    config = f.read()

template_object = {"compose": compose, "config": config}
template_object = json.dumps(template_object, indent=2)

print(template_object)

b = base64.b64encode(bytes(str(template_object), 'utf-8')) # bytes
base64_str = b.decode('utf-8')

print(base64_str)

pyperclip.copy(base64_str)
# pyperclip.copy(str(template_object))