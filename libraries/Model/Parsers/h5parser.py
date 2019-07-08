#!/usr/bin/env python

import h5py


# http://tdeboissiere.github.io/h5py-vs-npz.html
class H5Parser:
    @staticmethod
    def load_file(file_path: str) -> tuple:
        assert file_path.lower().endswith('h5')

        hf = h5py.File(file_path, "r")
        vertices = hf['vertices'][()]
        indices = hf['indices'][()]
        hf.close()

        return vertices, indices

    @staticmethod
    def save_file(vertices, indices, file_path: str) -> None:
        hf = h5py.File(f'{file_path}.h5', "w")
        hf.create_dataset("vertices", data=vertices, dtype='float32')
        hf.create_dataset("indices", data=indices, dtype='uint32')
        hf.close()
