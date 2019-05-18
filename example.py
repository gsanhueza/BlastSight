#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.openglwidget import OpenGLWidget
from Model.model import Model


class MineVisViewer(OpenGLWidget):
    # FIXME You still need to queue commands
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

    def show(self):
        super().show()
        sys.exit(self.app.exec_())


def test_viewer():
    viewer = MineVisViewer()
    id_off = viewer.add_mesh('tests/Files/caseron.off')
    # viewer.delete_element(id_off)
    viewer.show()


def test_block_model():
    viewer = MineVisViewer()
    id_csv = viewer.add_block_model('Model/BlockModel/complex.csv')
    bm = viewer.model.get_block_model(id_csv)
    bm.set_value_string('Au')
    bm.update_values()
    viewer.show()


def test_model():
    model = Model()
    id_1 = model.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('memory 1 ?')
    id_2 = model.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    input('memory 1 + 2?')
    model.delete_mesh(id_1)
    input('memory 2 - 1?')
    model.delete_mesh(id_2)
    input('memory with no meshes?')


def test_element():
    from Model.Parsers.offparser import OFFParser
    from Model.Elements.element import Element

    file_path = '/home/gabriel/xyzrgb_statuette.off'
    input('before?')
    vertices, indices = OFFParser.load_file(file_path)
    input('memory post-parse ?')
    element = Element(vertices=vertices)
    input('memory post-create ?')
    del vertices
    del indices
    input('memory post-del tuple ?')
    print(element.name)


def test_meshelement():
    from Model.Parsers.offparser import OFFParser
    from Model.Elements.meshelement import MeshElement

    file_path = '/home/gabriel/xyzrgb_statuette.off'
    input('before?')
    vertices, indices = OFFParser.load_file(file_path)
    input('memory post-parse ?')
    mesh = MeshElement(vertices=vertices, indices=indices)
    input('memory post-create ?')
    del vertices
    del indices
    input('memory post-del tuple ?')
    print(mesh.name)


if __name__ == '__main__':
    test_viewer()
