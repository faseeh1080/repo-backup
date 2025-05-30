# Repo Backup

_(By [FaseehFS](https://github.com/faseehfs/))_

This program clones all your repositories into a specified folder, making it easy to back up your GitHub repositories, **including LFS files**.

**NOTE:** The program will only clone up to 30 repositories. If you have fewer than 30, there won't be any issues.

## How to Configure

First, run the command `config`. It will generate a `config.json` file to configure the application. In the file, you'll see:

```json
{
  "users-and-organizations": [],
  "ignored-repos": [],
  "other-repos": [],
  "lfs": false,
  "backup-directory": "backup"
}
```

1. Here, add the names of the GitHub users and organizations in `users-and-organizations` list. All of their public repositories will be backed up when you run the application.

2. If there are public repositories that you don't need to back up, add their Web URLs (from GitHub Code tab) to `ignored-repos` list and they will be ignored.

3. In the `other-repos` list, add the web URLs of the other repositories you want to clone. For example, your private repositories.

4. If you also want to fetch LFS files, change `lfs` to `true`. If you have LFS installed, I recommend turning it on. It is turned off by default for people who don't have LFS installed.

5. `backup-directory` is the directory in which you back up your repos. It can be relative or absolute and is set to `backup` by default.

**NOTE:** Since GitHub API only shows public repositories for users without a Personal Access Token (PAT), you will need to add your private repositories to the `other-repos` list manually.

**NOTE:** For Windows, you will need to escape the backslashes with another backslash when adding the path to your backup directory.

## How to Run

Run the `backup` command to back up your repositories. It will clone all repositories that have not been cloned to the `backup-directory` and update the others, including LFS files, according to your configuration.

Use the option `--verbose` with the `backup` command to see the processes in more detail.

To reset the configuration, run the `config` command again; the `config.json` file will be regenerated.
