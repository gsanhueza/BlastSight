#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import QPainter
from PySide2.QtGui import QOpenGLShaderProgram
from PySide2.QtGui import QOpenGLShader
from PySide2.QtGui import QOpenGLBuffer
from PySide2.QtGui import QOpenGLVertexArrayObject
from PySide2.QtGui import QMatrix4x4
from PySide2.QtGui import QVector2D
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot

from View.gldrawable import GLDrawable
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

        # Mesh
        self.mesh = GLDrawable(self)
        self.block_model = GLDrawable(self)

        # FIXME Enable a way to change this (factory pattern?)
        self.block_model.vertex_shader_source = 'View/Shaders/block_model_vertex.glsl'
        self.block_model.fragment_shader_source = 'View/Shaders/block_model_fragment.glsl'
        self.block_model.geometry_shader_source = 'View/Shaders/block_model_geometry.glsl'

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

        # Wireframe (Shader toggling)
        self.wireframe_enabled = True

        # QPainter (after OpenGL)
        self.painter = QPainter()

    def initializeGL(self):
        self.mesh.set_vertex_shader_source('View/Shaders/mesh_vertex.glsl')
        self.mesh.set_fragment_shader_source('View/Shaders/mesh_fragment.glsl')
        self.mesh.set_geometry_shader_source('View/Shaders/mesh_geometry.glsl')
        self.mesh.initialize_shader_program()
        self.mesh.initialize_buffers()

        self.block_model.set_vertex_shader_source('View/Shaders/block_model_vertex.glsl')
        self.block_model.set_fragment_shader_source('View/Shaders/block_model_fragment.glsl')
        self.block_model.set_geometry_shader_source('View/Shaders/block_model_geometry.glsl')
        self.block_model.initialize_shader_program()
        self.block_model.initialize_buffers()

        # Data (Mesh)
        self.mesh.update_positions(np.array([-0.5, 0.5, 0.0,
                                             -0.5, -0.5, 0.0,
                                             0.5, 0.5, 0.0], np.float32))

        self.mesh.update_values(np.array([1.0, 0.0, 0.0,
                                          0.0, 1.0, 0.0,
                                          0.0, 0.0, 1.0], np.float32))

        self.mesh.update_indices(np.array([0, 1, 2], np.uint32))  # GL_UNSIGNED_INT = np.uint32

        # Data (Block Model)
        self.block_model.update_positions(np.array([-1.5, 1.5, 0.0,
                                                    -1.5, -1.5, 0.0,
                                                    1.5, 1.5, 0.0], np.float32))

        self.block_model.update_values(np.array([1.0, 0.0, 0.0,
                                                 0.0, 1.0, 0.0,
                                                 0.0, 0.0, 1.0], np.float32))

        self.block_model.update_indices(np.array([0, 1, 2], np.uint32))  # GL_UNSIGNED_INT = np.uint32

        # Setup vertex attributes
        self.mesh.setup_vertex_attribs()
        self.block_model.setup_vertex_attribs()

        # Setup uniforms
        self.mesh.setup_uniforms()
        self.block_model.setup_uniforms()

        # Camera setup
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos)

    def paintGL(self):
        self.painter.begin(self)
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)  # If uncommented, overpainting seems to stop working (maybe)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow rotation of the world
        self.world.rotate(self.xRot / 16.0, 1, 0, 0)
        self.world.rotate(self.yRot / 16.0, 0, 1, 0)
        self.world.rotate(self.zRot / 16.0, 0, 0, 1)

        # Draw mesh
        self.mesh.draw(GL_TRIANGLES)

        # Draw block model
        self.block_model.draw(GL_POINTS)

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
        self.mesh.update_positions(np.array(self.model.get_mesh_vertices(), np.float32))
        self.mesh.update_indices(np.array(self.model.get_mesh_indices(), np.uint32))
        self.mesh.update_values(np.array(self.model.get_mesh_values(), np.float32))

        self.mesh.setup_vertex_attribs()
        self.update()

    @Slot()
    def update_block_model(self):
        self.block_model.update_positions(np.array(self.model.get_block_model_vertices(), np.float32))
        self.block_model.update_indices(np.array(self.model.get_block_model_indices(), np.uint32))
        self.block_model.update_values(np.array(self.model.get_block_model_values(), np.float32))

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
            self.model.load_mesh(file_path)
            self.update_mesh()
        except KeyError:
            self.model.load_block_model(file_path)
            self.update_block_model()

        # Check if we're part of a MainWindow or a standalone widget
        if self.parent():
            self.parent().statusBar.showMessage('Drop')
