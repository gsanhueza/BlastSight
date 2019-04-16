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
from Controller.drawmode import DrawMode
from Controller.freemode import FreeMode

from Model.model import Model

_POSITION = 0
_COLOR = 1


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, model=Model()):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        # Controller mode
        self.current_mode = None

        # Model
        self.model = model

        # Drawable elements
        self.mesh_gl_collection = GLDrawableCollection()
        self.block_model_gl_collection = GLDrawableCollection()

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

        self.set_normal_mode()

    """
    FACADE METHODS
    """
    def add_mesh(self, file_path: str) -> bool:
        id_ = self.model.add_mesh(file_path)
        mesh = self.model.get_mesh(id_)
        mesh_gl = MeshGL(self, mesh)
        self.mesh_gl_collection.add(id_, mesh_gl)

        return True

    def update_mesh(self, id_: int) -> None:
        mesh = self.model.get_mesh(id_)
        mesh_gl = MeshGL(self, mesh)
        self.mesh_gl_collection[id_] = mesh_gl

    def show_mesh(self, id_: int) -> None:
        self.mesh_gl_collection[id_].show()

    def hide_mesh(self, id_: int) -> None:
        self.mesh_gl_collection[id_].hide()

    def delete_mesh(self, id_: int) -> None:
        # FIXME Maybe we can only delete the GLDrawable (and in the "destructor" call self.model.delete_mesh())
        self.model.delete_mesh(id_)
        self.mesh_gl_collection[id_] = None

    def add_block_model(self, file_path: str) -> bool:
        id_ = self.model.add_block_model(file_path)
        block_model = self.model.get_block_model(id_)
        block_model_gl = BlockModelGL(self, block_model)
        self.block_model_gl_collection.add(id_, block_model_gl)

        return True

    def delete_block_model(self, id_: int) -> None:
        self.model.delete_block_model(id_)
        self.block_model_gl_collection[id_] = None

    @Slot()
    def toggle_wireframe(self, id_: int) -> bool:
        status = self.mesh_gl_collection[id_].toggle_wireframe()
        self.update()

        return status

    def set_camera_position(self, x: float, y: float, z: float) -> None:
        self.xCamPos = x
        self.yCamPos = y
        self.zCamPos = z

    """
    Controller modes
    """
    @Slot()
    def set_normal_mode(self):
        self.current_mode = NormalMode(self)

    @Slot()
    def set_draw_mode(self):
        self.current_mode = DrawMode(self)

    @Slot()
    def set_free_mode(self):
        self.current_mode = FreeMode(self)

    """
    Internal methods
    """
    def initializeGL(self):
        # Meshes currently in model
        for id_, mesh in self.model.get_mesh_collection():
            mesh_gl = MeshGL(self, mesh)
            self.mesh_gl_collection.add(id_, mesh_gl)

        # Block models currently in model
        for id_, block_model in self.model.get_block_model_collection():
            block_model_gl = BlockModelGL(self, block_model)
            self.block_model_gl_collection.add(id_, block_model_gl)

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
        self.mesh_gl_collection.draw()
        self.block_model_gl_collection.draw()

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

    def dragEnterEvent(self, event, *args, **kwargs):
        if event.mimeData().hasFormat('text/plain'):
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs):
        file_path = event.mimeData().urls()[0].toLocalFile()

        # FIXME We should know beforehand if this is a mesh or a block model
        try:
            self.add_mesh(file_path)
        except KeyError:
            self.add_block_model(file_path)

        # Check if we're part of a MainWindow or a standalone widget
        if self.parent():
            self.parent().statusBar.showMessage('Drop')

        # Update
        self.update()
