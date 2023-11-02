# SQLite database documentation
Data in the dump is stored in 4 different tables:
- [Repos](#Repos)
- [Issues](#Issues)
- [Pulls](#Pulls)
- [Commits](#Commits)

## Repos
The table is labelled as `repos` with the following table structure:

| id  | name | stargazers |
|-----|------|------------|
| int | str  | int        |


## Issues
The table is labelled as `issues` with the following table structure:

| repo | issue_id  | comment_usernames | comment_creation_dates | assignees | created_at | closed_at |
|------|-----------|-------------------|------------------------|-----------|------------|-----------|
| str  | int       | [ str ]           | [ date ]               | [ str ]   | date       | date      |


## Pulls
The table is labelled as `pulls` with the following table structure:

| repo | pull_id  | comment_usernames | comment_creation_dates | commit_shas | created_at | created_by | merged_at | merged_by |
|------|----------|-------------------|------------------------|-------------|------------|------------|-----------|-----------|
| str  | int      | [ str ]           | [ date ]               | [ str ]     | date       | str        | date      | str       |


## Commits
The table is labelled as `commits` with the following table structure:

| repo | sha | author | created_at |
|------|-----|--------|------------|
| str  | str | str    | date       |
