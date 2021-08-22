# BlastSight

BlastSight is a 3D visualization software designed to aid in Mining research.

![blastsight](https://users.dcc.uchile.cl/~gsanhuez/blastsight_app.png)

## Installation

You can install BlastSight with the following command:

`pip install blastsight`

BlastSight requires the Python implementation of Qt5, and uses
`qtpy` to abstract backends.

You can install a backend yourself, or use one of the following commands
to automatically install one for you:

- `pip install blastsight[pyqt5]` for the PyQt5 backend.
- `pip install blastsight[pyside2]` for the PySide2 backend.

Both should work, but if you find errors using one backend, try with the other!
You can read the documentation from [qtpy](https://github.com/spyder-ide/qtpy)
for more information.

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

## Basic API

The following methods can be used to render your elements directly.
Keep in mind that these methods receive their arguments as *kwargs*, they're not positional.

```python
# Mesh
viewer.mesh(x: list, y: list, z: list, indices: list, color: list, alpha: float, wireframe: bool, highlight: bool)

# Blocks
viewer.blocks(x: list, y: list, z: list, block_size: list, values: list, vmin: float, vmax: float, colormap: str)

# Points
viewer.points(x: list, y: list, z: list, point_size: float, values: list, vmin: float, vmax: float, colormap: str)

# Lines
viewer.lines(x: list, y: list, z: list, color: list, loop: bool)

# Tubes
viewer.tubes(x: list, y: list, z: list, color: list, loop: bool, radius: float, resolution: int)
```

Notes:

* An additional 'name' *kwargs* can be used to give each element a name.
* For **every** element, you can replace (x, y, z) with *vertices*, which is a list
of positions, where each position is a list of (x, y, z).
* For **meshes**, the *indices* argument is a list of index, where index is a list of
(i1, i2, i3).
* For **blocks** and **points** you can replace (values, vmin, vmax) with *color*,
which is a list of colors for each position, where each color is a list of (r, g, b),
between 0.0 and 1.0.

## Examples

BlastSight comes with a folder of examples that show what you can do with it.

It's recommended to check `examples/demo.py` in https://github.com/gsanhueza/BlastSight/
to develop an idea of how to use this software.
