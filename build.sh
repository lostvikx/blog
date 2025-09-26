#!/usr/bin/env bash

rm -rf site/
uv run generate.py
cd site/
python -m http.server
