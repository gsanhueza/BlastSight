# MineVis

MineVis is a 3D visualization software designed to aid in Mining research.

## Installation

You can install MineVis with the following command:

`pip install git+https://github.com/gsanhueza/MineVis.git`

## Usage

Implemented in Python 3.7 and qtpy, it's useful as a library and as an application,
so you can use it as a viewer, or integrate it to an application you're developing.

### App Mode

Start the application with `python -m minevis`.

From there you can load elements with File > Load [element].

More information in Help > Help.

### Integrable Mode

Insert the following lines in your code:

```python
from qtpy.QtWidgets import QWidget
from minevis.view.integrableviewer import IntegrableViewer

class EmbeddedViewer(QWidget):
    def __init__(self), parent=None:
        QWidget.__init__(self, parent)
        self.viewer = IntegrableViewer(self)

    # etc...

```

### Viewer Mode (à la matplotlib)

Insert the following lines in your script:

```python
from minevis.view.viewer import Viewer
viewer = Viewer()

# Your code

viewer.show()

```

## Packaging

You need to have `setuptools` and `wheel` installed.

Run the following command to create a pip-installable package:
`python setup.py bdist_wheel`.

Alternatively, run `./wheelbuild.sh`.

Your package will be in `dist`.
You can install it with `pip install dist/minevis*`.

## Testing

Run the following command: `pytest --cov=minevis`.

Alternatively, run `./run_tests.sh`.

