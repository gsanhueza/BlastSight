#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can use the signals of the viewer.
"""

v = Viewer()

title = v.windowTitle()
v.setWindowTitle(f'{title} - Double click in a mesh.')

path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
v.load_mesh(path)


def update_info(x: list):
    update_title = []
    for d in v.get_all_drawables():
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
v.signal_elements_detected.connect(update_info)

v.show()
