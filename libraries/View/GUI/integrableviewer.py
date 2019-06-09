#!/usr/bin/env python

import numpy as np
import traceback

from OpenGL.GL import *
from qtpy.QtCore import QRect, Signal
from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtGui import QPainter
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QVector3D

from ..Drawables.gldrawablecollection import GLDrawableCollection
from ..Drawables.gldrawable import GLDrawable

from ..Drawables.blockmodelgl import BlockModelGL
from ..Drawables.meshgl import MeshGL
from ..Drawables.linegl import LineGL
from ..Drawables.tubegl import TubeGL
from ..Drawables.backgroundgl import BackgroundGL

from ..fpscounter import FPSCounter

from ...Controller.normalmode import NormalMode
from ...Controller.drawmode import DrawMode
from ...Controller.selectionmode import SelectionMode

from ...Model.Elements.element import Element
from ...Model.model import Model
from ...Model.utils import mesh_intersection


class IntegrableViewer(QOpenGLWidget):
    # Signals
    file_dropped_signal = Signal()

    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self._model = Model()
        # Controller mode
        self.current_mode = None

        # Drawable elements
        self.background = BackgroundGL(self, True)
        self.drawable_collection = GLDrawableCollection()

        # Camera/World/Projection
        self._camera = QMatrix4x4()
        self._world = QMatrix4x4()
        self._proj = QMatrix4x4()

        # World (we don't move the camera)
        self._initial_position = [0.0, 0.0, -3.0]
        self._initial_rotation = [0.0, 0.0, 0.0]

        self.xWorldPos, self.yWorldPos, self.zWorldPos = self._initial_position
        self.xWorldRot, self.yWorldRot, self.zWorldRot = self._initial_rotation

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
    def camera(self):
        return self._camera

    @property
    def world(self):
        return self._world

    @property
    def proj(self):
        return self._proj

    @property
    def centroid(self) -> list:
        return [self.xCentroid, self.yCentroid, self.zCentroid]

    @centroid.setter
    def centroid(self, centroid: list) -> None:
        self.xCentroid, self.yCentroid, self.zCentroid = centroid

    @property
    def camera_position(self) -> list:
        return [-self.xWorldPos, -self.yWorldPos, -self.zWorldPos]

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xWorldPos, self.yWorldPos, self.zWorldPos = [-pos[0], -pos[1], -pos[2]]

    @property
    def camera_rotation(self) -> list:
        return [self.xWorldRot, self.yWorldRot, self.zWorldRot]

    @camera_rotation.setter
    def camera_rotation(self, rot: list) -> None:
        self.xWorldRot, self.yWorldRot, self.zWorldRot = [rot[0], rot[1], rot[2]]

    @property
    def last_id(self) -> int:
        return list(self.drawable_collection.keys())[-1]

    """
    Load methods
    """
    def add_drawable(self, element: Element, drawable_type: type) -> GLDrawable:
        drawable = drawable_type(self, element)
        self.drawable_collection.add(drawable.id, drawable)

        self.file_dropped_signal.emit()
        self.update()

        return drawable

    def mesh(self, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.mesh(*args, **kwargs)
            return self.add_drawable(element, MeshGL)
        except Exception:
            traceback.print_exc()
            return None

    def mesh_by_path(self, file_path, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.mesh_by_path(file_path, *args, **kwargs)
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

    def lines(self, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.lines(*args, **kwargs)
            return self.add_drawable(element, LineGL)
        except Exception:
            traceback.print_exc()
            return None

    def tubes(self, *args, **kwargs) -> GLDrawable:
        try:
            element = self.model.tubes(*args, **kwargs)
            return self.add_drawable(element, TubeGL)
        except Exception:
            traceback.print_exc()
            return None

    """
    Individual drawable manipulation
    """
    def show_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].show()

    def hide_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].hide()

    def get_drawable(self, id_: int) -> GLDrawable:
        return self.drawable_collection[id_]

    def update_drawable(self, id_: int) -> None:
        self.centroid = self.model.get(id_).centroid
        self.get_drawable(id_).setup_attributes()

    def delete(self, id_: int) -> None:
        self.model.delete(id_)
        del self.drawable_collection[id_]

    def camera_at(self, id_: int) -> None:
        drawable = self.get_drawable(id_)
        self.xWorldPos, self.yWorldPos, self.zWorldPos = self._initial_position
        self.centroid = drawable.element.centroid
        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.background.initialize()

    def paintGL(self) -> None:
        self.painter.begin(self)

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow translation of the world
        self.world.translate(self.xWorldPos,
                             self.yWorldPos,
                             self.zWorldPos)

        # Allow rotation of the world
        self.world.rotate(self.xWorldRot, 1.0, 0.0, 0.0)
        self.world.rotate(self.yWorldRot, 0.0, 1.0, 0.0)
        self.world.rotate(self.zWorldRot, 0.0, 0.0, 1.0)

        # Translate by centroid
        self.world.translate(-self.xCentroid,
                             -self.yCentroid,
                             -self.zCentroid)

        # Draw gradient background
        glDisable(GL_DEPTH_TEST)
        self.background.draw()
        glEnable(GL_DEPTH_TEST)

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

    """
    Utilities
    """
    def detect_intersection(self, x: float, y: float, z: float) -> None:
        # For more info, read http://antongerdelan.net/opengl/raycasting.html
        y = self.height() - y  # Qt's y() to OpenGL's y()

        ray = QVector3D(x, y, z).unproject((self.camera * self.world), self.proj,
                                           QRect(0, 0, self.width(), self.height())).normalized()

        camera_pos = self.camera.column(3)
        ray_origin = ((self.camera * self.world).inverted()[0] * camera_pos).toVector3D()

        # To Numpy array
        ray = np.array([ray.x(), ray.y(), ray.z()])
        ray_origin = np.array([ray_origin.x(), ray_origin.y(), ray_origin.z()])

        for mesh in self.model.mesh_collection:
            print(f'(Mesh {mesh.id}) Intersects: {mesh_intersection(ray_origin, ray, mesh)}')
        print('-------------------------------')

    """
    Controller
    """
    def set_normal_mode(self) -> None:
        self.current_mode = NormalMode(self)

    def set_draw_mode(self) -> None:
        self.current_mode = DrawMode(self)

    def set_selection_mode(self) -> None:
        self.current_mode = SelectionMode(self)

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

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()

            # Brute-force trying to load
            self.mesh_by_path(file_path)
            self.block_model_by_path(file_path)
