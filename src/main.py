import os.path
import sqlite3
from getpass import getpass
from time import gmtime, strftime

from github import Auth, Github

# github organisation or user
ORG = input("organisation or user to crawl: ")

# filename = ORG + "_database_" + strftime("%Y-%m-%d", gmtime()) + ".sqlite3"
filename = ORG + "_database_2023-11-01.sqlite3"

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

# get the ORG in a Github api instance
ORG_USER = g.get_user(ORG)

if os.path.isfile("./" + filename) == False:
    database = sqlite3.connect(filename)
    db_cursor = database.cursor()
    last_repo = 0

    db_cursor.execute("CREATE TABLE repos(id, name, stargazers)")
    db_cursor.execute(
        # "CREATE TABLE issues(repo, id, comment_usernames, comment_creation_dates, assignees, created_at, closed_at, closed_by )"
        "CREATE TABLE issues(repo, issue_id, comment_usernames, comment_creation_dates, assignees, created_at, closed_at )"
    )
    db_cursor.execute(
        "CREATE TABLE pulls(repo, pull_id, comment_usernames, comment_creation_dates, commit_shas, created_at, created_by, merged_at, merged_by )"
    )
    db_cursor.execute("CREATE TABLE commits(repo, sha, author, created_at)")

else:
    database = sqlite3.connect(filename)
    db_cursor = database.cursor()
    last_repo = db_cursor.execute(
        "SELECT id FROM repos ORDER BY id DESC LIMIT 1"
    ).fetchone()[0]

repos_data = []
issues_data = []
pulls_data = []
commits_data = []
repo_counter = 0

for repo in ORG_USER.get_repos():
    repo_counter += 1
    if last_repo < repo_counter:
        repo_name = repo.name
        print("crawling " + repo_name)
        repos_data.append((repo_counter, repo_name, repo.stargazers_count))
        print("getting issues for " + repo_name)

        for issue in repo.get_issues("none", "all"):
            # print(issue.as_pull_request().url) #FIX: get this working at some pointcomment_usernames_list

            comment_usernames_list = "["
            comment_creation_dates_list = "["
            for comment in issue.get_comments():
                comment_usernames_list += str(comment.user.name) + ", "
                comment_creation_dates_list += str(comment.created_at) + ", "
            if comment_usernames_list != "[":
                comment_usernames_list = comment_usernames_list[:-2] + "]"
            else:
                comment_usernames_list = "[ ]"
            if comment_creation_dates_list != "[":
                comment_creation_dates_list = comment_creation_dates_list[:-2] + "]"
            else:
                comment_creation_dates_list = "[ ]"

            closed_at = "None"
            closed_by = "None"
            assignees = "[ ]"

            if issue.state == "closed":
                assignee_list = "["
                for assignee in issue.assignees:
                    assignee_list += str(assignee.name) + ", "
                if assignee_list != "[":
                    assignee_list = assignee_list[:-2] + "]"
                else:
                    assignee_list = "[ ]"

                closed_at = issue.closed_at
                closed_by = (
                    issue.closed_by
                )  # FIX: get this to give users name in future, dont use since its broken as shit
                assignees = assignee_list

            issues_data.append(
                (
                    repo_name,
                    issue.id,
                    comment_usernames_list,
                    comment_creation_dates_list,
                    assignees,
                    issue.created_at,
                    closed_at,
                    # closed_by,
                )
            )

        print("getting pulls for " + repo_name)
        for pull in repo.get_pulls("closed"):
            if pull.merged:
                comment_usernames_list = "["
                comment_creation_dates_list = "["
                for comment in pull.get_comments():
                    comment_usernames_list += str(comment.user.name) + ", "
                    comment_creation_dates_list += str(comment.created_at) + ", "
                if comment_usernames_list != "[":
                    comment_usernames_list = comment_usernames_list[:-2] + "]"
                else:
                    comment_usernames_list = "[ ]"
                if comment_creation_dates_list != "[":
                    comment_creation_dates_list = comment_creation_dates_list[:-2] + "]"
                else:
                    comment_creation_dates_list = "[ ]"

                commit_list = "["
                for commit in pull.get_commits():
                    commit_list += str(commit.sha) + ", "
                if commit_list != "[":
                    commit_list = commit_list[:-2] + "]"
                else:
                    commit_list = "[ ]"

                pulls_data.append(
                    (
                        repo_name,
                        pull.id,
                        comment_usernames_list,
                        comment_creation_dates_list,
                        commit_list,
                        pull.created_at,
                        pull.user.name,
                        pull.merged_at,
                        pull.merged_by.name,
                    )
                )

        print("getting commits for " + repo_name)
        for commits in repo.get_commits():
            if commits.committer != None:
                commit_author = commits.committer.name
                commit_creation_date = commits.committer.created_at

            if commits.author != None:
                commit_author = commits.author.login
                commit_creation_date = None
            else:
                commit_author = None
                commit_creation_date = None

            commits_data.append(
                (
                    repo_name,
                    commits.sha,
                    commit_author,
                    commit_creation_date,
                )
            )

        db_cursor.executemany("INSERT INTO repos VALUES(?, ?, ?)", repos_data)
        # db_cursor.executemany("INSERT INTO issues VALUES(?, ?, ?, ?, ?, ?, ?, ?)", issues_data)
        db_cursor.executemany(
            "INSERT INTO issues VALUES(?, ?, ?, ?, ?, ?, ?)", issues_data
        )
        db_cursor.executemany(
            "INSERT INTO pulls VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", pulls_data
        )
        db_cursor.executemany("INSERT INTO commits VALUES(?, ?, ?, ?)", commits_data)

        database.commit()

        repos_data = []
        issues_data = []
        pulls_data = []
        commits_data = []

print("Finished! :3")

database.close()
