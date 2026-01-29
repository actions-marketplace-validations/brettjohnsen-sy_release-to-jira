# release-to-jira

A GitHub action to automatically create releases on JIRA.

Creates a release on Github. Uses its auto-generated description to find related JIRA issues and updates their "Fix versions" field. If a release matching the tag doesn't exist on JIRA, it will be automatically created.

This flow assumes auto-generated release notes will include JIRA issue keys. This can be achieved by including JIRA issue key in PR titles.

## Inputs

|Input|Description|Example|
|---|---|---|
|`jira_server`|JIRA server URL.|`https://company.atlassian.net`|
|`jira_project`|JIRA project key.|`PRJ`|
|`jira_user`|JIRA user with project admin permission.|`apiuser@company.com`|
|`jira_token`|JIRA token. Managed [here](https://id.atlassian.com/manage-profile/security/api-tokens).|`abcdef12345678`|
|`release_name_format`|(Optional) Format string for the release name. Use `{version}` as placeholder for the git tag name. Defaults to `{version}`.|`Release {version}`, `{version}-prod`, `v{version}`|


## Usage

Run when a new tag is created:

```yaml
on:
  push:
    tags:        
      - '*'
jobs:
  jira-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: Medsien/release-to-jira@main
        with:
          jira_server: 'https://company.atlassian.net'
          jira_project: 'PRJ'
          jira_user: 'user@company.com'
          jira_token: '${{ secrets.JIRA_TOKEN }}'
```

### With custom release name format

You can customize the release name format by using the `release_name_format` input. The `{version}` placeholder will be replaced with the git tag name:

```yaml
on:
  push:
    tags:        
      - '*'
jobs:
  jira-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: Medsien/release-to-jira@main
        with:
          jira_server: 'https://company.atlassian.net'
          jira_project: 'PRJ'
          jira_user: 'user@company.com'
          jira_token: '${{ secrets.JIRA_TOKEN }}'
          release_name_format: 'Release {version}'  # Creates releases like "Release v1.0.0"
```
