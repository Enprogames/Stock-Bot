# Stock-Bot
A Bot written in python to trade stocks (and crypto in the future?). At the moment, the [Alpaca trading API](https://alpaca.markets/docs/api-documentation/) is being used for making trades, but this might be changed in the future, as we've had many problems with it.
## Current Tasks
- [x] Allow for trades to be made and viewed through the alpaca API
- [ ] Allow for stock data to be viewed and updated through alpaca data streaming API
- [ ] Create simulated trading environment for historical data
- [ ] Create algorithm which can be used to trade in either simulated or real environment
## Installation
1. Install [Python](https://www.python.org/downloads/)
1. Create fork of the repository
2. Setup [github ssh keys](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for your current device if you haven't yet.
3. Ensure [git is installed](https://git-scm.com/downloads)
4. Clone fork: `git clone https://github.com/username/Stock-Bot.git`
5. Change to project directory: `cd Stock-Bot`
6. Run setup.sh: `./setup.sh`. This will do the following (note that these commands can be run manually if desired):
     1. Create virtual environment using venv:
         1. Windows: `python -m venv venv --prompt stock-bot`
         2. Linux: `python3 -m venv venv --prompt stock-bot` 
     2. Activate virtual environment: 
         1. Windows: `source venv/Scripts/activate`
         2. Linux: `source venv/bin/activate`
     3. Install requirements: `pip install -r requirements.txt`
     4. Install pre-commit git hooks: `pre-commit install`
     5. Setup post-merge hooks to update pip, requirements, and hooks on merge.
## Running
This project is currently not in a runnable state. You can look at and tinker with the code in this repository, but at the moment there is no specific way of running the project.
## Contributing
1. Move into cloned directory: `cd Stock-Bot`
2. Add upstream remote if you haven't already (view currently set remotes through `git remote -v`): `git remote add upstream git@github.com:Enprogames/Stock-Bot.git`
3. Pull in any changes: `git pull upstream main`
4. Create new branch for the issue you will be working on: `git checkout -b your-branch-name`
5. Make changes to the project
6. Run pre-commit hooks through `pre-commit run --all-files` and make necessary changes to ensure all hooks pass. Pre-commit will not allow you to commit until all hooks have passed.
7. Add any new files through: `git add .` and commit them through: `git commit -am "useful commit message; Closes #123"`. 
8. Pull in any new changes (which could have been made while you were working) and rebase your commits on top of these changes: `git pull upstream main --rebase`
9. Push your changes to your fork: `git push origin your-branch-name`
10. Navigate to your fork on github.com and open a new pull request ![PULL-REQUEST-EXAMPLE](https://user-images.githubusercontent.com/10604391/125674000-d02eb7a0-b85d-4c8f-b8dd-2b144e274f7d.png) If an option doesn't immediately show up to open a pull request when navigating to your fork, click on the branch button and click contribute to open one.
11. Fill out pull request with useful information about changes.
12. Checkout main branch: `git checkout main`.
13. Contribute again by starting at step 3.
