#!/usr/bin/env python

from blastsight.view.viewer import Viewer

"""
In this demo, we'll show basic capabilities of BlastSight.
This demo is useful as a quick reference.
"""


def demo():
    viewer = Viewer()
    viewer.setWindowTitle('BlastSight (Demo)')

    """
    You can load a mesh with viewer.mesh().
    The minimum arguments needed are: x, y, z, indices.

    The color will be random unless you specify it with an RGB array.
    """
    viewer.mesh(x=[1, 3, 2],
                y=[0, 0, 1],
                z=[-3, -3, -3],
                color=[0.0, 0.0, 1.0],
                indices=[[0, 1, 2]],
                alpha=0.7,
                name='Normal Mesh')

    """
    Alternatively, you can use the arguments: vertices, indices
    You can load it directly as a wireframe, if you want.
    """
    viewer.mesh(vertices=[[1, 0, -3], [3, 0, -3], [2, -1, -3]],
                color=[1.0, 0.5, 0.0],
                indices=[[0, 1, 2]],
                alpha=1.0,
                wireframe=True,
                name='Wireframed Mesh')

    """
    A highlighted mesh renders as both a normal mesh and a wireframed mesh.
    """
    viewer.mesh(x=[-3, -1, -2, -2],
                y=[0, 0, 1, -1],
                z=[-3, -3, -3, -3],
                color=[1.0, 0.5, 0.5],
                indices=[[0, 1, 2], [0, 3, 1]],
                alpha=1.0,
                highlight=True,
                name='Highlighted Mesh')

    """
    You can load a set of blocks with viewer.blocks().
    Each value is mapped with the respective vertex.
    The arguments vmin, vmax and colormap are optional.

    The colormap is two colors separated with a`-`.
    Alternatively, you can pass an HTML color, like
    "#FF0000-#00FF00", as long as it's separated
    by the `-` character.
    """
    viewer.blocks(x=[-4, 4, 0],
                  y=[0, 0, 5],
                  z=[0, 0, 0],
                  block_size=[1.0, 1.0, 1.0],
                  values=[0.5, 1.0, 1.5],
                  vmin=0.5,
                  vmax=1.5,
                  colormap='red-blue',
                  name='Blocks')

    """
    You can load a set of blocks with viewer.points().
    Points and blocks receive the same arguments,
    except block_size (a point has point_size).
    You can also omit pass colors instead of values.

    If you're manually setting the colors, the `colormap`
    argument will be ignored.
    """
    viewer.points(vertices=[[-3, 2, 0], [0, 2, 1], [3, 2, 0]],
                  point_size=1.0,
                  color=[[1.0, 1.0, 0.0],
                         [0.0, 1.0, 1.0],
                         [1.0, 0.0, 1.0]],
                  marker='square',
                  name='Points rendered as squares')

    """
    You can also set multiple sizes for the points.
    If you pass an array instead of a float in the point_size argument,
    each point from vertices (or x, y, z) will have that particular size.
    """
    viewer.points(vertices=[[-2, 3, 1], [0, 3, 0], [2, 3, 1]],
                  point_size=[0.3, 0.6, 0.9],
                  color=[[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.0, 1.0]],
                  marker='circle',
                  name='Points rendered as circles')

    """
    As you noticed in the `marker` argument, you can have more than
    one point marker.
    Currently the markers are:
    - square: Squares that always face the camera.
    - circle: Circles that always face the camera.
    - sphere: Circles with a 3D effect.
    """
    viewer.points(vertices=[[-3, 5, 0], [3, 5, 0]],
                  point_size=2.0,
                  color=[[0.8, 0.5, 0.2],
                         [0.5, 0.2, 0.8]],
                  marker='sphere',
                  name='Points rendered as spheres')

    """
    You can load a set of blocks with viewer.lines().
    You need at least two vertices.

    If you need to join the first and the last vertex
    to form a loop, pass `loop=True` as argument.
    """
    viewer.lines(x=[-1.0, 1.0, -1.0, 1.0],
                 y=[1.0, 1.0, -1.0, -1.0],
                 z=[-2.0, -2.0, -2.0, -2.0],
                 color=[0.2, 0.8, 0.8],
                 loop=True,
                 name='Lines')

    """
    A tube is practically the same as a line, except
    that you can set the tube's radius and resolution
    (quality of the tube).
    """
    viewer.tubes(x=[1.0, -1.0, 1.0, -1.0],
                 y=[2.0, 2.0, -2.0, -2.0],
                 z=[-1.5, -1.5, -1.5, -1.5],
                 color=[0.9, 0.2, 0.2],
                 radius=0.2,
                 resolution=150,
                 loop=False,
                 name='Tubes')

    """
    A clever calculation with the bounding boxes of all the
    visible elements allows you to set the camera far enough
    that you can see every element on the screen without
    even showing the window.

    This method sets the world rotation at the center of the
    bounding box of all the visible elements.

    You might want to set the viewer's size before calling this
    method. (E.g.: viewer.resize(800, 600))
    """
    viewer.fit_to_screen()

    """
    Every drawable can be accessed in the viewer.drawable_collection dict.
    """
    for _id, drawable in viewer.drawable_collection.items():
        print(f'ID: {_id}\t Type: {type(drawable)}\t Name: {drawable.name}')

    """
    Finally, you can show the viewer with all the elements.
    """
    viewer.show()


if __name__ == '__main__':
    demo()
