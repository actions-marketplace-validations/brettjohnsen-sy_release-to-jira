"""
Utility functions for version extraction and formatting.
"""
import re
import sys


def extract_version_number(tag_name, tag_format=None):
    """
    Extract version number from a tag using a configurable pattern.
    
    Args:
        tag_name: The git tag name
        tag_format: Optional regex pattern with a capture group () to extract version.
                   If not provided, returns the tag as-is.
                   Examples:
                   - 'release/prod/(.+)-RC\\.\\d+' extracts '1.1.0' from 'release/prod/1.1.0-RC.12'
                   - 'v(.+)' extracts '1.0.0' from 'v1.0.0'
                   - '(.+)-beta' extracts '2.0.0' from '2.0.0-beta'
        
    Returns:
        The extracted version number from the first capture group, or the original tag if:
        - No tag_format is provided
        - The pattern doesn't match
        - The pattern has no capture groups
    """
    # If no pattern provided, return the tag as-is
    if not tag_format:
        return tag_name
    
    try:
        match = re.match(tag_format, tag_name)
        if match and match.groups():
            # Return the first capture group
            return match.group(1)
    except re.error as e:
        print(f"WARNING: Invalid regex pattern '{tag_format}': {e}", file=sys.stderr)
        print(f"Using tag as-is: '{tag_name}'", file=sys.stderr)
        return tag_name
    
    # If no match or no capture groups, return the original tag name
    return tag_name
