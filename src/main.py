import sqlite3
from getpass import getpass
from time import gmtime, strftime

import requests
from github import Auth, Github
from pprintpp import pprint

database = sqlite3.connect(
    #    "ctp_database_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + ".sqlite3"  #TODO: uncomment for prod
    "ctp_database.sqlite3"
)

# github username
username = "Catppuccin"
# url to request
# url = f"https://api.github.com/users/{username}"
# make the request and return the json
# user_data = requests.get(url).json()
# pretty print JSON data
# pprint(user_data)

authorise = input("Authorise to github? (yl:yes login, yt:yes token, n:no): ")
if authorise == "yl":
    auth = Auth.Login(input("Github username: "), getpass("Github password: "))
elif authorise == "yt":
    auth = Auth.Token(getpass("Input github auth token: "))
else:
    auth = None

# pygithub object
g = Github(auth=auth)

limit = g.rate_limiting
limit_reset = g.rate_limiting_resettime
print(limit)
print(limit_reset)

# get that user by username
user = g.get_user(username)
repo = user.get_repo("emacs")

# for repo in user.get_repos():
for commits in repo.get_commits():
    limit = g.rate_limiting
    print(commits)
    if limit[0] != 0:
        if commits.author != None:
            print(commits.author.name)
        else:
            print(commits.committer.name)
        print(commits.author.created_at)
