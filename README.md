# Hub harvester 
Gathers data from GitHub about a user or organisation by using the GitHub API to crawl its repositories.
This will be rather slow, so I recommend using an authentication token to help speed it up.

For documentation on how the `SQLite` database is formatted you can find it [here](docs/sqlite.md)
## Usage
- Install the `PyGithub` package: 
```bash
pip install pygithub
```
- Run the script in `src/`: **This will take a while to crawl**
```bash
python src/main.py
```

OR run the following:
```bash
git clone https://github.com/NamesCode/hub_harvester.git
cd hub_harvester
pip install pygithub
python src/main.py
```

### Using Nix
Run the following:
```bash
git clone https://github.com/NamesCode/hub_harvester.git
cd hub_harvester
nix develop
python src/main.py
```
