import os
from pprint import pprint

from jira_api import add_release_to_issue, get_or_create_release
from notes_parser import extract_changes, extract_issue_id

# Get the git tag name
tag_name = os.environ["GITHUB_REF_NAME"]

# Get the release name format (default to '{version}' if not set)
release_name_format = os.environ.get("INPUT_RELEASE_NAME_FORMAT", "{version}")

# Validate that the format string contains {version}
if "{version}" not in release_name_format:
    print(f"WARNING: release_name_format '{release_name_format}' does not contain '{{version}}' placeholder.")
    print(f"Using tag name '{tag_name}' as release name instead.")
    release_name = tag_name
else:
    # Format the release name by replacing {version} with the tag name
    release_name = release_name_format.replace("{version}", tag_name)

release = get_or_create_release(release_name)
print("JIRA Release:")
pprint(release)

changes = extract_changes()
print("Release Issues:")
pprint(changes)

for change in changes:
    issue_id = extract_issue_id(change["title"])
    if not issue_id:
        print("No issue id:", change["title"])
        continue
    print("Updating", issue_id)
    add_release_to_issue(release_name, issue_id)
