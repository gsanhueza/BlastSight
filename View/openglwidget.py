#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import QPainter
from PySide2.QtGui import QMatrix4x4
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot

from View.meshgl import MeshGL
from View.blockmodelgl import BlockModelGL

from Controller.normalmode import NormalMode

_POSITION = 0
_COLOR = 1


class OpenGLWidget(QOpenGLWidget):
    # FIXME We might not get a model every time.
    # FIXME We need to have a fallback option to only receive vertices
    def __init__(self, parent=None, mode_class=NormalMode, model=None):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        # Controller mode
        self.current_mode = mode_class(self)

        # Model
        self.model = model

        # Drawables
        self.mesh = MeshGL(self, self.model.get_mesh())
        self.block_model = BlockModelGL(self, self.model.get_block_model())

        # Camera/World/Projection
        self.camera = QMatrix4x4()
        self.world = QMatrix4x4()
        self.proj = QMatrix4x4()

        # Camera position
        self.xCamPos = 0.0
        self.yCamPos = 0.0
        self.zCamPos = -3.0

        # World rotation
        self.xRot = 0.0
        self.yRot = 0.0
        self.zRot = 0.0

        # QPainter (after OpenGL)
        self.painter = QPainter()

    def initializeGL(self):
        self.mesh.initialize()
        self.block_model.initialize()

        # Camera setup
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos)

    def paintGL(self):
        self.painter.begin(self)
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow rotation of the world
        self.world.rotate(self.xRot / 16.0, 1, 0, 0)
        self.world.rotate(self.yRot / 16.0, 0, 1, 0)
        self.world.rotate(self.zRot / 16.0, 0, 0, 1)

        # Draw mesh and block model
        self.mesh.draw()
        self.block_model.draw()

        # QPainter can draw *after* OpenGL finishes
        self.painter.end()
        self.current_mode.overpaint()

    def resizeGL(self, w, h):
        # TODO Allow perspective/orthogonal in the controller (mode)
        self.proj.setToIdentity()
        self.proj.perspective(45.0, (w / h), 0.01, 10000.0)

        # ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)
        # scale_factor = -self.zCamPos * 200
        # self.proj.ortho(-w/scale_factor, w/scale_factor, -h/scale_factor, h/scale_factor, 0.01, 10000)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event, *args, **kwargs):
        self.current_mode.mouseMoveEvent(event)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs):
        self.current_mode.mousePressEvent(event)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs):
        self.current_mode.mouseReleaseEvent(event)
        self.update()

    def wheelEvent(self, event, *args, **kwargs):
        self.current_mode.wheelEvent(event)
        self.update()

    @Slot()
    def update_mesh(self):
        self.mesh.setup_vertex_attribs()
        self.update()

    @Slot()
    def update_block_model(self):
        self.block_model.setup_vertex_attribs()
        self.update()

    @Slot()
    def toggle_wireframe(self):
        self.mesh.toggle_wireframe()
        self.update()

    # FIXME Should we (openglwidget) or mainwindow handle this? Should we notify mainwindow of an error?
    def dragEnterEvent(self, event, *args, **kwargs):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs):
        file_path = event.mimeData().urls()[0].toLocalFile()

        # FIXME We should know beforehand if this is a mesh or a block model
        try:
            self.model.get_mesh().load(file_path)
            self.update_mesh()
        except KeyError:
            self.model.get_block_model().load(file_path)
            self.update_block_model()

        # Check if we're part of a MainWindow or a standalone widget
        if self.parent():
            self.parent().statusBar.showMessage('Drop')
