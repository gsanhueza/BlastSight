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
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot

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

        # Shaders
        self.shader_program = QOpenGLShaderProgram(self)
        self.vertex_shader = None
        self.fragment_shader = None
        self.geometry_shader = None

        # VAO/VBO (Mesh)
        self.mesh_vao = QOpenGLVertexArrayObject()
        self.mesh_positions_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.mesh_indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self.mesh_colors_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

        # VAO/VBO (Block Model)
        self.block_model_vao = QOpenGLVertexArrayObject()
        self.block_model_positions_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.block_model_indices_ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self.block_model_colors_vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)

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

        # Shader locations
        self.vertex_shader_source = 'View/Shaders/vertex.glsl'
        self.fragment_shader_source = 'View/Shaders/fragment.glsl'
        self.geometry_shader_source = 'View/Shaders/geometry.glsl'

        # MVP locations
        self.model_view_matrix_loc = None
        self.proj_matrix_loc = None
        self.test_value_loc = None

        # Data (Mesh)
        self.mesh_positions = None
        self.mesh_indices = None
        self.mesh_values = None

        # Data (Block Model)
        self.block_model_positions = None
        self.block_model_indices = None
        self.block_model_values = None

        # Wireframe (Shader toggling)
        self.wireframe_enabled = True

        # QPainter (after OpenGL)
        self.painter = QPainter()

    def initializeGL(self):
        self.shader_program = QOpenGLShaderProgram(self.context())

        # Create shaders
        self.vertex_shader = QOpenGLShader(QOpenGLShader.Vertex)
        self.fragment_shader = QOpenGLShader(QOpenGLShader.Fragment)
        self.geometry_shader = QOpenGLShader(QOpenGLShader.Geometry)

        # Compile shaders
        self.vertex_shader.compileSourceFile(self.vertex_shader_source)
        self.fragment_shader.compileSourceFile(self.fragment_shader_source)
        self.geometry_shader.compileSourceFile(self.geometry_shader_source)

        # Add shaders to program
        self.shader_program.addShader(self.vertex_shader)
        self.shader_program.addShader(self.fragment_shader)
        self.shader_program.addShader(self.geometry_shader)

        # If the shader uses 'layout (location = 0) in vec3 a_position;', then
        # it's unnecessary to bind a name. We only need to remember that in
        # glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None),
        # that '_POSITION' is 0 here, and 0 in the shader (or 1, or 2...)

        # Bind attribute locations (Unneeded if shader has layout(location))
        # self.shader_program.bindAttributeLocation('a_position', _POSITION)
        # self.shader_program.bindAttributeLocation('a_color', _COLOR)

        self.shader_program.link()
        self.shader_program.bind()

        # MVP locations
        self.model_view_matrix_loc = self.shader_program.uniformLocation('model_view_matrix')
        self.proj_matrix_loc = self.shader_program.uniformLocation('proj_matrix')

        # Data (Mesh)
        self.mesh_positions = np.array([-0.5, 0.5, 0.0,
                                        -0.5, -0.5, 0.0,
                                        0.5, 0.5, 0.0], np.float32)

        self.mesh_values = np.array([1.0, 0.0, 0.0,
                                     0.0, 1.0, 0.0,
                                     0.0, 0.0, 1.0], np.float32)

        self.mesh_indices = np.array([0, 1, 2], np.uint32)  # GL_UNSIGNED_INT = np.uint32

        # Data (Block Model)
        self.block_model_positions = np.array([-1.5, 1.5, 0.0,
                                               -1.5, -1.5, 0.0,
                                               1.5, 1.5, 0.0], np.float32)

        self.block_model_values = np.array([1.0, 0.0, 0.0,
                                            0.0, 1.0, 0.0,
                                            0.0, 0.0, 1.0], np.float32)

        self.block_model_indices = np.array([0, 1, 2], np.uint32)  # GL_UNSIGNED_INT = np.uint32

        # VAO/VBO/IBO creation
        self.mesh_vao.create()
        self.mesh_positions_vbo.create()
        self.mesh_colors_vbo.create()
        self.mesh_indices_ibo.create()

        self.block_model_vao.create()
        self.block_model_positions_vbo.create()
        self.block_model_colors_vbo.create()
        self.block_model_indices_ibo.create()

        # Setup vertex attributes
        self.setup_vertex_attribs()

        # Camera setup
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos)

    def setup_vertex_attribs_mesh(self):
        _SIZE_OF_GL_FLOAT = 4

        self.makeCurrent()

        self.mesh_vao.bind()

        self.mesh_positions_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.mesh_positions.size, self.mesh_positions, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.mesh_colors_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.mesh_values.size, self.mesh_values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.mesh_indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.mesh_indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.mesh_vao.release()

    def setup_vertex_attribs_block_model(self):
        _SIZE_OF_GL_FLOAT = 4

        self.makeCurrent()

        self.block_model_vao.bind()

        self.block_model_positions_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.block_model_positions.size, self.block_model_positions, GL_STATIC_DRAW)
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, None)

        self.block_model_colors_vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, _SIZE_OF_GL_FLOAT * self.block_model_values.size, self.block_model_values, GL_STATIC_DRAW)
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, None)

        self.block_model_indices_ibo.bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.block_model_indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)

        self.block_model_vao.release()

    def setup_vertex_attribs(self):
        self.setup_vertex_attribs_mesh()
        self.setup_vertex_attribs_block_model()

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

        # Bind data of shaders to program
        self.shader_program.bind()
        self.shader_program.setUniformValue(self.proj_matrix_loc, self.proj)
        self.shader_program.setUniformValue(self.model_view_matrix_loc, self.camera * self.world)

        # Draw mesh
        self.draw_mesh()

        # Draw block model
        self.draw_block_model()

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

    # Draws the mesh only
    def draw_mesh(self):
        self.mesh_vao.bind()
        # glDrawArrays(GL_TRIANGLES, 0, self.mesh_positions.size)  # This works on its own
        glDrawElements(GL_TRIANGLES, self.mesh_indices.size, GL_UNSIGNED_INT, None)
        self.mesh_vao.release()

    # Draws the block model only
    def draw_block_model(self):
        self.block_model_vao.bind()
        # glDrawArrays(GL_POINTS, 0, self.block_model_positions.size)  # This works on its own
        # glDrawElements(GL_POINTS, self.block_model_indices.size, GL_UNSIGNED_INT, None)
        glDrawElements(GL_TRIANGLES, self.block_model_indices.size, GL_UNSIGNED_INT, None)
        self.block_model_vao.release()

    @Slot()
    def update_mesh(self):
        self.mesh_positions = np.array(self.model.get_mesh_vertices(), np.float32)
        self.mesh_indices = np.array(self.model.get_mesh_indices(), np.uint32)
        self.mesh_values = np.array(self.model.get_mesh_values(), np.float32)

        self.setup_vertex_attribs_mesh()
        self.update()

    @Slot()
    def update_block_model(self):
        self.block_model_positions = np.array(self.model.get_block_model_vertices(), np.float32)
        self.block_model_indices = np.array(self.model.get_block_model_indices(), np.uint32)
        self.block_model_values = np.array(self.model.get_block_model_values(), np.float32)

        self.setup_vertex_attribs_block_model()
        self.update()

    @Slot()
    def toggle_wireframe(self):
        if self.wireframe_enabled:
            self.shader_program.removeShader(self.geometry_shader)
            self.wireframe_enabled = False
        else:
            self.shader_program.addShader(self.geometry_shader)
            self.wireframe_enabled = True

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
