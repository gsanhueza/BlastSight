# MineVis

MineVis is a 3D visualization software designed to aid in Mining research.

## Packaging

You need to have `setuptools` and `wheel` installed.

Run the following command to create a pip-installable package:
`python setup.py bdist_wheel`

## Testing

Create a `.coveragerc` file with the following content:

```python
[coverage:run]
branch = True

[coverage:report]
show_missing = True
omit = 
    *__init__.py*
    main.py
    example.py
    minevis/__main__.py
    tests/*
    venv/*
    setup.py
```

Run the following command: `pytest --cov=.`.

Alternatively, run `./run_tests.sh`.

