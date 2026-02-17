import json
import base64
import os

with open("versions.lock.json") as f:
    versions = json.load(f)

apps = [
    {"url": "https://github.com/frappe/erpnext", "tag": versions["erpnext"]},
    {"url": "https://github.com/frappe/hrms", "tag": versions["hrms"]},
    {"url": "https://github.com/resilient-tech/india-compliance", "tag": versions["india_compliance"]},
    {"url": "https://github.com/frappe/crm", "tag": versions["crm"]},
    {"url": "https://github.com/frappe/ecommerce_integrations", "branch": "version-16"},
]

encoded = base64.b64encode(json.dumps(apps).encode()).decode()
with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"APPS_JSON_BASE64={encoded}\n")

