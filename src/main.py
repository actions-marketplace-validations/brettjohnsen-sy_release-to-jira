import os
from pprint import pprint

from jira_api import add_release_to_issue, get_or_create_release
from notes_parser import extract_changes, extract_issue_id
from version_utils import extract_version_number


# Get the git tag name
tag_name = os.environ["GITHUB_REF_NAME"]

# Extract version number from the tag
version = extract_version_number(tag_name)
print(f"Extracted version '{version}' from tag '{tag_name}'")

# Get the release name format (default to '{version}' if not set)
release_name_format = os.environ.get("INPUT_RELEASE_NAME_FORMAT", "{version}")

# Validate that the format string contains {version}
if "{version}" not in release_name_format:
    print(f"WARNING: release_name_format '{release_name_format}' does not contain '{{version}}' placeholder.")
    print(f"Using version '{version}' as release name instead.")
    release_name = version
else:
    # Format the release name by replacing {version} with the extracted version
    release_name = release_name_format.replace("{version}", version)

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
