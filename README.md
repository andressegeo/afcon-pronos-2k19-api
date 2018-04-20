# DGC Worldcup

## General
- gPXXX
- CdP: No one !
- dev: Andresse Njeungoue, Valentin Coudert, Vincent Tertre
- Dossier Drive: https://drive.google.com/drive/folders/1-psHxL-PypzUXhjdlc7iAzrZ39G1tLzY

## GCP
- project: https://console.cloud.google.com/home/dashboard?project=dgc-worldcup-russia-2018
- scope:
  - https://www.googleapis.com/auth/admin.directory.user.readonly
  - https://www.googleapis.com/auth/admin.directory.group.readonly

# Qu'est ce que c'est (technos)

Application web AppEngine / Python 2.7 / Flask / Angular / APIs Google (Admin SDK)

# Qu'est ce que ça fait

cf specs dans le dossier Drive.

# Installation

```bash
./tasks/setup.sh <path to Gcloud appengine sdk>
```

# Execution

```bash
source venv/bin/activate
dev_appserver.py ../dgc-worldcup/app.yaml api.yaml ../dgc-worldcup/dispatch.yaml
# ... then
deactivate
```

# Deploiement

```bash
./tasks/deploy.sh <dev|production|acceptance> <version>
```

