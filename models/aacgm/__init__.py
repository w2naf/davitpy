"""
*********************
**Module**: models.aacgm
*********************
"""
try:
    from aacgm2_davitpy import aacgm2_convert, aacgm2_convert_mlt
    from aacgm2_davitpy import aacgmConv, aacgmConvArr, mltFromYmdhms
except Exception, e:
    print __file__+' -> aacgm: ', e
