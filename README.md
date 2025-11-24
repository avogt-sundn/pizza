# Setup mit VS Code

## Vorgehen

1. Devcontainer mit Python mittels `DevContainer: Add Configuration Files..` erzeugt
2. `Python: Create Environment...`
1. `pip install pipreqs`
1. `/workspaces/pizza/.venv/bin/pipreqs /workspaces/pizza --force --ignore .venv,.git`
1. `pip install -r requirements.txt`





## Resolved bugs

### Your system has an unsupported version of sqlite3.

```shell

Your system has an unsupported version of sqlite3. Chroma                     requires sqlite3 >= 3.35.0.
Please visit                     https://docs.trychroma.com/troubleshooting#sqlite to learn how                     to upgrade.
```