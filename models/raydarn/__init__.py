# Copyright (C) 2012  VT SuperDARN Lab
# Full license can be found in LICENSE.txt
"""
*********************
**Module**: models.raydarn
*********************
This module wraps the ray-tracing coupled with IRI and IGRF

**Modules**
    * :mod:`models.raydarn.rt`: 

"""
try: from rt import *
except Exception, e:
    print __file__+' -> models.raydarn.rt: ', e
