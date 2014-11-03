from datetime import datetime as dt
import numpy as np
import unittest
from models import aacgm

class DavitPyAacgmTest(unittest.TestCase):
    def setUp(self):
        self.accuracy = 6

        self.test_data = []
        #                      (     glat,       glon,      height,             datetime, flg,      mlat,       mlon,        r,      mlt,      mslong)
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(2014, 3,22, 3,11),   0, 48.377539,  57.822458, 1.000000, 2.092153, -153.559832) )
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 49.425800,  58.259686, 1.000000, 2.121862, -153.568237) )
        self.test_data.append( (65.500000,  93.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 62.251076, 166.990581, 1.000000, 9.370588, -153.568237) )
        self.test_data.append( (65.500000,  93.500000,           0, dt(1997, 3,22, 3,11),   0, 60.799240, 166.518084, 1.000000, 9.339088, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(1997, 3,22, 3,11),   0, 70.420669, 150.743259, 1.000000, 8.287433, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(2004, 3,22, 3,11),   0, 70.726381, 150.672892, 1.000000, 8.338513, -154.404804) )

    def test_aacgm2_convert_scalar(self):
        print('Testing the scalar functionality of aacgm2_convert.')

        for item in self.test_data:
            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = item

            mlat_test, mlon_test, r_test = aacgm.aacgm2_convert(glat,glon,height,dtime,flg)
            self.assertAlmostEqual(mlat_test,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test,mlon,self.accuracy)
            self.assertAlmostEqual(r_test,r,self.accuracy)

    def test_aacgm2_convert_lists(self):
        print('Testing the list functionality of aacgm2_convert.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

        mlat_test, mlon_test, r_test = aacgm.aacgm2_convert(glat,glon,height,dtime,flg)

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgm2_convert_numpy(self):
        print('Testing the 1d numpy array functionality of aacgm2_convert.')


        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

        mlat_test, mlon_test, r_test = aacgm.aacgm2_convert(np.array(glat),np.array(glon),np.array(height),np.array(dtime),np.array(flg))

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgm2_convert_scalar_date_height(self):
        print('Testing aacgm2_convert when in_lat and in_lon are lists, but date, height, and flg are scalars.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = self.test_data[0]

        glat = [glat] * 10
        glon = [glon] * 10

        mlat_test, mlon_test, r_test = aacgm.aacgm2_convert(glat,glon,height,dtime)

        for mlat_test_0,mlon_test_0,r_test_0 in zip(mlat_test,mlon_test,r_test):
            self.assertAlmostEqual(mlat_test_0,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon,self.accuracy)
            self.assertAlmostEqual(r_test_0,r,self.accuracy)

    def test_aacgm2_convert_mlt_scalar(self):
        print('Testing the scalar functionality of aacgm2_convert_mlt.')

        for item in self.test_data:
            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = item

            mlt_test, mslong_test = aacgm.aacgm2_convert_mlt(mlon,height,dtime,return_mslong=True)
            self.assertAlmostEqual(mlt_test,mlt,self.accuracy)
            self.assertAlmostEqual(mslong_test,mslong,self.accuracy)

    def test_aacgm2_convert_mlt_lists(self):
        print('Testing the list functionality of aacgm2_convert_mlt.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

        mlt_test, mslong_test = aacgm.aacgm2_convert_mlt(mlon,height,dtime,return_mslong=True)

        for mlt_test_0, mslong_test_0, mlt_0, mslong_0 in zip(mlt_test,mslong_test,mlt,mslong):
            self.assertAlmostEqual(mlt_test_0,mlt_0,self.accuracy)
            self.assertAlmostEqual(mslong_test_0,mslong_0,self.accuracy)

    def test_aacgm2_convert_mlt_numpy(self):
        print('Testing the 1d numpy array functionality of aacgm2_convert_mlt.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

        mlt_test, mslong_test = aacgm.aacgm2_convert_mlt(np.array(mlon),np.array(height),np.array(dtime),return_mslong=True)

        for mlt_test_0, mslong_test_0, mlt_0, mslong_0 in zip(mlt_test,mslong_test,mlt,mslong):
            self.assertAlmostEqual(mlt_test_0,mlt_0,self.accuracy)
            self.assertAlmostEqual(mslong_test_0,mslong_0,self.accuracy)

    def test_aacgm2_convert_mlt_scalar_date_height(self):
        print('Testing aacgm2_convert_mlt when in_lat and in_lon are lists, but date, height, and flg are scalars.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = self.test_data[0]

        mlon = [mlon] * 10

        mlt_test, mslong_test = aacgm.aacgm2_convert_mlt(mlon,height,dtime,return_mslong=True)

        for mlt_test_0, mslong_test_0 in zip(mlt_test,mslong_test):
            self.assertAlmostEqual(mlt_test_0,mlt,self.accuracy)
            self.assertAlmostEqual(mslong_test_0,mslong,self.accuracy)

class LegacyDavitPyAacgmTest(unittest.TestCase):
    """This tests the legacy DavitPy AACGM function calls.  The primary difference is that only the year is passed to AACGM_v2_Convert.
        January 1 at 0000 UT is assumed for all calls.
    """
       
    def setUp(self):
        self.accuracy = 6

        self.test_data = []
        #                      (     glat,       glon,      height,             datetime, flg,      mlat,       mlon,        r,      mlt,      mslong)
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(2014, 3,22, 3,11),   0, 48.392864,  57.824783, 1.000000, 2.092153, -153.559832) )
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 49.438045,  58.272636, 1.000000, 2.121862, -153.568237) )
        self.test_data.append( (65.500000,  93.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 62.242400, 166.986299, 1.000000, 9.370588, -153.568237) )
        self.test_data.append( (65.500000,  93.500000,           0, dt(1997, 3,22, 3,11),   0, 60.789785, 166.513080, 1.000000, 9.339088, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(1997, 3,22, 3,11),   0, 70.410507, 150.748819, 1.000000, 8.287433, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(2004, 3,22, 3,11),   0, 70.717087, 150.672864, 1.000000, 8.338513, -154.404804) )

    # Testing aacgmConv() ##########################################################
    def test_aacgmConv_scalar(self):
        print('Testing the scalar functionality of aacgmConv().')

        for item in self.test_data:
            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = item

            mlat_test, mlon_test, r_test = aacgm.aacgmConv(glat,glon,height,dtime.year,flg)
            self.assertAlmostEqual(mlat_test,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test,mlon,self.accuracy)
            self.assertAlmostEqual(r_test,r,self.accuracy)

    def test_aacgmConv_lists(self):
        print('Testing the list functionality of aacgmConv().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        year = [x.year for x in dtime]

        mlat_test, mlon_test, r_test = aacgm.aacgmConv(glat,glon,height,year,flg)

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgmConv_numpy(self):
        print('Testing the 1d numpy array functionality of aacgmConv().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        year = [x.year for x in dtime]

        mlat_test, mlon_test, r_test = aacgm.aacgmConv(np.array(glat),np.array(glon),np.array(height),np.array(year),np.array(flg))

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgmConv_scalar_date_height(self):
        print('Testing aacgmConv() when in_lat and in_lon are lists, but date, height, and flg are scalars.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = self.test_data[0]

        glat = [glat] * 10
        glon = [glon] * 10

        mlat_test, mlon_test, r_test = aacgm.aacgmConv(glat,glon,height,dtime.year)

        for mlat_test_0,mlon_test_0,r_test_0 in zip(mlat_test,mlon_test,r_test):
            self.assertAlmostEqual(mlat_test_0,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon,self.accuracy)
            self.assertAlmostEqual(r_test_0,r,self.accuracy)

    # Testing aacgmConvArr() #######################################################
    def test_aacgmConvArr_scalar(self):
        print('Testing the scalar functionality of aacgmConvArr().')

        for item in self.test_data:
            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = item

            mlat_test, mlon_test, r_test = aacgm.aacgmConvArr(glat,glon,height,dtime.year,flg)
            self.assertAlmostEqual(mlat_test,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test,mlon,self.accuracy)
            self.assertAlmostEqual(r_test,r,self.accuracy)

    def test_aacgmConvArr_lists(self):
        print('Testing the list functionality of aacgmConvArr().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        year = [x.year for x in dtime]

        mlat_test, mlon_test, r_test = aacgm.aacgmConvArr(glat,glon,height,year,flg)

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgmConvArr_numpy(self):
        print('Testing the 1d numpy array functionality of aacgmConvArr().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        year = [x.year for x in dtime]

        mlat_test, mlon_test, r_test = aacgm.aacgmConvArr(np.array(glat),np.array(glon),np.array(height),np.array(year),np.array(flg))

        for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
            self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
            self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

    def test_aacgmConvArr_scalar_date_height(self):
        print('Testing aacgmConvArr() when in_lat and in_lon are lists, but date, height, and flg are scalars.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = self.test_data[0]

        glat = [glat] * 10
        glon = [glon] * 10

        mlat_test, mlon_test, r_test = aacgm.aacgmConvArr(glat,glon,height,dtime.year)

        for mlat_test_0,mlon_test_0,r_test_0 in zip(mlat_test,mlon_test,r_test):
            self.assertAlmostEqual(mlat_test_0,mlat,self.accuracy)
            self.assertAlmostEqual(mlon_test_0,mlon,self.accuracy)
            self.assertAlmostEqual(r_test_0,r,self.accuracy)

class LegacyDavitPyAacgmMltTest(unittest.TestCase):
    def setUp(self):
        self.accuracy = 6

        self.test_data = []
        #                      (     glat,       glon,      height,             datetime, flg,      mlat,       mlon,        r,      mlt,      mslong)
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(2014, 3,22, 3,11),   0, 48.377539,  57.822458, 1.000000, 2.092153, -153.559832) )
        self.test_data.append( (45.500000, -23.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 49.425800,  58.259686, 1.000000, 2.121862, -153.568237) )
        self.test_data.append( (65.500000,  93.500000, 1135.000000, dt(1997, 3,22, 3,11),   0, 62.251076, 166.990581, 1.000000, 9.370588, -153.568237) )
        self.test_data.append( (65.500000,  93.500000,           0, dt(1997, 3,22, 3,11),   0, 60.799240, 166.518084, 1.000000, 9.339088, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(1997, 3,22, 3,11),   0, 70.420669, 150.743259, 1.000000, 8.287433, -153.568237) )
        self.test_data.append( (75.500000,  73.500000,           0, dt(2004, 3,22, 3,11),   0, 70.726381, 150.672892, 1.000000, 8.338513, -154.404804) )

    # Testing mltFromYmdhms() ######################################################
    def test_mltFromYmdhms_scalar(self):
        print('Testing the scalar functionality of mltFromYmdhms().')

        for item in self.test_data:
            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = item

            mlt_test = aacgm.mltFromYmdhms(dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second,mlon,height=height)
            self.assertAlmostEqual(mlt_test,mlt,self.accuracy)

    def test_mltFromYmdhms_lists(self):
        print('Testing the list functionality of mltFromYmdhms().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        
        year   = [x.year for x in dtime]
        month  = [x.month for x in dtime]
        day    = [x.day for x in dtime]
        hour   = [x.hour for x in dtime]
        minute = [x.minute for x in dtime]
        second = [x.second for x in dtime]

        mlt_test = aacgm.mltFromYmdhms(year,month,day,hour,minute,second,mlon,height=height)

        for mlt_test_0, mlt_0, in zip(mlt_test,mlt):
            self.assertAlmostEqual(mlt_test_0,mlt_0,self.accuracy)

    def test_mltFromYmdhms_numpy(self):
        print('Testing the 1d numpy array functionality of mltFromYmdhms().')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)
        
        year   = np.array([x.year for x in dtime])
        month  = np.array([x.month for x in dtime])
        day    = np.array([x.day for x in dtime])
        hour   = np.array([x.hour for x in dtime])
        minute = np.array([x.minute for x in dtime])
        second = np.array([x.second for x in dtime])
        mlon   = np.array(mlon)
        height = np.array(height)

        mlt_test = aacgm.mltFromYmdhms(year,month,day,hour,minute,second,mlon,height=height)

        for mlt_test_0, mlt_0, in zip(mlt_test,mlt):
            self.assertAlmostEqual(mlt_test_0,mlt_0,self.accuracy)

    def test_mltFromYmdhms_scalar_date_height(self):
        print('Testing mltFromYmdhms() when in_lat and in_lon are lists, but date, height, and flg are scalars.')

        glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = self.test_data[0]

        mlon = [mlon] * 10

        mlt_test = aacgm.mltFromYmdhms(dtime.year,dtime.month,dtime.day,dtime.hour,dtime.minute,dtime.second,mlon,height=height)

        for mlt_test_0 in mlt_test:
            self.assertAlmostEqual(mlt_test_0,mlt,self.accuracy)

unittest.main()
