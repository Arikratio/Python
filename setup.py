from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.extension import Extension
import numpy

setup(
    ext_modules = cythonize("cythv.pyx"),
    include_dirs=[numpy.get_include()]
)