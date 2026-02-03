"""
GitHub API functions for managing releases.
"""
import os
import requests
from urllib.parse import quote


def get_github_token():
    """Get GitHub token from environment."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    # Return None if token is empty or whitespace-only
    if token:
        token = token.strip()
        return token if token else None
    return None


def get_repository_info():
    """Get repository owner and name from environment."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        return None, None
    parts = repo.split("/")
    if len(parts) != 2:
        return None, None
    return parts[0], parts[1]


def update_release_name(tag_name, release_name):
    """
    Update the name of a GitHub release.
    
    Args:
        tag_name: The git tag name (used to identify the release)
        release_name: The new name for the release
        
    Returns:
        True if successful, False otherwise
    """
    token = get_github_token()
    if not token:
        print("WARNING: No GitHub token found. Cannot update GitHub release name.")
        print("Set GITHUB_TOKEN or GH_TOKEN environment variable to enable this feature.")
        return False
    
    owner, repo = get_repository_info()
    if not owner or not repo:
        print(f"WARNING: Could not parse repository information from GITHUB_REPOSITORY: {os.environ.get('GITHUB_REPOSITORY')}")
        return False
    
    # URL-encode the tag name to handle special characters
    encoded_tag = quote(tag_name, safe='')
    
    # Get the release by tag
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{encoded_tag}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        # Get the release
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        release = response.json()
        release_id = release["id"]
        current_name = release.get("name", "")
        
        # Only update if the name is different
        if current_name == release_name:
            print(f"GitHub release name is already '{release_name}'. No update needed.")
            return True
        
        # Update the release name
        update_url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
        update_data = {"name": release_name}
        
        response = requests.patch(update_url, json=update_data, headers=headers)
        response.raise_for_status()
        
        print(f"✓ Updated GitHub release name from '{current_name}' to '{release_name}'")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Failed to update GitHub release name: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False
