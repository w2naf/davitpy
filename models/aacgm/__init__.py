"""
*********************
**Module**: models.aacgm
*********************
"""
try:
    from aacgm2 import *
except Exception, e:
    print __file__+' -> aacgm: ', e
