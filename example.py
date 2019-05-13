#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.openglwidget import OpenGLWidget


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
    id_off = viewer.add_mesh('/home/gabriel/xyzrgb_statuette.off')
    viewer.delete_mesh(id_off)
    viewer.show()


def test_block_model():
    viewer = MineVisViewer()
    id_csv = viewer.add_block_model('Model/BlockModel/complex.csv')
    bm = viewer.model.get_block_model(id_csv)
    bm.set_value_string('Au')
    bm.update_values()
    viewer.show()


if __name__ == '__main__':
    test_block_model()
