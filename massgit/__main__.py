import os.path
import sys

from ._main.main import main

if __name__ == "__main__":
    main(
        sys.argv[1:],
        install_config_dir=os.path.normpath(os.path.join(__file__, "..", "..", "etc")),
    )
