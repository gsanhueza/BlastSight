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


def try_viewer():
    viewer = MineVisViewer()
    id_off = viewer.add_mesh('tests/Files/caseron.off')
    # viewer.delete_element(id_off)
    viewer.show()


def try_model():
    model = Model()
    mesh_1 = model.mesh_by_path('/home/gabriel/xyzrgb_statuette.off')
    input('memory 1 ?')
    mesh_2 = model.mesh_by_path('/home/gabriel/xyzrgb_statuette.off')
    input('memory 1 + 2?')
    model.delete(mesh_1.id)
    input('memory 2 - 1?')
    model.delete(mesh_2.id)
    input('memory with no meshes?')


def try_element():
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


def try_mesh():
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


def try_block_model():
    viewer = MineVisViewer()
    id_csv = viewer.add_block_model('Model/BlockModel/complex.csv')
    bm = viewer.model.get_block_model(id_csv)
    bm.set_value_string('Au')
    bm.update_values()
    viewer.show()


if __name__ == '__main__':
    try_viewer()
