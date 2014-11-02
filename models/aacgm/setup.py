from distutils.core import setup, Extension
setup(name='aacgm2', version='1.0', ext_modules=[Extension('aacgm2',
    ['aacgmlib_v2_py.c', 'aacgmlib_v2.c','AstAlg.c'])])
