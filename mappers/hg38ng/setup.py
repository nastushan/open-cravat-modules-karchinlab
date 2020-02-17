from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='hg38ng', 
    ext_modules=cythonize(
        'hg38ng.pyx', 
        compiler_directives={'language_level': '3'}
    )
)
