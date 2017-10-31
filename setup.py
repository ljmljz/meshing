from distutils.core import setup, Extension
import os, sys
import site

ext_modules = [
    Extension(
        'meshing._geometry',
        sources=['meshing/src/wrapper.cpp'],
        libraries=['python2.7'],
        include_dirs=[
            'meshing/src',
            '/user/local/include',
            os.path.join(sys.prefix, 'include'),
            os.path.join(site.getsitepackages()[0], 'numpy', 'core', 'include')
        ],
        library_dirs=[os.path.join(sys.prefix, 'lib')],
        extra_compile_args=['-std=c++11']
    )
]

setup(
    name="meshing",
    version="0.1",
    description="A library for meshing. Supporting triangulation, extrusion, translation, scale and rotation etc.",
    author="Jimmy Li",
    author_email="ljzljm@163.com",
    url="https://github.com/ljmljz/meshing",
    license="MIT",
    packages=['meshing'],
    ext_modules = ext_modules
)