import sys

from ._main.main import main

if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
