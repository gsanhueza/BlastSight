#!/usr/bin/env python

#  Copyright (c) 2019-2023 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtGui import QColor
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QTreeWidgetItem

from .customwidgets.colordialog import ColorDialog
from .dialogs.propertiesdialog import PropertiesDialog


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, drawable=None):
        super().__init__(parent)
        self.drawable = drawable

        self.setText(0, f'{drawable.name}.{drawable.extension} (id: {drawable.id})')
        self.set_visible(drawable.is_visible)

    @property
    def id(self) -> int:
        return self.drawable.id

    def set_visible(self, is_visible: bool) -> None:
        font = QFont()
        font.setBold(is_visible)
        font.setItalic(not is_visible)
        self.setFont(0, font)

    def show(self) -> None:
        self.drawable.show()
        self.set_visible(self.drawable.is_visible)

    def hide(self) -> None:
        self.drawable.hide()
        self.set_visible(self.drawable.is_visible)

    def toggle_highlighting(self) -> None:
        self.drawable.toggle_highlighting()

    def toggle_wireframe(self) -> None:
        self.drawable.toggle_wireframe()

    def toggle_visibility(self) -> None:
        self.drawable.toggle_visibility()
        self.set_visible(self.drawable.is_visible)

    """
    Element properties handling
    """
    def update_color(self, viewer, color: iter) -> None:
        viewer.get_drawable(self.id).rgba = color
        viewer.update_drawable(self.id)

    def handle_color(self, viewer) -> None:
        element = viewer.get_drawable(self.id)

        dialog = ColorDialog()
        dialog.setCurrentColor(QColor.fromRgbF(*element.rgba))
        dialog.accepted.connect(lambda: self.update_color(viewer, dialog.currentColor().getRgbF()))
        dialog.show()

    def handle_properties(self, viewer) -> None:
        element = viewer.get_drawable(self.id)
        dialog = PropertiesDialog()
        dialog.setWindowTitle(f'Set properties ({element.name}.{element.extension})')

        # Fill headers and set current ones
        dialog.fill_headers(element.all_headers)
        dialog.set_current_headers(element.headers)

        # Fill properties
        dialog.set_alpha(element.alpha)
        dialog.set_colormap(element.colormap)
        dialog.set_vmin(element.vmin)
        dialog.set_vmax(element.vmax)

        if hasattr(element, 'marker'):
            # PointElement
            dialog.use_for_points()
            dialog.fill_markers(['square', 'sphere', 'circle'])
            dialog.set_marker(element.marker)
            dialog.set_point_size(element.avg_size)
        else:
            # BlockElement
            dialog.use_for_blocks()
            dialog.set_block_size(element.size.tolist())

        def has_altered_coordinates() -> bool:
            return any(map(lambda x, y: x != y, element.headers[:3], dialog.get_current_headers()[:3]))

        def update_properties() -> None:
            # Update headers
            altered_coordinates = has_altered_coordinates()
            element.headers = dialog.get_current_headers()

            # Update properties
            element.alpha = dialog.get_alpha()
            element.colormap = dialog.get_colormap()

            # Update limits
            if dialog.is_recalculate_checked():
                element.recalculate_limits()
            else:
                element.vmin = dialog.get_vmin()
                element.vmax = dialog.get_vmax()

                # Update sizes
                if hasattr(element, 'block_size'):
                    element.block_size = dialog.get_block_size()
                else:
                    element.avg_size = dialog.get_point_size()

            # Update marker
            if hasattr(element, 'marker'):
                element.marker = dialog.get_marker()

            # If coordinates were altered, call fit_to_screen()
            if altered_coordinates:
                viewer.fit_to_screen()

            # Finally, recreate instance with the "new" data
            viewer.update_drawable(element.id)

        dialog.accepted.connect(update_properties)
        dialog.show()
