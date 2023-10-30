import sqlite3
from getpass import getpass
from time import gmtime, strftime

from github import Auth, Github

database = sqlite3.connect(
    #    "ctp_database_" + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + ".sqlite3"  #TODO: uncomment for prod
    "ctp_database.sqlite3"
)

# github organisation
ORG = "Catppuccin"

authorise = input("Authorise to github? (yl:yes login, yt:yes token, n:no): ")
if authorise == "yl":
    AUTH = Auth.Login(input("Github username: "), getpass("Github password: "))
elif authorise == "yt":
    AUTH = Auth.Token(getpass("Input github auth token: "))
else:
    AUTH = None

# pygithub object
g = Github(auth=AUTH)

limit = g.rate_limiting
limit_reset = g.rate_limiting_resettime

print(limit)
print(limit_reset)

# get the ORG in a Github api instance
ORG_USER = g.get_user(ORG)
# repo = user.get_repo("emacs")

for repo in ORG_USER.get_repos():
    print(repo.stargazers_count)
    print(repo.name)

    for issue in repo.get_issues():
        if issue.state == "closed":
            print(issue.closed_at)
            print(issue.closed_by)
            print(issue.created_at)
            for assignee in issue.assignees:
                print(assignee)

    for pull in repo.get_pulls():
        if pull.merged:
            print(pull.created_at)
            print(pull.commits)
            print(pull.user)
            print(pull.merged_at)
            print(pull.merged_by)

    for commits in repo.get_commits():
        print(commits.sha)
        if commits.author != None:
            print(commits.author.name)
            print(commits.author.created_at)
        else:
            print(commits.committer.name)
            print(commits.committer.created_at)
