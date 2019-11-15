# Repo Reporter

## Set-up

Follow these set-up instructions to start a local instance of Repo Reporter.

Be sure to `cd` to the root directory of this repo before running these commands.

### Create Private Environment File

The flask application will look for a file named `.env` in its root directory. If it finds it, it will load it to your local environment. Create this file.

`$ touch .env`

> `.env` is a file ignored by git.

### Create GitHub Personal Access Token

A GitHub account authenticates you to the GitHub API. Be sure the account has push privileges for the configured repos.

Create a personal access token on GitHub following these [instructions](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). Be sure to select the **repo** scope. No other scope is needed.

> This token should be kept secret.

### Store GitHub Personal Access Token in your local Environment

The token must be named `GITHUB_PERSONAL_ACCESS_TOKEN`

`$ echo GITHUB_PERSONAL_ACCESS_TOKEN=your-newly-aquired-super-secret-token > .env`

### Install MongoDB

Install MongoDB on Mac Catalina using Homebrew.

```sh
$ brew tap mongodb/brew
$ brew install mongodb-community
```

### Start Mongo Daemon

Start the mongo daemon on it's default port.

`$ mongod --dbpath /usr/local/var/mongodb`

### Python3

Ensure you have Python3 installed.

`$ python3 --version`

> This project is built using Python 3.7.3, the macOS Catalina default.

### Create Python3 Virtual Environment

Create a Python3 virtual environment named `repo-reporter-venv`:

`$ python3 -m venv repo-reporter-venv`

> Actually, you can name the virtual environment whatever you want with no breaking changes.

### Activate Python3 Virtual Environment

Ask linux to run the activate program located in the virtual environment.

`$ source repo-reporter-venv/bin/activate`

### Install Project Dependencies

Install dependencies to the `repo-reporter-venv` virtual environment lib.

`$(repo-reporter-venv) pip install -r ./requirements.txt`

### Start Flask Server

Start the flask server on the default port, `5000`.

`$(repo-reporter-venv) flask run`
