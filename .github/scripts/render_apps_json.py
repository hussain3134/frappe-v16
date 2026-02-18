import base64
import json
import os
import sys

LOCK_FILE = "versions.lock.json"


def main() -> int:
    with open(LOCK_FILE, "r", encoding="utf-8") as f:
        versions = json.load(f)

    apps = [
        {"url": "https://github.com/frappe/erpnext", "tag": versions["erpnext"]},
        {"url": "https://github.com/frappe/hrms", "tag": versions["hrms"]},
        {"url": "https://github.com/resilient-tech/india-compliance", "tag": versions["india_compliance"]},
        {"url": "https://github.com/frappe/crm", "tag": versions["crm"]},
        # ecommerce_integrations: track branch until v16 tags exist
        {"url": "https://github.com/frappe/ecommerce_integrations", "branch": "version-16"},
    ]

    # compact JSON (avoid whitespace differences)
    apps_json = json.dumps(apps, separators=(",", ":"))
    encoded = base64.b64encode(apps_json.encode("utf-8")).decode("utf-8")

    env_file = os.environ.get("GITHUB_ENV")
    if not env_file:
        print("GITHUB_ENV is not set (this script should run inside GitHub Actions).", file=sys.stderr)
        return 1

    with open(env_file, "a", encoding="utf-8") as f:
        f.write(f"APPS_JSON_BASE64={encoded}\n")

    print("Exported APPS_JSON_BASE64 for apps:")
    for a in apps:
        if "tag" in a:
            print(f"- {a['url']} tag={a['tag']}")
        else:
            print(f"- {a['url']} branch={a['branch']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
