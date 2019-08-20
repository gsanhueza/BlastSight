# MineVis

MineVis is a 3D visualization software designed to aid in Mining research.

## Packaging

You need to have `setuptools` and `wheel` installed.

Run the following command to create a pip-installable package:
`python setup.py bdist_wheel`.

Alternatively, run `./build_wheel.sh`.

Your package will be in `dist`.
You can install it with `pip install dist/minevis*`.

## Testing

Run the following command: `pytest --cov=minevis`.

Alternatively, run `./run_tests.sh`.

