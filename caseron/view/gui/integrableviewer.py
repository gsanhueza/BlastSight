#!/usr/bin/env python

import numpy as np
import traceback

from OpenGL.GL import *

from qtpy.QtCore import QPoint
from qtpy.QtCore import Signal
from qtpy.QtCore import QFileInfo
from qtpy.QtGui import QMatrix4x4
from qtpy.QtGui import QPixmap
from qtpy.QtGui import QRegion
from qtpy.QtGui import QVector4D
from qtpy.QtWidgets import QOpenGLWidget

from ..drawables.glaxiscollection import GLAxisCollection
from ..drawables.glbackgroundcollection import GLBackgroundCollection
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
from ...controller.measurementmode import MeasurementMode

from ...model import utils
from ...model.model import Model
from ...model.elements.nullelement import NullElement


class IntegrableViewer(QOpenGLWidget):
    # Signals
    signal_load_success = Signal(int)
    signal_load_failure = Signal()
    signal_export_success = Signal(int)
    signal_export_failure = Signal()

    signal_file_modified = Signal()
    signal_mesh_clicked = Signal(object)
    signal_mesh_distances = Signal(object)
    signal_mode_updated = Signal(str)
    signal_fps_updated = Signal(float)

    def __init__(self, parent=None):
        QOpenGLWidget.__init__(self, parent)
        self.setAcceptDrops(True)

        # Model
        self.model = Model()

        # Controller mode
        self.signal_mode_updated.connect(lambda m: print(f'MODE: {m}'))
        self.current_mode = None
        self.set_normal_mode()

        # Drawable elements
        self.axis_collection = GLAxisCollection(self)
        self.background_collection = GLBackgroundCollection(self)
        self.drawable_collection = GLDrawableCollection(self)

        self.axis_collection.add(AxisGL(NullElement(id='AXIS')))
        self.background_collection.add(BackgroundGL(NullElement(id='BG')))

        # Camera/World/Projection
        self.camera = QMatrix4x4()
        self.world = QMatrix4x4()
        self.proj = QMatrix4x4()

        # FPS Counter
        self.fps_counter = FPSCounter()

        # Initial positions and rotations
        self.rotation_center = [0.0, 0.0, 0.0]
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.camera_position = [0.0, 0.0, 200.0]

        # Extra information
        self.fov = 45.0
        self.smoothness = 1.0  # Bigger => smoother (but slower) rotations
        self.projection_mode = 'perspective'  # 'perspective'/'orthographic'

    """
    Properties
    """
    @property
    def last_id(self) -> int:
        return self.drawable_collection.last_id

    @property
    def last_drawable(self):
        return self.get_drawable(self.last_id)

    @property
    def off_center(self) -> np.ndarray:
        return self.camera_position - self.rotation_center

    @property
    def camera_position(self) -> np.ndarray:
        return np.array([self.xCameraPos, self.yCameraPos, self.zCameraPos])

    @property
    def rotation_angle(self) -> np.ndarray:
        return np.array([self.xCenterRot, self.yCenterRot, self.zCenterRot])

    @property
    def rotation_center(self) -> np.ndarray:
        return np.array([self.xCenterPos, self.yCenterPos, self.zCenterPos])

    @camera_position.setter
    def camera_position(self, pos: list) -> None:
        self.xCameraPos, self.yCameraPos, self.zCameraPos = pos

    @rotation_angle.setter
    def rotation_angle(self, rot: list) -> None:
        self.xCenterRot, self.yCenterRot, self.zCenterRot = rot

    @rotation_center.setter
    def rotation_center(self, center: list) -> None:
        self.xCenterPos, self.yCenterPos, self.zCenterPos = center

    """
    Axis/Background
    """
    @property
    def axis(self):
        return self.axis_collection.get('AXIS')

    @property
    def background(self):
        return self.background_collection.get('BG')

    """
    Load methods
    """
    def _load_drawable(self, method: classmethod, drawable_type: type, *args, **kwargs):
        try:
            element = method(*args, **kwargs)
            drawable = drawable_type(element, *args, **kwargs)
            self.drawable_collection.add(drawable)

            self.signal_load_success.emit(drawable.id)
            self.signal_file_modified.emit()
            self.update()

            return drawable
        except Exception:
            self.signal_load_failure.emit()
            traceback.print_exc()
            return None

    def _load_folder(self, method: classmethod, path: str, *args, **kwargs) -> list:
        path_list = self.model.get_paths_from_directory(path)
        drawables = []

        for path in path_list:
            drawables.append(method(path, *args, **kwargs))

        return [d for d in drawables if d is not None]

    """
    Load methods by arguments
    """
    def mesh(self, *args, **kwargs) -> MeshGL:
        return self._load_drawable(self.model.mesh, MeshGL, *args, **kwargs)

    def blocks(self, *args, **kwargs) -> BlockGL:
        return self._load_drawable(self.model.blocks, BlockGL, *args, **kwargs)

    def points(self, *args, **kwargs) -> PointGL:
        return self._load_drawable(self.model.points, PointGL, *args, **kwargs)

    def lines(self, *args, **kwargs) -> LineGL:
        return self._load_drawable(self.model.lines, LineGL, *args, **kwargs)

    def tubes(self, *args, **kwargs) -> TubeGL:
        return self._load_drawable(self.model.tubes, TubeGL, *args, **kwargs)

    """
    Load methods by path
    """
    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshGL:
        return self._load_drawable(self.model.mesh_by_path, MeshGL, path, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockGL:
        return self._load_drawable(self.model.blocks_by_path, BlockGL, path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointGL:
        return self._load_drawable(self.model.points_by_path, PointGL, path, *args, **kwargs)

    def meshes_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self._load_folder(self.mesh_by_path, path, *args, **kwargs)

    def blocks_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self._load_folder(self.blocks_by_path, path, *args, **kwargs)

    def points_by_folder_path(self, path: str, *args, **kwargs) -> list:
        return self._load_folder(self.points_by_path, path, *args, **kwargs)

    """
    Export methods
    """
    def _export_element(self, method: classmethod, path: str, _id: int) -> None:
        try:
            method(path, _id)
            self.signal_export_success.emit(_id)
        except Exception:
            self.signal_export_failure.emit()

    def export_mesh(self, path, _id) -> None:
        self._export_element(self.model.export_mesh, path, _id)

    def export_blocks(self, path, _id) -> None:
        self._export_element(self.model.export_blocks, path, _id)

    def export_points(self, path, _id) -> None:
        self._export_element(self.model.export_points, path, _id)

    """
    Drawable manipulation
    """
    def get_drawable(self, _id: int):
        return self.drawable_collection.get(_id, None)

    def show_drawable(self, _id: int) -> None:
        self.get_drawable(_id).show()
        self.update()

    def hide_drawable(self, _id: int) -> None:
        self.get_drawable(_id).hide()
        self.update()

    def update_drawable(self, _id: int) -> None:
        self.makeCurrent()
        self.get_drawable(_id).setup_attributes()
        self.update()

    def delete(self, _id: int) -> None:
        if _id < 0:
            return

        self.makeCurrent()
        self.model.delete(_id)
        self.drawable_collection.delete(_id)
        self.signal_file_modified.emit()
        self.update()

    def update_all(self) -> None:
        for _id in list(self.drawable_collection.keys()):
            self.update_drawable(_id)

    def clear(self) -> None:
        for _id in list(self.drawable_collection.keys()):
            self.delete(_id)

    """
    Camera handling
    """
    def camera_at(self, _id: int) -> None:
        self.fit_to_bounds(*self.get_drawable(_id).element.bounding_box)
        self.update()

    def plan_view(self) -> None:
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.update()

    def north_view(self) -> None:
        self.rotation_angle = [270.0, 0.0, 270.0]
        self.update()

    def east_view(self) -> None:
        self.rotation_angle = [270.0, 0.0, 0.0]
        self.update()

    def fit_to_bounds(self, min_bound: np.ndarray, max_bound: np.ndarray) -> None:
        center = (min_bound + max_bound) / 2
        self.rotation_center = center
        self.camera_position = center

        # Put the camera in a position that allow us to see between the boundaries.
        # In perspective projection, we need a clever trigonometric calculation.
        md = np.max(np.diff([min_bound, max_bound], axis=0))
        aspect = self.width() / self.height()
        fov_rad = self.fov * np.pi / 180.0
        dist = (md / np.tan(fov_rad / 2) + md) / 2.0
        camera_shift = dist * max(1.0, 1.0 / aspect)

        # But in orthographic projection, it's more direct.
        if self.projection_mode == 'orthographic':
            dist = md / 2
            camera_shift = dist * max(1.0, aspect)

        self.zCameraPos += 1.1 * camera_shift
        self.update()

    def fit_to_screen(self) -> None:
        drawables = [d for d in self.drawable_collection.values() if d.is_visible]

        if len(drawables) == 0:
            return

        min_all = np.inf * np.ones(3)
        max_all = -np.inf * np.ones(3)

        for drawable in drawables:
            min_bound, max_bound = drawable.element.bounding_box
            min_all = np.min((min_all, min_bound), axis=0)
            max_all = np.max((max_all, max_bound), axis=0)

        self.fit_to_bounds(min_all, max_all)
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
        self.proj.setToIdentity()

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

        # Project (Perspective/Orthographic)
        self.resizeGL(self.width(), self.height())

        # Draw every GLDrawable (meshes, blocks, points, etc)
        glEnable(GL_BLEND)
        self.background_collection.draw(self.proj, self.camera, self.world)
        self.drawable_collection.draw(self.proj, self.camera, self.world)
        self.axis_collection.draw(self.proj, self.camera, self.world)

        # Tick FPS counter
        self.fps_counter.tick()
        self.signal_fps_updated.emit(self.fps_counter.fps)

    def resizeGL(self, w: float, h: float) -> None:
        if self.projection_mode == 'perspective':
            self.proj.perspective(self.fov, (w / h), 1.0, 10000.0)
        elif self.projection_mode == 'orthographic':
            z = self.off_center[2]
            aspect = w / h
            self.proj.ortho(-z, z, -z / aspect, z / aspect, 0.0, 10000.0)

    """
    Utilities
    """
    def get_pixmap(self) -> QPixmap:
        pixmap = QPixmap(self.size())
        self.render(pixmap, QPoint(), QRegion(self.rect()))
        return pixmap

    def take_screenshot(self, save_path=None) -> None:
        if save_path is not None:
            self.get_pixmap().save(save_path)

    def screen_to_ndc(self, _x, _y, _z) -> np.ndarray:
        # Click at bottom-left of screen => (-1.0, -1.0, z)
        # Click at top-right of screen => (1.0, 1.0, z)
        # But we can't really know where's z, so we just return 1.0
        x = (2.0 * _x / self.width()) - 1.0
        y = 1.0 - (2.0 * _y / self.height())
        z = 1.0
        return np.array([x, y, z])

    def unproject(self, _x, _y, _z, model, view, proj) -> np.ndarray:
        # Adapted from http://antongerdelan.net/opengl/raycasting.html
        x, y, z = self.screen_to_ndc(_x, _y, _z)

        ray_eye = proj.inverted()[0] * QVector4D(x, y, -1.0, 1.0)
        ray_eye = QVector4D(ray_eye.x(), ray_eye.y(), -1.0, 0.0)

        ray_world = ((view * model).inverted()[0] * ray_eye).toVector3D()
        ray = ray_world.normalized()
        return np.array([ray.x(), ray.y(), ray.z()])

    def get_origin(self, model, view) -> np.ndarray:
        origin = (view * model).inverted()[0].column(3).toVector3D()
        return np.array([origin.x(), origin.y(), origin.z()])

    def ray_from_click(self, x: float, y: float, z: float) -> tuple:
        # Generates a ray from a click on screen
        # Assume perspective first
        ray = self.unproject(x, y, z, self.world, self.camera, self.proj)
        origin = self.get_origin(self.world, self.camera)

        # Orthographic projection needs a bit more of vector arithmetic.
        if self.projection_mode == 'orthographic':
            # A click in the center of the screen gives us the perfect ray,
            # by recycling the perspective's un-project method.
            ray = self.unproject(self.width() / 2, self.height() / 2, z,
                                 self.world, self.camera, self.proj)

            # But if we don't click in the exact center of screen,
            # we need to trick the origin calculation.
            ndc = self.screen_to_ndc(x, y, z)
            aspect = self.width() / self.height()
            aspect_bias = np.array([1.0, 1.0 / aspect, 0.0])

            # The idea is to strategically move the camera by an offset, so that
            # clicking anywhere in the screen will give us the same result as
            # clicking at the exact center of the screen from a shifted camera.
            offset = self.off_center[2] * ndc * aspect_bias

            # Hack to get the origin when the click is not exactly at center of screen.
            self.camera.translate(*-offset)
            origin = self.get_origin(self.world, self.camera)
            self.camera.translate(*offset)

        return ray, origin

    def slice_visible_meshes(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        mesh_drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        mesh_elements = [m.element for m in mesh_drawables if 'SLICE' not in m.element.name]

        for mesh in mesh_elements:
            slices = utils.slice_mesh(mesh, origin, plane_normal)
            for i, vert_slice in enumerate(slices):
                self.lines(vertices=vert_slice,
                           color=mesh.color,
                           name=f'MESHSLICE_{i}_{mesh.name}',
                           extension=mesh.extension,
                           loop=True)

    def slice_visible_blocks(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        block_drawables = [m for m in self.drawable_collection.filter(BlockGL) if m.is_visible]
        block_elements = [m.element for m in block_drawables if 'SLICE' not in m.element.name]

        for block in block_elements:
            slices, values = utils.slice_blocks(block, origin, plane_normal)
            self.blocks(vertices=slices,
                        values=values,
                        vmin=block.vmin,
                        vmax=block.vmax,
                        colormap=block.colormap,
                        name=f'BLOCKSLICE_{block.name}',
                        extension=block.extension,
                        block_size=block.block_size,
                        alpha=1.0,
                        )

    def slice_visible_drawables(self, origin: np.ndarray, plane_normal: np.ndarray) -> None:
        self.slice_visible_meshes(origin, plane_normal)
        self.slice_visible_blocks(origin, plane_normal)

    def slice_from_rays(self, origin_list: list, ray_list: list) -> None:
        # A plane is created from `origin` and `ray_list`.
        # In perspective projection, the origin is the same.
        origin = origin_list[0]

        if self.projection_mode == 'perspective':
            # Perspective: Same origins, different rays
            plane_normal = np.cross(*ray_list)
        else:
            # Orthographic: Same rays, different origins
            origin_diff = np.diff(origin_list, axis=0)[0]
            plane_normal = np.cross(ray_list[0], origin_diff)

        plane_normal /= np.linalg.norm(plane_normal)

        # Slice drawables
        self.slice_visible_drawables(origin, plane_normal)

        # Auto-exit the slice mode for now
        self.set_normal_mode()

    def measure_from_rays(self, origin_list: list, ray_list: list) -> None:
        drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        elements = [m.element for m in drawables]

        points_A = []
        points_B = []

        for mesh in elements:
            int_A = utils.mesh_intersection(origin_list[0], ray_list[0], mesh)
            int_B = utils.mesh_intersection(origin_list[1], ray_list[1], mesh)

            # Discard non-intersections
            if int_A.size > 0:
               points_A.append(utils.closest_point_to(origin_list[0], int_A))

            if int_B.size > 0:
               points_B.append(utils.closest_point_to(origin_list[1], int_B))

        distance = None
        if len(points_A) > 0 and len(points_B) > 0:
            points_A = np.vstack(points_A)
            points_B = np.vstack(points_B)

            closest_A = utils.closest_point_to(origin_list[0], points_A)
            closest_B = utils.closest_point_to(origin_list[1], points_B)

            distance = np.linalg.norm(closest_B - closest_A)

        self.signal_mesh_distances.emit(distance)

    def detect_mesh_intersection(self, x: float, y: float, z: float) -> None:
        ray, origin = self.ray_from_click(x, y, z)
        intersected_ids = []

        drawables = [m for m in self.drawable_collection.filter(MeshGL) if m.is_visible]
        elements = [m.element for m in drawables]

        for mesh in elements:
            intersections = utils.mesh_intersection(origin, ray, mesh)
            point = utils.closest_point_to(origin, intersections)
            # print(f'(Mesh {mesh.id}): Intersections: {intersections}')
            # print(f'(Mesh {mesh.id}): Closest intersection: {point}')
            if point is not None:
                intersected_ids.append(mesh.id)

        # Emit signal with clicked mesh
        self.signal_mesh_clicked.emit(intersected_ids)

        # print('-------------------------------')

    """
    Controller
    """
    def set_controller_mode(self, mode: str) -> None:
        controllers = {
            'normal': NormalMode,
            'detection': DetectionMode,
            'slice': SliceMode,
            'measurement': MeasurementMode,
        }

        self.current_mode = controllers[mode]()
        self.signal_mode_updated.emit(self.current_mode.name)
        self.update()

    def set_normal_mode(self) -> None:
        self.set_controller_mode('normal')

    def set_detection_mode(self) -> None:
        self.set_controller_mode('detection')

    def set_slice_mode(self) -> None:
        self.set_controller_mode('slice')

    def set_measurement_mode(self) -> None:
        self.set_controller_mode('measurement')

    """
    Projections
    """
    def perspective_projection(self) -> None:
        self.projection_mode = 'perspective'
        self.update()

    def orthographic_projection(self) -> None:
        self.projection_mode = 'orthographic'
        self.update()

    """
    Events (dependent on current controller)
    """
    def mouseMoveEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mouseMoveEvent(event, self)
        self.update()

    def mousePressEvent(self, event, *args, **kwargs) -> None:
        self.current_mode.mousePressEvent(event, self)
        self.update()

    def mouseDoubleClickEvent(self, event, *args, **kwargs):
        self.current_mode.mouseDoubleClickEvent(event, self)
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
                self.meshes_by_folder_path(path)
            else:
                self.mesh_by_path(path)
