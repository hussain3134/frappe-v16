import base64
import json

import pyperclip

with open("build/docker-compose.yml", "r") as f:
    compose = f.read()

with open("build/template.toml", "r") as f:
    config = f.read()

template_object = {"compose": compose, "config": config}
template_object = json.dumps(template_object, indent=2)

print(template_object)

b = base64.b64encode(bytes(str(template_object), 'utf-8')) # bytes
base64_str = b.decode('utf-8')

print(base64_str)

pyperclip.copy(base64_str)
# pyperclip.copy(str(template_object))