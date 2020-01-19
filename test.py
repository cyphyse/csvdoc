# -*- coding: <utf-8>
# extern
import sys
import os
import subprocess
# logging
import logging
logger = logging.getLogger(__file__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# search for python env in root directories
python_path = None
search_path = os.path.dirname(os.path.abspath(__file__))
while not search_path == os.path.dirname(search_path):
    for dir in os.listdir(search_path):
        if dir in ["env", "venv"]:
            candidate = os.path.join(search_path, dir, "bin", "python3")
            if os.path.isfile(candidate):
                python_path = candidate
        if python_path is not None:
            break
    if python_path is not None:
        break
    search_path = os.path.dirname(search_path)

if python_path is None:
    logger.warning("No virtual environment found, use python3 from os ...")
    python_path = "python3"
logger.info("Using following python environment to test: " + python_path)

subprocess.call(
    [
        python_path,
        "-m",
        "unittest",
        "discover", "-s", "./test", "-p", "test_*.py",
    ]
)
