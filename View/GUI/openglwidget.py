#!/usr/bin/env python

import traceback

from OpenGL.GL import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QMatrix4x4

from View.Drawables.drawablecollection import GLDrawableCollection
from View.Drawables.blockmodelgl import BlockModelGL
from View.Drawables.meshgl import MeshGL
from View.Drawables.gldrawable import GLDrawable
from View.fpscounter import FPSCounter

from Controller.normalmode import NormalMode
from Controller.drawmode import DrawMode
from Controller.freemode import FreeMode

from Model.Elements.element import Element
from Model.model import Model


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)

        self._model = Model()
        # Controller mode
        self.current_mode = None

        # Drawable elements
        self._drawable_collection = GLDrawableCollection()

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

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def drawable_collection(self):
        return self._drawable_collection

    """
    FACADE METHODS
    """
    def add_drawable(self, element: Element, drawable_type: type) -> GLDrawable:
        id_ = element.id

        drawable = drawable_type(self, element)
        drawable.id = id_
        self.drawable_collection.add(id_, drawable)

        return drawable

    def mesh(self, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.mesh(*args, **kwargs)
            self.set_centroid(element.centroid)
            return self.add_drawable(element, MeshGL)
        except Exception:
            traceback.print_exc()
            return None

    def mesh_by_path(self, file_path: str) -> GLDrawable:
        try:
            element = self.model.mesh_by_path(file_path)
            self.set_centroid(element.centroid)
            return self.add_drawable(element, MeshGL)
        except Exception:
            traceback.print_exc()
            return None

    def block_model(self, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.block_model(*args, **kwargs)
            return self.add_drawable(element, BlockModelGL)
        except Exception:
            traceback.print_exc()
            return None

    def block_model_by_path(self, file_path: str) -> GLDrawable:
        try:
            element = self.model.block_model_by_path(file_path)
            return self.add_drawable(element, BlockModelGL)
        except Exception:
            traceback.print_exc()
            return None

    def show_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].show()

    def hide_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].hide()

    def get_drawable(self, id_: int) -> None:
        return self.drawable_collection[id_]

    def update_drawable(self, id_: int) -> None:
        self.set_centroid(self.model.get(id_).centroid)
        self.get_drawable(id_).setup_vertex_attribs()

    def delete(self, id_: int) -> None:
        self.model.delete(id_)
        del self.drawable_collection[id_]

    def toggle_wireframe(self, id_: int) -> bool:
        status = self.drawable_collection[id_].toggle_wireframe()
        self.update()

        return status

    def set_world_position(self, x: float, y: float, z: float) -> None:
        self.xWorldPos = -x
        self.yWorldPos = -y
        self.zWorldPos = -z

    def set_centroid(self, centroid) -> None:
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

    def initializeGL(self) -> None:
        # Standalone viewer will put items here before "show()"
        # FIXME Wrong initialization, doesn't set toggled wireframe
        for id_, drawable in self.drawable_collection.items():
            drawable.initialize()

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
