"""
Utility functions for version extraction and formatting.
"""
import re


def extract_version_number(tag_name):
    """
    Extract version number from a tag.
    
    Supports tags in the format: release/prod/[version]-RC.[number]
    Example: "release/prod/1.1.0-RC.12" -> "1.1.0"
    
    The version number must follow semantic versioning (X.Y.Z format).
    If the tag doesn't match the expected pattern, returns the tag as-is
    for backward compatibility.
    
    Args:
        tag_name: The git tag name
        
    Returns:
        The extracted version number (X.Y.Z) or the original tag if no match
    """
    # Pattern to match: release/prod/[version]-RC.[number]
    # This captures the semantic version number part (X.Y.Z) before -RC
    pattern = r'release/prod/([0-9]+\.[0-9]+\.[0-9]+)-RC\.[0-9]+'
    
    match = re.match(pattern, tag_name)
    if match:
        return match.group(1)
    
    # If no match, return the original tag name for backward compatibility
    return tag_name
