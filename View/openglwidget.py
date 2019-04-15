#!/usr/bin/env python

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import QPainter
from PySide2.QtGui import QMatrix4x4
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot

from View.meshgl import MeshGL
from View.gldrawablecollection import GLDrawableCollection
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
        self.mesh_collection = GLDrawableCollection()
        self.block_model_collection = GLDrawableCollection()
        # self.mesh = MeshGL(self, self.model.get_mesh())
        # self.block_model = BlockModelGL(self, self.model.get_block_model())

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
        self.mesh_collection.draw()
        self.block_model_collection.draw()

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
        self.mesh_collection.clear()
        for mesh in self.model.get_meshes():
            mesh_gl = MeshGL(self, mesh)
            self.mesh_collection.add(mesh_gl)

    @Slot()
    def update_block_model(self):
        block_model = self.model.get_block_model()
        block_model_gl = BlockModelGL(self, block_model)
        self.block_model_collection.add(block_model_gl)

    @Slot()
    def toggle_wireframe(self):
        _id = self.model.mesh_last_identifier
        mesh = self.mesh_collection[_id - 1]
        mesh.toggle_wireframe()

        self.update()

    def dragEnterEvent(self, event, *args, **kwargs):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs):
        file_path = event.mimeData().urls()[0].toLocalFile()

        # FIXME We should know beforehand if this is a mesh or a block model
        try:
            _id = self.model.add_mesh(file_path)
            self.update_mesh()
        except KeyError:
            self.model.add_block_model(file_path)
            self.update_block_model()

        # Check if we're part of a MainWindow or a standalone widget
        if self.parent():
            self.parent().statusBar.showMessage('Drop')

        # Update
        self.update()

    def set_camera_pos(self, x, y, z):
        self.xCamPos = x
        self.yCamPos = y
        self.zCamPos = z
