#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtCore import Qt
from qtpy.QtWidgets import *
from qtpy.QtGui import *

from ..customwidgets.coloredbutton import ColoredButton
from ..customwidgets.colordialog import ColorDialog
from ..customwidgets.doublespinbox import DoubleSpinBox
from ..customwidgets.separatorframe import SeparatorFrame


class PropertiesDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(360, 440)
        self.resize(360, 440)

        # Labels (top)
        self.label_x = QLabel('X coordinate')
        self.label_y = QLabel('Y coordinate')
        self.label_z = QLabel('Z coordinate')
        self.label_value = QLabel('Current value')

        # Comboboxes (top)
        self.comboBox_x = QComboBox(self)
        self.comboBox_y = QComboBox(self)
        self.comboBox_z = QComboBox(self)
        self.comboBox_value = QComboBox(self)

        # Line separator
        self.line = SeparatorFrame(self)

        # Labels (bottom)
        self.label_alpha = QLabel('Alpha')
        self.label_vmin = QLabel('Min value')
        self.label_vmax = QLabel('Max value')
        self.label_colormap = QLabel('Colormap')
        self.label_blocksize = QLabel('Block size')
        self.label_pointsize = QLabel('Point size')
        self.label_markers = QLabel('Markers')
        self.label_recalculate = QLabel('Re-calculate limits')

        # Right column (Spinbox/buttons/etc) (bottom)
        self.doubleSpinBox_alpha = DoubleSpinBox(self, lower=0.0, upper=1.0, step=0.1)
        self.doubleSpinBox_vmin = DoubleSpinBox(self)
        self.doubleSpinBox_vmax = DoubleSpinBox(self)

        # Colormap
        self.pushButton_color_low = ColoredButton(self, 'Low', (1.0, 0.0, 0.0, 1.0))
        self.pushButton_color_low.clicked.connect(self.show_colordialog_low)

        self.pushButton_color_high = ColoredButton(self, 'High', (0.0, 0.0, 1.0, 1.0))
        self.pushButton_color_high.clicked.connect(self.show_colordialog_high)

        self.doubleSpinBox_pointsize = DoubleSpinBox(self, lower=0.0)
        self.comboBox_markers = QComboBox(self)

        # Block size
        self.doubleSpinBox_xsize = DoubleSpinBox(self, lower=0.0)
        self.doubleSpinBox_ysize = DoubleSpinBox(self, lower=0.0)
        self.doubleSpinBox_zsize = DoubleSpinBox(self, lower=0.0)

        # Recalculate
        self.checkBox_recalculate = QCheckBox('Enable auto-calculation', self)

        # ButtonBox (Accept/Reject)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Layouts
        self.verticalLayout = QVBoxLayout(self)
        self.gridLayout_top = QGridLayout()
        self.gridLayout_bottom = QGridLayout()
        self.horizontalLayout_colormap = QHBoxLayout()
        self.horizontalLayout_blocksize = QHBoxLayout()

        # Accomodate labels (top)
        self.gridLayout_top.addWidget(self.label_x, 0, 0, 1, 1)
        self.gridLayout_top.addWidget(self.label_y, 1, 0, 1, 1)
        self.gridLayout_top.addWidget(self.label_z, 2, 0, 1, 1)
        self.gridLayout_top.addWidget(self.label_value, 3, 0, 1, 1)

        # Accomodate comboboxes (top)
        self.gridLayout_top.addWidget(self.comboBox_x, 0, 1, 1, 1)
        self.gridLayout_top.addWidget(self.comboBox_y, 1, 1, 1, 1)
        self.gridLayout_top.addWidget(self.comboBox_z, 2, 1, 1, 1)
        self.gridLayout_top.addWidget(self.comboBox_value, 3, 1, 1, 1)

        # Top grid stretching
        self.gridLayout_top.setColumnStretch(0, 1)
        self.gridLayout_top.setColumnStretch(1, 2)

        # Accomodate labels (bottom)
        self.gridLayout_bottom.addWidget(self.label_alpha, 0, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_vmin, 1, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_vmax, 2, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_colormap, 3, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_blocksize, 4, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_pointsize, 5, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_markers, 6, 0, 1, 1)
        self.gridLayout_bottom.addWidget(self.label_recalculate, 7, 0, 1, 1)

        # Accomodate block sizes
        self.horizontalLayout_blocksize.addWidget(self.doubleSpinBox_xsize)
        self.horizontalLayout_blocksize.addWidget(self.doubleSpinBox_ysize)
        self.horizontalLayout_blocksize.addWidget(self.doubleSpinBox_zsize)

        # Accomodate colormap buttons
        self.horizontalLayout_colormap.addWidget(self.pushButton_color_low)
        self.horizontalLayout_colormap.addWidget(self.pushButton_color_high)

        # Accomodate right column (bottom)
        self.gridLayout_bottom.addWidget(self.doubleSpinBox_alpha, 0, 1, 1, 1)
        self.gridLayout_bottom.addWidget(self.doubleSpinBox_vmin, 1, 1, 1, 1)
        self.gridLayout_bottom.addWidget(self.doubleSpinBox_vmax, 2, 1, 1, 1)
        self.gridLayout_bottom.addLayout(self.horizontalLayout_colormap, 3, 1, 1, 1)
        self.gridLayout_bottom.addLayout(self.horizontalLayout_blocksize, 4, 1, 1, 1)
        self.gridLayout_bottom.addWidget(self.doubleSpinBox_pointsize, 5, 1, 1, 1)
        self.gridLayout_bottom.addWidget(self.comboBox_markers, 6, 1, 1, 1)
        self.gridLayout_bottom.addWidget(self.checkBox_recalculate, 7, 1, 1, 1)

        # Bottom grid stretching
        self.gridLayout_bottom.setColumnStretch(0, 1)
        self.gridLayout_bottom.setColumnStretch(1, 2)

        # Accomodate general layout
        self.verticalLayout.addLayout(self.gridLayout_top)
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout.addLayout(self.gridLayout_bottom)
        self.verticalLayout.addWidget(self.buttonBox)

        # Signal handling for limits checkbox
        def handle_limits_enabled(status: bool) -> None:
            self.doubleSpinBox_vmin.setDisabled(status)
            self.doubleSpinBox_vmax.setDisabled(status)
            self.doubleSpinBox_xsize.setDisabled(status)
            self.doubleSpinBox_ysize.setDisabled(status)
            self.doubleSpinBox_zsize.setDisabled(status)

        # Connect auto-calculate limits
        self.checkBox_recalculate.clicked.connect(handle_limits_enabled)

        self.label_markers.setVisible(False)
        self.comboBox_markers.setVisible(False)

    def show_colordialog_low(self) -> None:
        dialog = ColorDialog()
        dialog.setCurrentColor(self.pushButton_color_low.qcolor)
        dialog.accepted.connect(lambda *_: self.pushButton_color_low.set_qcolor(dialog.currentColor()))
        dialog.show()

    def show_colordialog_high(self) -> None:
        dialog = ColorDialog()
        dialog.setCurrentColor(self.pushButton_color_high.qcolor)
        dialog.accepted.connect(lambda *_: self.pushButton_color_high.set_qcolor(dialog.currentColor()))
        dialog.show()

    def use_for_blocks(self, value: bool = True) -> None:
        # Show widgets related to Blocks
        self.label_blocksize.setVisible(value)
        self.doubleSpinBox_xsize.setVisible(value)
        self.doubleSpinBox_ysize.setVisible(value)
        self.doubleSpinBox_zsize.setVisible(value)

        # Hide widgets related to Points
        self.label_markers.setVisible(not value)
        self.comboBox_markers.setVisible(not value)
        self.label_pointsize.setVisible(not value)
        self.doubleSpinBox_pointsize.setVisible(not value)

    def use_for_points(self, value: bool = True) -> None:
        self.use_for_blocks(not value)

    def fill_headers(self, headers: list) -> None:
        for header in headers:
            self.comboBox_x.addItem(header)
            self.comboBox_y.addItem(header)
            self.comboBox_z.addItem(header)
            self.comboBox_value.addItem(header)

    def fill_markers(self, markers: list):
        for marker in markers:
            self.comboBox_markers.addItem(marker)

    """
    Getters/Setters
    """
    def get_current_headers(self) -> list:
        return [self.comboBox_x.currentText(),
                self.comboBox_y.currentText(),
                self.comboBox_z.currentText(),
                self.comboBox_value.currentText()]

    def get_alpha(self) -> float:
        return self.doubleSpinBox_alpha.value()

    def get_colormap(self) -> str:
        color_low = self.pushButton_color_low.qcolor.name()
        color_high = self.pushButton_color_high.qcolor.name()
        return f'{color_low}-{color_high}'

    def get_vmin(self) -> float:
        return self.doubleSpinBox_vmin.value()

    def get_vmax(self) -> float:
        return self.doubleSpinBox_vmax.value()

    def get_block_size(self) -> list:
        return [self.doubleSpinBox_xsize.value(),
                self.doubleSpinBox_ysize.value(),
                self.doubleSpinBox_zsize.value()]

    def get_point_size(self) -> float:
        return self.doubleSpinBox_pointsize.value()

    def get_marker(self) -> str:
        return self.comboBox_markers.currentText()

    def is_recalculate_checked(self) -> bool:
        return self.checkBox_recalculate.isChecked()

    def set_current_headers(self, headers: list) -> None:
        self.comboBox_x.setCurrentIndex(self.comboBox_x.findText(headers[0]))
        self.comboBox_y.setCurrentIndex(self.comboBox_y.findText(headers[1]))
        self.comboBox_z.setCurrentIndex(self.comboBox_z.findText(headers[2]))
        self.comboBox_value.setCurrentIndex(self.comboBox_value.findText(headers[3]))

    def set_alpha(self, value: float) -> None:
        return self.doubleSpinBox_alpha.setValue(value)

    def set_colormap(self, value: str) -> None:
        low, high = value.split('-')
        self.pushButton_color_low.set_color(QColor(low).getRgbF())
        self.pushButton_color_high.set_color(QColor(high).getRgbF())

    def set_vmin(self, value: float) -> None:
        self.doubleSpinBox_vmin.setValue(value)

    def set_vmax(self, value: float) -> None:
        self.doubleSpinBox_vmax.setValue(value)

    def set_block_size(self, value: list) -> None:
        self.doubleSpinBox_xsize.setValue(value[0])
        self.doubleSpinBox_ysize.setValue(value[1])
        self.doubleSpinBox_zsize.setValue(value[2])

    def set_point_size(self, value: float) -> None:
        self.doubleSpinBox_pointsize.setValue(value)

    def set_marker(self, value: str) -> None:
        self.comboBox_markers.setCurrentIndex(self.comboBox_markers.findText(value))
