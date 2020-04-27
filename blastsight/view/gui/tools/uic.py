#!/usr/bin/env python

"""
Adapted from https://github.com/mottosso/Qt.py

Dynamically loads an UI file using either PyQt5 or PySide2.
At least works better than qtpy for the PySide2 binding.
"""


def loadUi(uifile, baseinstance=None):
    try:
        # Return PyQt5.ui.loadUi directly
        from PyQt5 import uic

        return uic.loadUi(uifile, baseinstance)
    except (ImportError, TypeError):
        # Implement `PyQt5.uic.loadUi` for PySide(2)

        # ImportError: We'll use PySide2 because PyQt5 is not installed.
        # TypeError: We'll use PySide2 because the code uses it, but PyQt5 is also installed.

        import os
        import importlib

        from PySide2.QtUiTools import QUiLoader
        from PySide2 import QtCore
        from PySide2 import QtWidgets
        from xml.etree import ElementTree
        from io import StringIO

        class _UiLoader(QUiLoader):
            """Create the user interface in a base instance.

            Unlike `QUiLoader` itself this class does not
            create a new instance of the top-level widget, but creates the user
            interface in an existing instance of the top-level class if needed.

            This mimics the behaviour of `PyQt5.uic.loadUi`.

            """

            def __init__(self, baseinstance):
                super(_UiLoader, self).__init__(baseinstance)
                self.baseinstance = baseinstance
                self.custom_widgets = {}

            def _loadCustomWidgets(self, etree):
                """
                Workaround to pyside-77 bug.

                From QUiLoader doc we should use registerCustomWidget method.
                But this causes a segfault on some platforms.

                Instead we fetch from customwidgets DOM node the python class
                objects. Then we can directly use them in createWidget method.
                """

                def headerToModule(header):
                    """
                    Translate a header file to python module path
                    foo/bar.h => foo.bar
                    """
                    # Remove header extension
                    module = os.path.splitext(header)[0]

                    # Replace os separator by python module separator
                    return module.replace("/", ".").replace("\\", ".")

                custom_widgets = etree.find("customwidgets")

                if custom_widgets is None:
                    return

                for custom_widget in custom_widgets:
                    class_name = custom_widget.find("class").text
                    header = custom_widget.find("header").text
                    module = importlib.import_module(headerToModule(header))
                    self.custom_widgets[class_name] = getattr(module, class_name)

            def load(self, uifile, *args, **kwargs):
                from xml.etree.ElementTree import ElementTree

                # For whatever reason, if this doesn't happen then
                # reading an invalid or non-existing .ui file throws
                # a RuntimeError.
                etree = ElementTree()
                etree.parse(uifile)
                self._loadCustomWidgets(etree)

                widget = QUiLoader.load(self, uifile, *args, **kwargs)

                # Workaround for PySide 1.0.9, see issue #208
                widget.parentWidget()

                return widget

            def createWidget(self, class_name, parent=None, name=""):
                """Called for each widget defined in ui file

                Overridden here to populate `baseinstance` instead.

                """

                if parent is None and self.baseinstance:
                    # Supposed to create the top-level widget,
                    # return the base instance instead
                    return self.baseinstance

                # For some reason, Line is not in the list of available
                # widgets, but works fine, so we have to special case it here.
                if class_name in self.availableWidgets() + ["Line"]:
                    # Create a new widget for child widgets
                    widget = QUiLoader.createWidget(self, class_name, parent, name)
                elif class_name in self.custom_widgets:
                    widget = self.custom_widgets[class_name](parent)
                else:
                    raise Exception("Custom widget '%s' not supported"
                                    % class_name)

                if self.baseinstance:
                    # Set an attribute for the new child widget on the base
                    # instance, just like PyQt5.uic.loadUi does.
                    setattr(self.baseinstance, name, widget)

                return widget

        widget = _UiLoader(baseinstance).load(uifile)
        QtCore.QMetaObject.connectSlotsByName(widget)

        return widget
