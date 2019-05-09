#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.openglwidget import OpenGLWidget
from Model.model import Model


class MineVisViewer(OpenGLWidget):
    # FIXME You still need to queue commands
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

    def show(self):
        super().show()
        sys.exit(self.app.exec_())


def test_model():
    model = Model()
    input('Before load')
    id_off = model.add_mesh('Model/Mesh/caseron.off')
    input('After load')
    model.update_mesh(id_off, '/home/gabriel/xyzrgb_statuette.off')
    input('After update')
    model.update_mesh(id_off, '/home/gabriel/xyzrgb_statuette.off')
    input('After update')
    model.delete_mesh(id_off)
    input('After delete')
    id_off = model.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('After big load again')
    model.delete_mesh(id_off)
    input('After delete')


def test_viewer():
    viewer = MineVisViewer()
    input('Before load')
    id_off = viewer.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('After load')
    viewer.delete_mesh(id_off)
    input('After delete')
    id_off = viewer.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('After load')
    viewer.delete_mesh(id_off)
    input('After delete')
    id_off = viewer.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('After load')
    viewer.delete_mesh(id_off)
    input('After delete')
    viewer.show()


if __name__ == '__main__':
    test_viewer()
