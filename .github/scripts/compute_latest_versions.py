from __future__ import annotations
import json
import re
import subprocess
import urllib.request

LOCK_FILE = "versions.lock.json"

def git_latest_tag(repo_url: str, major: str) -> str:
    regex = rf"v{major}\.\d+\.\d+"
    out = subprocess.check_output(
        [
            "git",
            "-c",
            "versionsort.suffix=-",
            "ls-remote",
            "--refs",
            "--tags",
            "--sort=v:refname",
            repo_url,
            f"refs/tags/v{major}.*",
        ],
        text=True,
    )
    tags = []
    for line in out.splitlines():
        _sha, ref = line.split()
        tag = ref.replace("refs/tags/", "")
        if re.fullmatch(regex, tag):
            tags.append(tag)
    if not tags:
        raise RuntimeError(f"No v{major} tags found for {repo_url}")
    return tags[-1]

def git_branch_sha(repo_url: str, branch: str) -> str:
    out = subprocess.check_output(
        ["git", "ls-remote", repo_url, f"refs/heads/{branch}"],
        text=True,
    ).strip()
    sha, _ = out.split()
    return sha

def github_latest_release(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": "builder"})
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read().decode())
    tag = payload["tag_name"]
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise RuntimeError(f"Unexpected CRM tag format: {tag}")
    return tag

def load():
    try:
        with open(LOCK_FILE) as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(LOCK_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

def main():
    current = load()

    latest = {
        "erpnext": git_latest_tag("https://github.com/frappe/erpnext", "16"),
        "hrms": git_latest_tag("https://github.com/frappe/hrms", "16"),
        "crm": github_latest_release("frappe", "crm"),
        "india_compliance_ref": "refs/heads/version-16",
        "india_compliance_sha": git_branch_sha("https://github.com/resilient-tech/india-compliance", "version-16")
        "ecommerce_integrations_ref": "refs/heads/version-16",
        "ecommerce_integrations_sha": git_branch_sha("https://github.com/frappe/ecommerce_integrations", "version-16")
    }

    if latest == current:
        print("No changes")
        return

    print("Updating versions.lock.json")
    save(latest)

if __name__ == "__main__":
    main()

