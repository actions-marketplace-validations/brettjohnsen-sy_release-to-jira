import os

import requests
from requests.auth import HTTPBasicAuth

BASE = os.environ["INPUT_JIRA_SERVER"]
PROJECT = os.environ["INPUT_JIRA_PROJECT"]
USER = os.environ["INPUT_JIRA_USER"]
TOKEN = os.environ["INPUT_JIRA_TOKEN"]

base_url = f"{BASE}/rest/api/3/"
project_path = f"project/{PROJECT}"
auth = HTTPBasicAuth(USER, TOKEN)


def get(endpoint, params=None):
    return requests.get(
        base_url + project_path + "/" + endpoint, params=params, auth=auth
    ).json()


def post(endpoint, body):
    return requests.post(base_url + endpoint, json=body, auth=auth)


def put(endpoint, body):
    return requests.put(base_url + endpoint, json=body, auth=auth)


def get_project_id():
    return get("")["id"]


def get_or_create_release(release_name):
    result = get("version", {"query": release_name})

    # Jira errors often look like:
    # {"errorMessages": [...], "errors": {...}}
    if isinstance(result, dict) and ("errorMessages" in result or "errors" in result):
        raise Exception(f"Jira API error while searching versions: {result}")

    # Defensive: ensure expected fields exist before using them
    total = result.get("total") if isinstance(result, dict) else None
    values = result.get("values") if isinstance(result, dict) else None

    if total is None or values is None:
        raise Exception(
            "Unexpected Jira response while searching versions. "
            f"Expected keys 'total' and 'values'. Got: {result}"
        )

    if total == 0:
        resp = post(
            "version",
            {"name": release_name, "projectId": get_project_id()},
        )

        # If your post() returns a Response-like object, keep this;
        # otherwise adjust based on your helper.
        created = resp.json()

        if isinstance(created, dict) and ("errorMessages" in created or "errors" in created):
            raise Exception(f"Jira API error while creating version '{release_name}': {created}")

        return created

    if total > 1:
        raise Exception(f"Found multiple releases with the same name: {release_name}")

    # total == 1
    return values[0]

def add_release_to_issue(release_name, issue):
    response = put(
        f"issue/{issue}",
        {"update": {"fixVersions": [{"add": {"name": release_name}}]}},
    )
    response.raise_for_status()
    return response.status_code == 204
