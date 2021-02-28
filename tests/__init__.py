#!/usr/bin/env python

import sys
from qtpy.QtWidgets import QApplication

from blastsight.view.integrableviewer import IntegrableViewer

app = QApplication(sys.argv)

# Needed to create OpenGLWidget.context() before running tests that use OpenGL
viewer = IntegrableViewer()
viewer.show()
viewer.hide()
