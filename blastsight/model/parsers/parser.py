#!/usr/bin/env python

#  Copyright (c) 2019-2020 Gabriel Sanhueza.
#
#  Distributed under the MIT License.
#  See LICENSE for more info.


class Parser:
    @staticmethod
    def load_file(path: str, *args, **kwargs) -> dict:
        raise NotImplementedError

    @staticmethod
    def save_file(path: str, *args, **kwargs) -> None:
        raise NotImplementedError
