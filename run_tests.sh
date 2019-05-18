#!/usr/bin/env sh
python -m pytest --cov=. tests/ --cov-report term-missing

