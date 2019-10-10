#!/usr/bin/env python

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can use the signals of the viewer.
"""

v = Viewer()
title = v.windowTitle()
v.setWindowTitle(f'{title} - Double click in a mesh.')
v.mesh_by_path('../test_files/caseron.off')


def update_info(x: list):
    update_title = []
    for d in v.drawable_collection.values():
        d.is_highlighted = False

    for attr in x:
        _id = attr.get('id')
        name = attr.get('name')

        v.get_drawable(_id).is_highlighted = True
        update_title.append(name)

    v.setWindowTitle(f'{title} - {update_title}')
    print(f'Attributes list: {x}')


"""
For example, you may want to do something when we detect a clicked mesh.
For that, just connect the signal to your function/method.
Check IntegrableViewer's code to know which signals are available.
"""
v.signal_mesh_clicked.connect(update_info)

v.fit_to_screen()
v.show()
