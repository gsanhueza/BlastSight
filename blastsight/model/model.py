#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.

import numpy as np
import warnings

from . import utils

from qtpy.QtCore import QDirIterator
from qtpy.QtCore import QFileInfo
from qtpy.QtCore import QMutex
from qtpy.QtCore import QMutexLocker

from .elementfactory import ElementFactory

from .elements.element import Element
from .elements.elementcollection import ElementCollection
from .elements.blockelement import BlockElement
from .elements.pointelement import PointElement
from .elements.lineelement import LineElement
from .elements.meshelement import MeshElement
from .elements.nullelement import NullElement
from .elements.tubeelement import TubeElement

from .parsers.parser import Parser
from .parsers.parsercollection import ParserCollection
from .parsers.dxfparser import DXFParser
from .parsers.offparser import OFFParser
from .parsers.h5mparser import H5MParser
from .parsers.h5pparser import H5PParser
from .parsers.csvparser import CSVParser
from .parsers.gslibparser import GSLibParser


class Model:
    def __init__(self):
        self._mutex = QMutex()
        self.parser_collection = ParserCollection()
        self.element_collection = ElementCollection()
        self.factory = ElementFactory()

        self.add_parser('dxf', DXFParser())
        self.add_parser('off', OFFParser())
        self.add_parser('h5m', H5MParser())
        self.add_parser('h5p', H5PParser())
        self.add_parser('csv', CSVParser())
        self.add_parser('out', GSLibParser())

    @property
    def last_id(self) -> int:
        return self.element_collection.last_id

    """
    Utilities
    """
    def add_parser(self, extension: str, handler: Parser) -> None:
        self.parser_collection.add(extension, handler)

    def get_parser(self, extension: str) -> Parser:
        return self.parser_collection.get(extension)

    @staticmethod
    def get_paths_from_directory(path: str) -> list:
        it = QDirIterator(path, QDirIterator.Subdirectories)
        path_list = []

        while it.hasNext():
            next_path = it.next()
            if QFileInfo(next_path).isFile():
                path_list.append(next_path)

        return sorted(path_list)

    """
    Register methods
    """
    def register_element(self, element):
        # In a multi-threaded application, we can't risk assigning
        # the same ID to different elements, so we use a mutex here.
        with QMutexLocker(self._mutex):
            self.element_collection.add(element)

        return element

    def register_element_by_path(self, path: str, generator, *args, **kwargs):
        ext = path.split('.')[-1]
        info = self.get_parser(ext).load_file(path, *args, **kwargs)
        data = info.data
        properties = info.properties

        # Prioritize kwargs over file properties (useful in CLI)
        kwargs['data'] = kwargs.get('data', data)
        for k, v in properties.items():
            kwargs[k] = kwargs.get(k, v)

        return self.register_element(generator(*args, **kwargs))

    """
    Load methods by arguments
    """
    def null(self, *args, **kwargs) -> NullElement:
        # A NullElement won't be registered
        return self.factory.null(*args, **kwargs)

    def mesh(self, *args, **kwargs) -> MeshElement:
        return self.register_element(self.factory.mesh(*args, **kwargs))

    def blocks(self, *args, **kwargs) -> BlockElement:
        return self.register_element(self.factory.blocks(*args, **kwargs))

    def points(self, *args, **kwargs) -> PointElement:
        return self.register_element(self.factory.points(*args, **kwargs))

    def lines(self, *args, **kwargs) -> LineElement:
        return self.register_element(self.factory.lines(*args, **kwargs))

    def tubes(self, *args, **kwargs) -> TubeElement:
        return self.register_element(self.factory.tubes(*args, **kwargs))

    """
    Load methods by path
    """
    def load_mesh(self, path: str, *args, **kwargs) -> MeshElement:
        return self.register_element_by_path(path, self.factory.mesh, *args, **kwargs)

    def load_blocks(self, path: str, *args, **kwargs) -> BlockElement:
        return self.register_element_by_path(path, self.factory.blocks, *args, **kwargs)

    def load_points(self, path: str, *args, **kwargs) -> PointElement:
        return self.register_element_by_path(path, self.factory.points, *args, **kwargs)

    def load_lines(self, path: str, *args, **kwargs) -> LineElement:
        return self.register_element_by_path(path, self.factory.lines, *args, **kwargs)

    def load_tubes(self, path: str, *args, **kwargs) -> TubeElement:
        return self.register_element_by_path(path, self.factory.tubes, *args, **kwargs)

    """
    Load methods by path (DEPRECATED)
    """
    def mesh_by_path(self, path: str, *args, **kwargs) -> MeshElement:
        warnings.warn('mesh_by_path() is deprecated. Use load_mesh() instead.', DeprecationWarning, 2)
        return self.load_mesh(path, *args, **kwargs)

    def blocks_by_path(self, path: str, *args, **kwargs) -> BlockElement:
        warnings.warn('blocks_by_path() is deprecated. Use load_blocks() instead.', DeprecationWarning, 2)
        return self.load_blocks(path, *args, **kwargs)

    def points_by_path(self, path: str, *args, **kwargs) -> PointElement:
        warnings.warn('points_by_path() is deprecated. Use load_points() instead.', DeprecationWarning, 2)
        return self.load_points(path, *args, **kwargs)

    def lines_by_path(self, path: str, *args, **kwargs) -> LineElement:
        warnings.warn('lines_by_path() is deprecated. Use load_lines() instead.', DeprecationWarning, 2)
        return self.load_lines(path, *args, **kwargs)

    def tubes_by_path(self, path: str, *args, **kwargs) -> TubeElement:
        warnings.warn('tubes_by_path() is deprecated. Use load_tubes() instead.', DeprecationWarning, 2)
        return self.load_tubes(path, *args, **kwargs)

    """
    Element handling
    """
    def get(self, _id: int) -> Element:
        return self.element_collection.get(_id)

    def delete(self, _id: int) -> None:
        self.element_collection.delete(_id)

    """
    Element exporting
    """
    def export(self, path: str, _id: int) -> None:
        element = self.get(_id)
        ext = path.split('.')[-1]

        data = element.data
        properties = {}
        for k in element.exportable_properties:
            properties[k] = getattr(element, k)

        self.get_parser(ext).save_file(path=path, data=data, properties=properties)

    def export_mesh(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_blocks(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_points(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_lines(self, path: str, _id: int) -> None:
        self.export(path, _id)

    def export_tubes(self, path: str, _id: int) -> None:
        self.export(path, _id)

    """
    Adapter for viewer's utilities (slice/distance)
    """
    @staticmethod
    def slice_meshes(origin: np.ndarray, normal: np.ndarray, meshes: list) -> list:
        """
        Returns a list of dicts, where each dict is the mesh ID and its sliced vertices
        """
        result = []

        for mesh in meshes:
            vertices = mesh.slice_with_plane(origin, normal)
            if len(vertices) > 0:
                result.append({'element_id': mesh.id,
                               'vertices': vertices,
                               })

        return result

    @staticmethod
    def slice_blocks(origin: np.ndarray, normal: np.ndarray, block_list: list) -> list:
        """
        Returns a list of dicts, where each dict is the block ID and its sliced indices
        """
        result = []

        for block in block_list:
            indices = block.slice_with_plane(origin, normal)
            if len(indices) > 0:
                result.append({
                    'element_id': block.id,
                    'indices': indices,
                })

        return result

    @staticmethod
    def measure_from_rays(origin_list: list, ray_list: list, meshes: list) -> dict:
        """
        Returns a dict with the following structure:

        {
            'point_a': list(float) or None,
            'point_b': list(float) or None',
            'distance': float or None
        }
        """
        points_A = []
        points_B = []

        closest_A = None
        closest_B = None

        # Detect intersections
        for mesh in meshes:
            int_A = mesh.intersect_with_ray(origin_list[0], ray_list[0])
            int_B = mesh.intersect_with_ray(origin_list[1], ray_list[1])

            # Discard non-intersections
            if int_A.size > 0:
                points_A.append(utils.closest_point_to(origin_list[0], int_A))

            if int_B.size > 0:
                points_B.append(utils.closest_point_to(origin_list[1], int_B))

        # Get closest points for each origin
        if len(points_A) > 0:
            points_A = np.vstack(points_A)
            closest_A = utils.closest_point_to(origin_list[0], points_A)

        if len(points_B) > 0:
            points_B = np.vstack(points_B)
            closest_B = utils.closest_point_to(origin_list[1], points_B)

        # Calculate distance if possible
        try:
            distance = np.linalg.norm(closest_B - closest_A)
        except TypeError:
            distance = None

        return {
            'point_a': closest_A,
            'point_b': closest_B,
            'distance': distance,
        }

    @staticmethod
    def detect_mesh_intersection(ray: np.ndarray, origin: np.ndarray, meshes: list) -> list:
        attributes_list = []

        for mesh in meshes:
            intersections = mesh.intersect_with_ray(origin, ray)
            closest_point = utils.closest_point_to(origin, intersections)
            if closest_point is not None:
                attributes = {**mesh.attributes,
                              'intersections': intersections,
                              'closest_point': closest_point,
                              }
                attributes_list.append(attributes)

        return attributes_list
