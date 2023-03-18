import os
import runpy
import sys
from pathlib import Path

import openmc_depletion_plotter


def main():
    path_to_app = str(Path(openmc_depletion_plotter.__path__[0]) / "app.py")

    # default is 200MB, this sets uplod file zise to 100GB
    os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "100000"

    sys.argv = ["streamlit", "run", path_to_app]
    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    main()
