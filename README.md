# MineVis

MineVis is a 3D visualization software designed to aid in Mining research.

## Packaging

Run the following command to create a pip-installable package:
`python setup.py sdist bdist_wheel`


## Testing

Create a `.coveragerc` file with the following content:

```python
[coverage:run]
branch = True

[coverage:report]
show_missing = True
omit = 
    *__init__.py*
    minevis/main.py
    minevis/example.py
    venv/*
    minevis/*/tests/*

```

Run the following command: `pytest --cov=.`.

Alternatively, run `./run_tests.sh`.

