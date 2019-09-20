#!/usr/bin/env python

import math
import numpy as np
import traceback

from datetime import datetime
from OpenGL.GL import *

from qtpy.QtCore import QPoint
from qtpy.QtCore import Signal
from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector3D
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget

from ..drawables.glconstantcollection import GLConstantCollection
from ..drawables.gldrawablecollection import GLDrawableCollection

from ..drawables.axisgl import AxisGL
from ..drawables.backgroundgl import BackgroundGL
from ..drawables.blockgl import BlockGL
from ..drawables.linegl import LineGL
from ..drawables.meshgl import MeshGL
from ..drawables.pointgl import PointGL
from ..drawables.tubegl import TubeGL

from ..fpscounter import FPSCounter

from ...controller.detectionmode import DetectionMode
from ...controller.normalmode import NormalMode
from ...controller.slicemode import SliceMode

from ...model import utils
from ...model.model import Model
from ...model.elements.nullelement import NullElement


class IntegrableViewer(QOpenGLWidget):
    # Signals
    file_modified_signal = Signal()
    fps_signal = Signal(float)
    mesh_clicked_signal = Signal(object)

    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        self._model = Model()
        # Controller mode
        self.current_mode = None
        self.set_normal_mode()

        # Drawable elements
        self.constant_collection = GLConstantCollection(self)
        self.drawable_collection = GLDrawableCollection(self)

        self.constant_collection.add(BackgroundGL(NullElement(id='BG')))
        self.constant_collection.add(AxisGL(NullElement(id='AXIS')))

        # Camera/World/Projection
        self._camera = QMatrix4x4()
        self._world = QMatrix4x4()
        self._proj = QMatrix4x4()

        # Initial positions and rotations
        self.rotation_center = [0.0, 0.0, 0.0]
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.camera_position = [0.0, 0.0, 200.0]

        # FPS Counter
        self.fps_counter = FPSCounter()
        self.fps_signal.connect(self.print_fps)

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
    def camera_position(self) -> np.ndarray:
        return np.array([self.xCameraPos, self.yCameraPos, self.zCameraPos])

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xCameraPos, self.yCameraPos, self.zCameraPos = pos

    @property
    def rotation_angle(self) -> np.ndarray:
        return np.array([self.xCenterRot, self.yCenterRot, self.zCenterRot])

    @rotation_angle.setter
    def rotation_angle(self, rot: list) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = rot

    @property
    def rotation_center(self) -> np.ndarray:
        return np.array([self.xCenterPos, self.yCenterPos, self.zCenterPos])

    @rotation_center.setter
    def rotation_center(self, _center: list) -> None:
        self.xCenterPos, self.yCenterPos, self.zCenterPos = _center

    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    """
    Load methods
    """
    def add_drawable(self, method: classmethod, drawable_type: type, *args, **kwargs):
        try:
            element = method(*args, **kwargs)
            drawable = drawable_type(element, *args, **kwargs)
            self.drawable_collection.add(drawable)

            self.file_modified_signal.emit()
            self.update()

            return drawable
        except Exception:
            traceback.print_exc()
            return None

    def mesh(self, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh, MeshGL, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self.add_drawable(self.model.blocks, BlockGL, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points, PointGL, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineGL:
        return self.add_drawable(self.model.lines, LineGL, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self.add_drawable(self.model.tubes, TubeGL, *args, **kwargs)

    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        return self.add_drawable(self.model.mesh_by_path, MeshGL, path, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockGL:
        return self.add_drawable(self.model.blocks_by_path, BlockGL, path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        return self.add_drawable(self.model.points_by_path, PointGL, path, *args, **kwargs)

    """
    Export methods
    """
    def export_mesh(self, path, id_):
        self.model.export_mesh(path, id_)

    def export_blocks(self, path, id_):
        self.model.export_blocks(path, id_)

    def export_points(self, path, id_):
        self.model.export_points(path, id_)

    """
    Individual drawable manipulation
    """
    def show_drawable(self, id_: int) -> None:
        self.get_drawable(id_).show()
        self.update()

    def hide_drawable(self, id_: int) -> None:
        self.get_drawable(id_).hide()
        self.update()

    def get_drawable(self, id_: int):
        return self.drawable_collection[id_]

    def update_drawable(self, id_: int) -> None:
        self.makeCurrent()
        self.get_drawable(id_).setup_attributes()
        self.update()

    def delete(self, id_: int) -> None:
        self.makeCurrent()
        self.model.delete(id_)
        self.drawable_collection.delete(id_)
        self.file_modified_signal.emit()
        self.update()

    def clear(self):
        for id_ in list(self.drawable_collection.keys()):
            self.delete(id_)

    def camera_at(self, id_: int) -> None:
        drawable = self.get_drawable(id_)
        self.rotation_center = drawable.element.center
        self.camera_position = drawable.element.center

        # Put the camera in a position that allow us to see the element
        max_diff = np.max(np.diff(drawable.element.bounding_box, axis=0))
        self.zCameraPos += 1.2 * max_diff / math.tan(math.pi / 4)

        self.update()

    def plan_view(self):
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [0.0, 0.0, 0.0]
        self.update()

    def north_view(self):
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [270.0, 0.0, 270.0]
        self.update()

    def east_view(self):
        self.xCenterRot, self.yCenterRot, self.zCenterRot = [270.0, 0.0, 0.0]
        self.update()

    def show_all(self):
        if self.last_id == -1:
            return

        min_all = np.inf * np.ones(3)
        max_all = -np.inf * np.ones(3)

        for drawable in self.drawable_collection.values():
            min_bound, max_bound = drawable.element.bounding_box
            min_all = np.min((min_all, min_bound), axis=0)
            max_all = np.max((max_all, max_bound), axis=0)

        center_all = (min_all + max_all) / 2
        self.rotation_center = center_all
        self.camera_position = center_all

        # Put the camera in a position that allow us to see the element
        max_diff = np.max(np.diff([min_all, max_all], axis=0))
        self.zCameraPos += 1.2 * max_diff / math.tan(math.pi / 4)

        self.update()

    """
    Internal methods
    """
    def initializeGL(self) -> None:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_POINT_SPRITE)
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self) -> None:
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.world.setToIdentity()
        self.camera.setToIdentity()

        # Translate by rotation center (world position)
        self.world.translate(*self.rotation_center)

        # Allow rotation of the world
        self.world.rotate(self.xCenterRot, 1.0, 0.0, 0.0)
        self.world.rotate(self.yCenterRot, 0.0, 1.0, 0.0)
        self.world.rotate(self.zCenterRot, 0.0, 0.0, 1.0)

        # Restore world
        self.world.translate(*-self.rotation_center)

        # Translate the camera
        self.camera.translate(*-self.camera_position)

        # Draw every GLDrawable (meshes, block models, etc)
        glEnable(GL_BLEND)
        self.constant_collection.draw(self.proj, self.camera, self.world)
        self.drawable_collection.draw(self.proj, self.camera, self.world)

        # QPainter can draw *after* OpenGL finishes
        self.current_mode.overpaint(self)

        self.fps_counter.tick()
        self.fps_signal.emit(self.fps_counter.fps)

    def resizeGL(self, w: float, h: float) -> None:
        # TODO Enable perspective/orthogonal in application
        self.proj.setToIdentity()
        # Perspective
        self.proj.perspective(45.0, (w / h), 1.0, 10000.0)

        # Orthogonal
        # w = w * (abs(self.zCenterPos) - abs(self.zCameraPos)) * -0.001
        # h = h * (abs(self.zCenterPos) - abs(self.zCameraPos)) * -0.001
        # self.proj.ortho(-w, w, -h, h, 1.0, 10000.0)

    """
    Utilities
    """
    @staticmethod
    def print_fps(fps):
        print(f'               \r', end='')
        print(f'FPS: {fps:.1f} \r', end='')

    def unproject(self, _x, _y, _z, model, view, proj) -> QVector3D:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        x = (2.0 * _x / self.width()) - 1.0
        y = 1.0 - (2.0 * _y / self.height())

        ray_eye = proj.inverted()[0] * QVector4D(x, y, -1.0, 1.0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        ray_world = ((view * model).inverted()[0] * ray_eye).toVector3D()
        return ray_world.normalized()

    def ray_from_click(self, x: float, y: float, z: float) -> tuple:
        # Generates a ray from a click on screen
        ray = self.unproject(x, y, z, self.world, self.camera, self.proj)
        origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()

        # To Numpy array
        ray = np.array([ray.x(), ray.y(), ray.z()])
        origin = np.array([origin.x(), origin.y(), origin.z()])

        return ray, origin

    def slice_from_rays(self, ray_list: list):
        camera_origin = (self.camera * self.world).inverted()[0].column(3).toVector3D()
        origin = np.array([camera_origin.x(), camera_origin.y(), camera_origin.z()])

        mesh_drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        mesh_elements = [m.element for m in mesh_drawables]

        for mesh in mesh_elements:
            slices = utils.slice_mesh_from_rays(mesh, origin, ray_list)

            for i, vert_slice in enumerate(slices):
                self.lines(vertices=vert_slice,
                           color=mesh.color,
                           name=f'SLICE_{i}_{mesh.name}',
                           extension=mesh.extension,
                           loop=True)

        # We'll auto-exit the slice mode for now
        self.set_normal_mode()

    def detect_mesh_intersection(self, x: float, y: float, z: float) -> None:
        ray, origin = self.ray_from_click(x, y, z)
        intersected_mesh_ids = []

        mesh_drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        mesh_elements = [m.element for m in mesh_drawables]

        for mesh in mesh_elements:
            point_list = utils.mesh_intersection(origin, ray, mesh)
            # print(f'(Mesh {mesh.id}) Intersects: {point_list}')
            if len(point_list) > 0:
                intersected_mesh_ids.append(mesh.id)

        # Emit signal with clicked mesh
        self.mesh_clicked_signal.emit(intersected_mesh_ids)

        # print('-------------------------------')

    """
    Controller
    """
    def set_controller_mode(self, mode: str):
        controllers = {
            'normal': NormalMode,
            'detection': DetectionMode,
            'slice': SliceMode,
        }

        self.current_mode = controllers[mode]()
        self.update()

    def set_normal_mode(self) -> None:
        self.set_controller_mode('normal')

    def set_detection_mode(self) -> None:
        self.set_controller_mode('detection')

    def set_slice_mode(self) -> None:
        self.set_controller_mode('slice')

    def take_screenshot(self, save_path=None):
        if not save_path:
            save_path = f'MineVis Screenshot ({datetime.now().strftime("%Y%m%d-%H%M%S")}).png'
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        pixmap.save(save_path)

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
        path_list = []
        while it.hasNext():
            path_list.append(it.next())

        for path in sorted(path_list):
            self.mesh_by_path(path)
