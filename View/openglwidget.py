#!/usr/bin/env python

import numpy as np

from OpenGL.GL import *
from PySide2.QtWidgets import QOpenGLWidget
from PySide2.QtGui import *
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter

from .normalmode import NormalMode


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, mode_class=NormalMode, model=None):
        QOpenGLWidget.__init__(self, parent)
        self.setFocusPolicy(Qt.StrongFocus)

        # Visualization mode
        self.current_mode = mode_class(self)

        # Model
        self.model = model

        # Shader utility
        self.program = QOpenGLShaderProgram(self)
        self.rotation = 0

        # VAO/VBO
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer()

        # Camera
        self.camera = QMatrix4x4()
        self.xCamPos = 0.0
        self.yCamPos = 0.0
        self.zCamPos = 0.0

        # World
        self.world = QMatrix4x4()

        # Rotation
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        # Projection
        self.proj = QMatrix4x4()


    def setup_vertex_attribs(self):
        _POSITION = 0
        _COLOR = 1

        position = np.array([-0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0], np.float32)
        color = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], np.float32)

        self.vbo.bind()

        glEnableVertexAttribArray(_POSITION)
        glEnableVertexAttribArray(_COLOR)
        print("TEST1")
        glVertexAttribPointer(_POSITION, 3, GL_FLOAT, False, 0, position)
        print("TEST2")
        glVertexAttribPointer(_COLOR, 3, GL_FLOAT, False, 0, color)
        print("TEST3")

        self.vbo.release()

    def initializeGL(self):
        # FIXME Are you sure you'll use just one shader for everything?
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'View/Shaders/vertex.glsl')
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'View/Shaders/fragment.glsl')

        self.program.bindAttributeLocation('vertex', 0)
        self.program.bindAttributeLocation('color', 1)
        self.program.link()

        self.program.bind()

        self.modelViewMatrixLoc = self.program.uniformLocation('modelViewMatrix')
        self.projMatrixLoc = self.program.uniformLocation('projMatrix')

        self.vao.create()

        # Store the vertex attribute bindings for the program.
        self.setup_vertex_attribs()

        # Our camera has an initial position.
        self.camera.setToIdentity()
        self.camera.translate(self.xCamPos, self.yCamPos, self.zCamPos);

        self.program.release()

    def paintGL(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        self.world.setToIdentity()

        # Allow rotation of the world
        self.world.rotate(self.xRot / 16.0, 1, 0, 0)
        self.world.rotate(self.yRot / 16.0, 0, 1, 0)
        self.world.rotate(self.zRot / 16.0, 0, 0, 1)

        # Bind VAO
        vaoBinder = QOpenGLVertexArrayObject.Binder(self.vao)

        # Bind data of shaders to program
        self.program.bind();
        self.program.setUniformValue(self.projMatrixLoc, self.proj);
        self.program.setUniformValue(self.modelViewMatrixLoc, self.camera * self.world);

        # Load new data only on model data change
        self.dataAlreadyLoaded = False
        if (not self.dataAlreadyLoaded):

            # Load data
            def loadData():
                pass
            loadData()

            # Store the vertex attribute bindings for the program.
            self.setup_vertex_attribs()

            self.dataAlreadyLoaded = True

        # Draw triangulation
        # Last argument = Number of vertices in total
        glDrawArrays(GL_TRIANGLES, 0, 3 * 4);

        self.program.release();

    def resizeGL(self, w, h):
        self.proj.setToIdentity()
        self.proj.perspective(45.0, (w / h), 0.01, 10000.0)

    # Controller dependent on current mode
    def mouseMoveEvent(self, event):
        self.current_mode.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.current_mode.mousePressEvent(event)

    @Slot()
    def update_mesh():
        # TODO On mesh load, delete current opengl vertices/faces, recreate them and update
        self.update()
