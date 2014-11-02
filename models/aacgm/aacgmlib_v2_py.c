#include <Python.h>
#include <math.h>
#include "aacgmlib_v2.h"

static PyObject *
aacgm2_AACGM_v2_Convert(PyObject *self, PyObject *args)
{
    double inlat, inlon, height, outLat, outLon, r;
    int flg;

    if(!PyArg_ParseTuple(args, "dddi", &inlat, &inlon, &height, &flg))
        return NULL;
    else
    {
        AACGM_v2_Convert(inlat,inlon,height,&outLat,&outLon,&r,flg);
        return Py_BuildValue("ddd",outLat,outLon,r);
    }
}

static PyObject *
aacgm2_AACGM_v2_SetDateTime(PyObject *self, PyObject *args)
{
    int year, month, day, hour, minute, second;

    if(!PyArg_ParseTuple(args, "iiiiii", &year, &month, &day, &hour, &minute, &second))
        return NULL;
    else
    {
        AACGM_v2_SetDateTime(year,month,day,hour,minute,second);
        Py_RETURN_NONE;
    }
}

static PyObject *
aacgm2_AACGM_v2_GetDateTime(PyObject *self, PyObject *args)
{
    int year, month, day, hour, minute, second, dayno;

    AACGM_v2_GetDateTime(&year,&month,&day,&hour,&minute,&second,&dayno);
    return Py_BuildValue("iiiiiii",year, month, day, hour, minute, second, dayno);
}

static PyObject *
aacgm2_AACGM_v2_SetNow(PyObject *self, PyObject *args)
{
    AACGM_v2_SetNow();
    Py_RETURN_NONE;
}


static PyObject *
aacgm2_AACGM_v2_ConvertMLT(PyObject *self, PyObject *args)
{
    double mlon,height,mlt,mslong;
    
    if(!PyArg_ParseTuple(args, "dd", &mlon, &height))
        return NULL;
    else
    { 
        AACGM_v2_ConvertMLT(mlon, height, &mlt, &mslong);
        return Py_BuildValue("dd",mlt,mslong);
    }
    
}

static PyMethodDef aacgmMethods[]=
{
    {"AACGM_v2_Convert", aacgm2_AACGM_v2_Convert, METH_VARARGS, "Convert to AACGM Coords\nlat, lon, r = AACGM_v2_Convert(inLat, inLon, height, flg)\nSet date and time with AACGM_v2_SetDateTime() or AACGM_v2_SetNow().\nHeight in km; flg=0: geo to aacgm; flg=1: aacgm to geo"},
    {"AACGM_v2_SetDateTime", aacgm2_AACGM_v2_SetDateTime, METH_VARARGS, "Set the date/time to be used by the AACGM library.\nAACGM_v2_SetDateTime(year,month,day,hour,minute,second)"},
    {"AACGM_v2_GetDateTime", aacgm2_AACGM_v2_GetDateTime, METH_NOARGS, "Returns the date/time currently used by AACGM in format (year, month, day, hour, minute, second, dayno)."},
    {"AACGM_v2_SetNow", aacgm2_AACGM_v2_SetNow, METH_NOARGS, "Sets the AACGM date/time to the current UT time.\nReturn None."},
    {"AACGM_v2_ConvertMLT", aacgm2_AACGM_v2_ConvertMLT, METH_VARARGS, "Calculate MLT from magnetic longitude [deg], height [km], and currently set AACGM time.\nAlso return Mean Solar Longitude.\nmlt,mslong=AACGM_v2_MLTConvert(mlon,height)"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC initaacgm2(void) {
    (void) Py_InitModule3("aacgm2", aacgmMethods,"Altitude Adjusted Corrected Geomagnetic Coordinate System Version 2 (AACGM_v2).\n(a.k.a. Again Adjusted Altitude Adjusted Corrected Geomagnetic Coordinate System (AAAACGM))\nFor details, see [Shepherd, 2014] at DOI: 10.1002/2014JA020264.");
}
