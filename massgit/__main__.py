import os

from massgit._main.clone import clone
from massgit._repo import load_repos

if __name__ == "__main__":
    os.chdir("dev")
    repos = load_repos()
    clone(repos)
