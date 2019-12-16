# BlastSight

BlastSight is a 3D visualization software designed to aid in Mining research.

![blastsight](https://users.dcc.uchile.cl/~gsanhuez/blastsight_app.png)

## Installation

You can install BlastSight with the following command:

`pip install git+https://github.com/gsanhueza/BlastSight.git`

## Usage

Implemented in Python 3.7 and qtpy, it's useful as a library and as an application,
so you can use it as a viewer, or integrate it to an application you're developing.

### Application Mode

Start the application with `python -m blastsight`.

From there you can load elements with File > Load [element].

More information in Help > Help.

### Integrable Mode

You can embed BlastSight's viewer within your application.

Check the following code and adapt it to your needs.

```python
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QGridLayout
from blastsight.view.integrableviewer import IntegrableViewer


class EmbeddedViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('EmbeddedViewer')
        self.resize(800, 600)
        self.viewer = IntegrableViewer(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.viewer, 0, 0, 1, 1)


if __name__ == '__main__':
    app = QApplication([])
    embedded = EmbeddedViewer()
    embedded.show()
    app.exec_()
```

### Viewer Mode

You can also use BlastSight as a simple viewer when you write your own script.

Insert the following lines in your script:

```python
from blastsight.view.viewer import Viewer
viewer = Viewer()

# Your code

viewer.show()
```

## Examples

BlastSight comes with a folder of examples that show what you can do with it.

It's recommended to check `examples/demo.py` in https://github.com/gsanhueza/BlastSight/
to develop an idea of how to use this software.

## Packaging

You need to have `setuptools` and `wheel` installed.

Run the following command to create a pip-installable package:
`python setup.py bdist_wheel`.

Alternatively, run `./wheelbuild.sh`.

Your package will be in `dist`.
You can install it with `pip install dist/blastsight*`.

## Testing

Run the following command: `pytest --cov=blastsight`.

Alternatively, run `./run_tests.sh`.

