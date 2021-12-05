#!/bin/sh
pwd >> boot_errors.txt
poetry run python3 main.py | tee boot_errors.txt
# poetry run python3 main.py

