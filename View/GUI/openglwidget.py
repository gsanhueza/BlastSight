#!/usr/bin/env python

import traceback

from OpenGL.GL import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QMatrix4x4

from View.Drawables.drawablecollection import GLDrawableCollection
from View.Drawables.gldrawable import GLDrawable
from View.Drawables.blockmodelgl import BlockModelGL
from View.Drawables.meshgl import MeshGL
from View.fpscounter import FPSCounter

from Controller.normalmode import NormalMode
from Controller.drawmode import DrawMode
from Controller.freemode import FreeMode

from Model.model import Model
from Model.Elements.element import Element


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, model=Model()):
        QOpenGLWidget.__init__(self, parent)

        # Controller mode
        self.current_mode = None

        # Model
        self.model = model

        # Drawable elements
        self.drawable_collection = GLDrawableCollection()

        # Camera/World/Projection
        self.camera = QMatrix4x4()
        self.world = QMatrix4x4()
        self.proj = QMatrix4x4()

        # World (we don't move the camera)
        self.xWorldPos = 0.0
        self.yWorldPos = 0.0
        self.zWorldPos = -3.0

        self.xWorldRot = 0.0
        self.yWorldRot = 0.0
        self.zWorldRot = 0.0

        # Centroid (objects will rotate around this)
        self.xCentroid = 0.0
        self.yCentroid = 0.0
        self.zCentroid = 0.0

        # QPainter (after OpenGL)
        self.painter = QPainter()

        # Controller
        self.set_normal_mode()

        # FPS Counter
        self.fps_counter = FPSCounter()

    """
    FACADE METHODS
    """
    # FIXME We changed the way the model handles new data
    def add_drawable(self, element: Element, drawable_type: type):
        id_ = element.id

        drawable = drawable_type(self, element)
        self.drawable_collection.add(id_, drawable)

        if element.centroid.size > 0:
            self.set_centroid(list(element.centroid))

        return id_

    def add_mesh(self, file_path: str) -> int:
        try:
            element = self.model.mesh_by_path(file_path)
            return self.add_drawable(element, MeshGL)
        except Exception:
            traceback.print_exc()
            return -1

    def add_block_model(self, file_path: str) -> int:
        try:
            element = self.model.block_model_by_path(file_path)
            return self.add_drawable(element, BlockModelGL)
        except Exception:
            traceback.print_exc()
            return -1

    def show_element(self, id_: int) -> None:
        self.drawable_collection[id_].show()

    def hide_element(self, id_: int) -> None:
        self.drawable_collection[id_].hide()

    def delete_element(self, id_: int) -> None:
        self.model.delete(id_)
        del self.drawable_collection[id_]

    def get_element(self, id_: int) -> None:
        return self.drawable_collection[id_]

    def toggle_wireframe(self, id_: int) -> bool:
        status = self.drawable_collection[id_].toggle_wireframe()
        self.update()

        return status

    def get_gl_collection(self) -> GLDrawableCollection:
        return self.drawable_collection.items()

    def set_world_position(self, x: float, y: float, z: float) -> None:
        self.xWorldPos = -x
        self.yWorldPos = -y
        self.zWorldPos = -z

    def set_centroid(self, centroid: list) -> None:
        self.xCentroid = -centroid[0]
        self.yCentroid = -centroid[1]
        self.zCentroid = -centroid[2]

    """
    Controller modes
    """
    def set_normal_mode(self) -> None:
        self.current_mode = NormalMode(self)

    def set_draw_mode(self) -> None:
        self.current_mode = DrawMode(self)

    def set_free_mode(self) -> None:
        self.current_mode = FreeMode(self)

    """
    Internal methods
    """
    def set_model(self, model: Model) -> None:
        self.model = model

    def initializeGL(self) -> None:
        # Meshes currently in model
        for id_, mesh in self.model.mesh_collection:
            drawable = MeshGL(self, mesh)
            self.drawable_collection.add(id_, drawable)

        # Block models currently in model
        for id_, block_model in self.model.block_model_collection:
            drawable = BlockModelGL(self, block_model)
            self.drawable_collection.add(id_, drawable)

    def paintGL(self) -> None:
        self.painter.begin(self)
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow translation of the world
        self.world.translate(self.xWorldPos,
                             self.yWorldPos,
                             self.zWorldPos)

        # Allow rotation of the world
        self.world.rotate(self.xWorldRot / 16.0, 1, 0, 0)
        self.world.rotate(self.yWorldRot / 16.0, 0, 1, 0)
        self.world.rotate(self.zWorldRot / 16.0, 0, 0, 1)

        # Translate by centroid
        self.world.translate(self.xCentroid,
                             self.yCentroid,
                             self.zCentroid)

        # Draw every GLDrawable (meshes, block models, etc)
        self.drawable_collection.draw(self.proj, self.camera, self.world)

        # QPainter can draw *after* OpenGL finishes
        self.painter.end()
        self.current_mode.overpaint()

        self.fps_counter.tick()

    def resizeGL(self, w: float, h: float) -> None:
        # TODO Allow perspective/orthogonal in the controller (mode)
        self.proj.setToIdentity()
        self.proj.perspective(45.0, (w / h), 0.01, 10000.0)

        # ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)
        # scale_factor = self.zWorldPos * 200
        # self.proj.ortho(-w/scale_factor, w/scale_factor, -h/scale_factor, h/scale_factor, 0.01, 10000)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseReleaseEvent(event)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.wheelEvent(event)
        self.update()
