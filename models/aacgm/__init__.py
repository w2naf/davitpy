"""
*********************
**Module**: models.aacgm
*********************
"""
try:
    from aacgm2_davitpy import aacgm2_convert
    from aacgm2_davitpy import aacgmConv
except Exception, e:
    print __file__+' -> aacgm: ', e
