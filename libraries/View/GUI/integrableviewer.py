#!/usr/bin/env python

import math
import numpy as np
import traceback

from OpenGL.GL import *
from qtpy.QtCore import Signal, QPoint
from qtpy.QtCore import QFileInfo, QDirIterator
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QOpenGLWidget
from qtpy.QtGui import QRegion, QPixmap
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D

from ..Drawables.gldrawablecollection import GLDrawableCollection

from ..Drawables.blockmodelgl import BlockModelGL
from ..Drawables.meshgl import MeshGL
from ..Drawables.pointgl import PointGL
from ..Drawables.linegl import LineGL
from ..Drawables.tubegl import TubeGL
from ..Drawables.backgroundgl import BackgroundGL
from ..Drawables.axisgl import AxisGL

from ..fpscounter import FPSCounter

from ...Controller.normalmode import NormalMode
from ...Controller.selectionmode import SelectionMode

from ...Model.model import Model
from ...Model.utils import mesh_intersection


class IntegrableViewer(QOpenGLWidget):
    # Signals
    file_modified_signal = Signal()
    fps_signal = Signal(float)

    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self._model = Model()
        # Controller mode
        self.current_mode = None
        self.set_normal_mode()

        # Drawable elements
        self.drawable_collection = GLDrawableCollection(self)

        self.drawable_collection.add(BackgroundGL(self, type('NullElement', (), {'id': 'BG'})))
        self.drawable_collection.add(AxisGL(self, type('NullElement', (), {'id': 'AXIS'})))

        # Camera/World/Projection
        self._camera = QMatrix4x4()
        self._world = QMatrix4x4()
        self._proj = QMatrix4x4()

        # Positions and rotations
        self._initial_centroid = [0.0, 0.0, 0.0]
        self._initial_position = [0.0, 0.0, -200.0]
        self._initial_rotation = [0.0, 0.0, 0.0]

        self.xWorldPos, self.yWorldPos, self.zWorldPos = self._initial_centroid
        self.xWorldRot, self.yWorldRot, self.zWorldRot = self._initial_rotation
        self.xCameraPos, self.yCameraPos, self.zCameraPos = self._initial_position

        # FPS Counter
        self.fps_counter = FPSCounter()
        self.fps_signal.connect(self.print_fps)

        # Thread Pool
        self.thread_pool = QThreadPool()

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
        return [-self.xCameraPos, -self.yCameraPos, -self.zCameraPos]

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xCameraPos, self.yCameraPos, self.zCameraPos = -pos[0], -pos[1], -pos[2]

    @property
    def camera_rotation(self) -> list:
        return [self.xWorldRot, self.yWorldRot, self.zWorldRot]

    @camera_rotation.setter
    def camera_rotation(self, rot: list) -> None:
        self.xWorldRot, self.yWorldRot, self.zWorldRot = [rot[0], rot[1], rot[2]]

    @property
    def centroid(self) -> list:
        return [self.xWorldPos, self.yWorldPos, self.zWorldPos]

    @centroid.setter
    def centroid(self, _centroid: list) -> None:
        self.xWorldPos, self.yWorldPos, self.zWorldPos = _centroid

    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    """
    Load methods
    """
    def add_drawable(self, method: classmethod, drawable_type: type, *args, **kwargs):
        try:
            element = method(*args, **kwargs)
            drawable = drawable_type(self, element)
            self.drawable_collection.add(drawable)

            self.file_modified_signal.emit()
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

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh_by_path, MeshGL, path, *args, **kwargs)

    def block_model_by_path(self, path: str, *args, **kwargs) -> BlockModelGL:
        return self.add_drawable(self.model.block_model_by_path, BlockModelGL, path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points_by_path, PointGL, path, *args, **kwargs)

    """
    Individual drawable manipulation
    """
    def show_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].show()
        self.update()

    def hide_drawable(self, id_: int) -> None:
        self.drawable_collection[id_].hide()
        self.update()

    def get_drawable(self, id_: int):
        return self.drawable_collection[id_]

    def update_drawable(self, id_: int) -> None:
        self.xWorldPos, self.yWorldPos, self.zWorldPos = self.model.get(id_).centroid
        self.get_drawable(id_).setup_attributes()
        self.update()

    def delete(self, id_: int) -> None:
        self.model.delete(id_)
        self.drawable_collection.delete(id_)
        self.file_modified_signal.emit()
        self.update()

    def camera_at(self, id_: int) -> None:
        drawable = self.get_drawable(id_)
        self.centroid = drawable.element.centroid
        self.camera_position = drawable.element.centroid

        dx = abs(drawable.element.x.max() - drawable.element.x.min())
        dy = abs(drawable.element.y.max() - drawable.element.y.min())
        dz = abs(drawable.element.z.max() - drawable.element.z.min())

        # Put the camera in a position that allow us to see the element
        self.zCameraPos -= 1.2 * max(dx, dy, dz) / math.tan(math.pi / 4)
        self.update()

    def plan_view(self):
        self.xWorldRot, self.yWorldRot, self.zWorldRot = [0.0, 0.0, 0.0]
        self.update()

    def north_view(self):
        self.xWorldRot, self.yWorldRot, self.zWorldRot = [270.0, 0.0, 270.0]
        self.update()

    def east_view(self):
        self.xWorldRot, self.yWorldRot, self.zWorldRot = [270.0, 0.0, 0.0]
        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_POINT_SPRITE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self) -> None:
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()
        self.camera.setToIdentity()

        # Translate by centroid (world position)
        self.world.translate(self.xWorldPos, self.yWorldPos, self.zWorldPos)

        # Allow rotation of the world
        self.world.rotate(self.xWorldRot, 1.0, 0.0, 0.0)
        self.world.rotate(self.yWorldRot, 0.0, 1.0, 0.0)
        self.world.rotate(self.zWorldRot, 0.0, 0.0, 1.0)

        # Restore world
        self.world.translate(-self.xWorldPos, -self.yWorldPos, -self.zWorldPos)

        # Translate the camera
        self.camera.translate(self.xCameraPos, self.yCameraPos, self.zCameraPos)
        # Draw every GLDrawable (meshes, block models, etc)
        glEnable(GL_BLEND)
        self.drawable_collection.draw(self.proj, self.camera, self.world)

        # QPainter can draw *after* OpenGL finishes
        self.current_mode.overpaint(self)

        self.fps_counter.tick()
        self.fps_signal.emit(self.fps_counter.fps)

    def resizeGL(self, w: float, h: float) -> None:
        self.proj.setToIdentity()
        perspective = True  # TODO Switch perspective/orthogonal in application

        if perspective:
            self.proj.perspective(45.0, (w / h), 1.0, 10000.0)
        else:
            w = w * (abs(self.zWorldPos) - abs(self.zCameraPos)) * -0.001
            h = h * (abs(self.zWorldPos) - abs(self.zCameraPos)) * -0.001
            self.proj.ortho(-w, w, -h, h, 1.0, 10000.0)

    """
    Utilities
    """
    @staticmethod
    def print_fps(fps):
        print(f'               \r', end='')
        print(f'FPS: {fps:.1f}\r', end='')

    def unproject(self, _x, _y, _z, model, view, proj) -> QVector3D:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        x = (2.0 * _x / self.width()) - 1.0
        y = 1.0 - (2.0 * _y / self.height())

        ray_eye = proj.inverted()[0] * QVector4D(x, y, -1.0, 1.0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        ray_world = ((view * model).inverted()[0] * ray_eye).toVector3D()
        return ray_world.normalized()

    def detect_intersection(self, x: float, y: float, z: float) -> None:
        ray = self.unproject(x, y, z, self.world, self.camera, self.proj)
        ray_origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()

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
        self.current_mode = NormalMode()
        self.update()

    def set_selection_mode(self) -> None:
        self.current_mode = SelectionMode()
        self.update()

    def take_screenshot(self):
        save_path = 'minevis_screenshot.png'

        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        pixmap.save(save_path)

        del pixmap

    # Movement/actions dependent on current mode
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event, self)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event, self)
        self.update()

    def mouseReleaseEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseReleaseEvent(event, self)
        self.update()

    def wheelEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.wheelEvent(event, self)
        self.update()

    def dragEnterEvent(self, event, *args, **kwargs) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event, *args, **kwargs) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            if QFileInfo(path).isDir():
                self._load_as_dir(path)
            else:
                self.mesh_by_path(path)

    def _load_as_dir(self, path):
        it = QDirIterator(path, QDirIterator.Subdirectories)
        while it.hasNext():
            self.mesh_by_path(it.next())
