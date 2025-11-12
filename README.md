# Setup mit VS Code

## Vorgehen

1. Devcontainer mit Python mittels `DevContainer: Add Configuration Files..` erzeugt
2. `Python: Create Environment...`
1. `pip install pipreqs`
1. `/workspaces/pizza/.venv/bin/pipreqs /workspaces/pizza --force --ignore .venv,.git`
1. `pip install -requirements.txt`