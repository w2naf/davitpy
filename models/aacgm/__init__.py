"""
*********************
**Module**: models.aacgm

This is C-based python extension module for AACGM version 2.
Please see DOI: 10.1002/2014JA020264 for more details.
*********************
"""
try:
    from aacgm2_davitpy import aacgm2_convert, aacgm2_convert_mlt

    #Legacy functions
    from aacgm2_davitpy import aacgmConv, aacgmConvArr, mltFromYmdhms, mltFromEpoch, mltFromYrsec
except Exception, e:
    print __file__+' -> aacgm: ', e
