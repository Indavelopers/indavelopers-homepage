# Development processes

## Dev process

### Dev

1. Open project dir: `cd indavelopers-homepage`
1. Fetch new repo updates: `git fetch origin master`
1. Check repo history: `git log --oneline --graph --all`
1. Check Pyenv's Python version: `which python && python -V`
1. Start Python virtual env: `. .venv/bin/activate`
1. Open webapp dir: `cd webapp`
1. Run app in debug mode: `flask --debug --app main run`
1. Check on `localhost:5000` (default Flask port)

### Deploy

1. Choose GCP project in Cloud SDK and/or IDE: `gcloud config project set indavelopers`, `indavelopers`
1. Deploy to GAE: `gcloud app deploy --version VERSION_ID --no-promote`
1. Check on live version URL
1. Migrate traffic to new version: `gcloud app services set-traffic --splits="VERSION_ID"=1`
    1. Or do a live deploy to the newest version: `gcloud app deploy --version VERSION_ID`
1. Commit changes
1. Push changes to remote repo

## Architecture

### Dependencies

- Python 3.12
  - Runtime managed by [Pyenv](https://realpython.com/intro-to-pyenv)
  - Virtual env: Pyenv's virtualenv
- Flask 3
- Google App Engine
  - Runtime: Python 3.12
