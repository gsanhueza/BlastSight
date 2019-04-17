#!/usr/bin/env python


def main_pyqt5():
    import sys

    from PyQt5.QtWidgets import QApplication
    from View.mainwindow import MainWindow
    from Model.model import Model

    # Qt Application
    qt_app = QApplication(sys.argv)

    model = Model()
    model.add_mesh('Model/Mesh/caseron.off')
    window = MainWindow()
    window.set_model(model)

    window.show()
    sys.exit(qt_app.exec_())


def main_pyside2():
    import sys

    from PySide2.QtWidgets import QApplication
    from PySide2.QtUiTools import QUiLoader
    from Model.model import Model
    from View.openglwidget import OpenGLWidget
    from View.mainwindow import MainWindow

    # Qt Application
    qt_app = QApplication(sys.argv)

    model = Model()

    # Dynamic UI loading
    loader = QUiLoader()
    loader.registerCustomWidget(MainWindow)
    loader.registerCustomWidget(OpenGLWidget)

    window = loader.load('View/UI/mainwindow.ui')
    # window.ready()
    window.show()

    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main_pyqt5()
    # main_pyside2()
