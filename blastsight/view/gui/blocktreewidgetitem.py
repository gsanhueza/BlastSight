#!/usr/bin/env python

#  Copyright (c) 2019-2024 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

from qtpy.QtWidgets import QMenu

from .actioncollection import ActionCollection
from .dialogs.propertiesdialog import PropertiesDialog
from .treewidgetitem import TreeWidgetItem


class BlockTreeWidgetItem(TreeWidgetItem):
    def __init__(self, parent=None, drawable=None):
        super().__init__(parent, drawable)

    """
    Element properties handling
    """
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

    """
    Context menu
    """
    def generate_context_menu(self, viewer, tree) -> QMenu:
        menu = QMenu()
        actions = ActionCollection(tree)

        menu.addAction(actions.action_show)
        menu.addAction(actions.action_hide)
        menu.addAction(actions.action_focus_camera)
        menu.addSeparator()

        menu.addAction(actions.action_properties)
        menu.addSeparator()

        menu.addAction(actions.action_export_element)
        menu.addAction(actions.action_delete)

        self.connect_actions(actions, viewer, tree)
        return menu

    """
    Actions
    """
    def connect_actions(self, actions: list, viewer, tree) -> None:
        super().connect_actions(actions, viewer, tree)
        actions.action_properties.triggered.connect(lambda: self.handle_properties(viewer))
