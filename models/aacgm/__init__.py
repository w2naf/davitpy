"""
*********************
**Module**: models.aacgm
*********************
"""
try:
    import aacgm2
except Exception, e:
    print __file__+' -> aacgm: ', e

import datetime
import numpy as np

def aacgmConv(inLat, inLon, height, year, flg):
    years   = np.array(year).tolist()
    dtimes  = [datetime.datetime(yr,1,1) for yr in years]   
    return aacgm2_convert(inLat, inLon, height, year, flg)

def aacgm2_convert(in_lat, in_lon, height, dtime, flg=0):
    # Convert to numpy arrays to make it easy to handle both
    # scalars and lists.
    in_lats = np.array(in_lat)
    in_lons = np.array(in_lon)
    heights = np.array(height)
    dtimes  = np.array(dtime)
    flgs    = np.array(flg)

    # Make sure we have the same number of lats,lons.
    if in_lats.size != in_lons.size:
        print('Please provide the same number of latitudes and longitudes')
        return None

    # Check height, year, and flg to make sure they are the correct length.
    if (heights.size != in_lats.size) and (heights.size == 1):
        heights = heights.repeat(in_lats.size)

    if (dtimes.size != in_lats.size) and (dtimes.size == 1):
        dtimes = dtimes.repeat(in_lats.size)

    if (flgs.size != in_lats.size) and (flgs.size == 1):
        flgs = flgs.repeat(in_lats.size)
    
    #Make sure things actually come out as lists.
    if in_lats.shape == (): in_lats.shape = (1,)
    if in_lons.shape == (): in_lons.shape = (1,)
    if heights.shape == (): heights.shape = (1,)
    if dtimes.shape  == (): dtimes.shape  = (1,)
    if flgs.shape    == (): flgs.shape    = (1,)

    # Initialize lists for final answers and call AACGM function.
    mlats, mlons, rs = [], [], []
    current_datetime = None

    for lat_0, lon_0, height_0, dt_0, flg_0 in zip(in_lats,in_lons,heights,dtimes,flgs):
        if dt_0 != current_datetime:
            aacgm2.AACGM_v2_SetDateTime(dt_0.year,dt_0.month,dt_0.day,dt_0.hour,dt_0.minute,dt_0.second)
            current_datetime = dt_0

        mlat_0, mlon_0, r_0 = aacgm2.AACGM_v2_Convert(lat_0,lon_0,height_0,flg_0)

        mlats.append(mlat_0)
        mlons.append(mlon_0)
        rs.append(r_0)

    # Return a scalar if only one value
    # Return a numpy array if a numpy array was given.
    if in_lats.size == 1:
        ret_mlats   = mlats[0]
        ret_mlon    = mlons[0]
        ret_rs      = rs[0]
    else:
        ret_mlats   = np.array(mlats)
        ret_mlon    = np.array(mlons)
        ret_rs      = np.array(rs)

    return ret_mlats,ret_mlon,ret_rs

if __name__ == '__main__':
    import unittest
    from models import aacgm

    class DavitPyAacgmTest(unittest.TestCase):
        def setUp(self):
            self.accuracy = 6

            dt = datetime.datetime
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

                mlat_test, mlon_test, r_test = aacgm2_convert(glat,glon,height,dtime,flg)
                self.assertAlmostEqual(mlat_test,mlat,self.accuracy)
                self.assertAlmostEqual(mlon_test,mlon,self.accuracy)
                self.assertAlmostEqual(r_test,r,self.accuracy)

        def test_aacgm2_convert_lists(self):
            print('Testing the list functionality of aacgm2_convert.')

            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

            mlat_test, mlon_test, r_test = aacgm2_convert(glat,glon,height,dtime,flg)

            for mlat_test_0,mlon_test_0,r_test_0, mlat_0, mlon_0, r_0 \
                    in zip(mlat_test,mlon_test,r_test,mlat,mlon,r):
                self.assertAlmostEqual(mlat_test_0,mlat_0,self.accuracy)
                self.assertAlmostEqual(mlon_test_0,mlon_0,self.accuracy)
                self.assertAlmostEqual(r_test_0,r_0,self.accuracy)

        def test_aacgm2_convert_numpy(self):
            print('Testing the 1d numpy array functionality of aacgm2_convert.')

            glat,glon,height,dtime,flg,mlat,mlon,r,mlt,mslong = zip(*self.test_data)

            mlat_test, mlon_test, r_test = aacgm2_convert(np.array(glat),np.array(glon),np.array(height),np.array(dtime),np.array(flg))

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

            mlat_test, mlon_test, r_test = aacgm2_convert(glat,glon,height,dtime)

            for mlat_test_0,mlon_test_0,r_test_0 in zip(mlat_test,mlon_test,r_test):
                self.assertAlmostEqual(mlat_test_0,mlat,self.accuracy)
                self.assertAlmostEqual(mlon_test_0,mlon,self.accuracy)
                self.assertAlmostEqual(r_test_0,r,self.accuracy)
           
    unittest.main()
