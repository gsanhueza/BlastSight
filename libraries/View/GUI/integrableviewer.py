#!/usr/bin/env python

import math
import numpy as np
import traceback

from OpenGL.GL import *
from qtpy.QtCore import QRect, Signal
from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtGui import QPainter
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D

from ..Drawables.gldrawablecollection import GLDrawableCollection
from ..Drawables.gldrawable import GLDrawable

from ..Drawables.blockmodelgl import BlockModelGL
from ..Drawables.meshgl import MeshGL
from ..Drawables.pointgl import PointGL
from ..Drawables.linegl import LineGL
from ..Drawables.tubegl import TubeGL
from ..Drawables.backgroundgl import BackgroundGL
from ..Drawables.backgroundprogram import BackgroundProgram

from ..fpscounter import FPSCounter

from ...Controller.normalmode import NormalMode
from ...Controller.drawmode import DrawMode
from ...Controller.selectionmode import SelectionMode

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
        self.set_normal_mode()

        # Drawable elements
        self.background = BackgroundGL(self, True)
        self.background_program = BackgroundProgram(self)
        self.drawable_collection = GLDrawableCollection(self)

        # Camera/World/Projection
        self._camera = QMatrix4x4()
        self._world = QMatrix4x4()
        self._proj = QMatrix4x4()

        # World (we don't move the camera)
        self._initial_position = [0.0, 0.0, -200.0]
        self._initial_rotation = [0.0, 0.0, 0.0]

        self.xWorldPos, self.yWorldPos, self.zWorldPos = self._initial_position
        self.xWorldRot, self.yWorldRot, self.zWorldRot = self._initial_rotation

        # Centroid (objects will rotate around this)
        self._initial_centroid = [0.0, 0.0, 0.0]
        self.xCentroid, self.yCentroid, self.zCentroid = self._initial_centroid

        # QPainter (after OpenGL)
        self.painter = QPainter()

        # FPS Counter
        self.fps_counter = FPSCounter()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, _model):
        self._model = _model

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
    def centroid(self) -> list:
        return [self.xCentroid, self.yCentroid, self.zCentroid]

    @centroid.setter
    def centroid(self, _centroid: list) -> None:
        self.xCentroid, self.yCentroid, self.zCentroid = _centroid

    @property
    def last_id(self) -> int:
        try:
            return list(self.drawable_collection.keys())[-1]
        except IndexError:
            return -1

    """
    Load methods
    """
    def add_drawable(self, method: classmethod, drawable: type, *args, **kwargs):
        try:
            element = method(*args, **kwargs)
            drawable = drawable(self, element)
            self.drawable_collection.add(drawable.id, drawable)

            self.file_dropped_signal.emit()
            self.update()

            return drawable
        except Exception:
            traceback.print_exc()
            return None

    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh, MeshGL, *args, **kwargs)

    def block_model(self, *args, **kwargs) -> BlockModelGL:
        return self.add_drawable(self.model.block_model, BlockModelGL, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points, PointGL, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineGL:
        return self.add_drawable(self.model.lines, LineGL, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.add_drawable(self.model.tubes, TubeGL, *args, **kwargs)

    def mesh_by_path(self, file_path: str, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh_by_path, MeshGL, file_path, *args, **kwargs)

    def block_model_by_path(self, file_path: str, *args, **kwargs) -> BlockModelGL:
        return self.add_drawable(self.model.block_model_by_path, BlockModelGL, file_path, *args, **kwargs)

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
        self.xCentroid, self.yCentroid, self.zCentroid = self.model.get(id_).centroid
        self.get_drawable(id_).setup_attributes()

    def delete(self, id_: int) -> None:
        self.model.delete(id_)
        del self.drawable_collection[id_]

    def camera_at(self, id_: int) -> None:
        drawable = self.get_drawable(id_)
        self.xWorldPos, self.yWorldPos, self.zWorldPos = self._initial_position
        self.xCentroid, self.yCentroid, self.zCentroid = drawable.element.centroid

        dx = abs(drawable.element.x.max() - drawable.element.x.min())
        dy = abs(drawable.element.y.max() - drawable.element.y.min())
        dz = abs(drawable.element.z.max() - drawable.element.z.min())

        # Put the camera in a position that allow us to see it
        self.zWorldPos = -1.2 * max(dx, dy, dz) / math.tan(math.pi / 4)
        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.background_program.setup()
        self.background_program.bind()
        self.background_program.update_uniform('top_color', QVector4D(30, 47, 73, 255) / 255)
        self.background_program.update_uniform('bot_color', QVector4D(109, 126, 146, 255) / 255)

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
        self.background_program.bind()
        self.background.draw()
        glEnable(GL_DEPTH_TEST)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

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

        ## ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)
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

    # Movement/actions dependent on current mode
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
