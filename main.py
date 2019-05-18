#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication
from View.GUI.minevis import MineVis

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MineVis()

    window.show()
    sys.exit(app.exec_())
