#!/usr/bin/env python

import pathlib

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show how you can create a basic animation.

An animation is interpreted as changing the state of the viewer one frame at the time.
That means we'll define a function that makes a change in one single frame.
The function must receive a single argument, of the same type of the 'start' and 'end' values.
"""

v = Viewer()
path = f'{pathlib.Path(__file__).parent.parent}/test_files/caseron.off'
mesh = v.load_mesh(path, highlight=True)


def autorotate(angle):
    v.set_rotation_angle([0.0, -angle, 0.0])


"""
The animate() method receives a 'start' value, an 'end' value, a 'method' (the function that changes
one frame in the viewer), and two optional kwargs: 'milliseconds' (how much time should the
animation last) and 'steps' (smoothness of the animation depends on this).
"""

# Start animation
v.animate(0, 360, autorotate, milliseconds=3000, steps=100)

# Show viewer
v.show()
