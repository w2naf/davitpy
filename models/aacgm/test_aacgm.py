import unittest
import aacgm2

accuracy = 6
class AacgmTest(unittest.TestCase):
    def test_aacgm_convert(self):
        #This test mirrors the C language test provided by Simon Shepherd.
        # /* compute AACGM lat/lon with no time specified */
        lat =   45.5
        lon =  -23.5
        hgt = 1135.
        geo =    0

        mlat, mlon, r  = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}\n".format(mlat,mlon,r))
        self.assertAlmostEqual(mlat,0.,accuracy)
        self.assertAlmostEqual(mlon,0.,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        
        year   = 2014
        month  = 3
        day    = 22
        hour   = 3
        minute = 11
        second = 0
        print("Setting time to : {0:04d}{1:02d}{2:02d} {3:02d}{4:02d}{5:02d}\n".format(year, month, day, hour, minute, second))

        # /* set date and time */
        aacgm2.AACGM_v2_SetDateTime(year, month, day, hour, minute, second)

        # /* compute AACGM lat/lon */
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,48.377539,accuracy)
        self.assertAlmostEqual(mlon,57.822458,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,2.092153,accuracy)
        self.assertAlmostEqual(mslong,-153.559832,accuracy)

        # /* pick a different year */
        year   = 1997;
        print("Setting time to : {0:04d}{1:02d}{2:02d} {3:02d}{4:02d}{5:02d}\n".format(year, month, day, hour, minute, second))
        aacgm2.AACGM_v2_SetDateTime(year, month, day, hour, minute, second)
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,49.425800,accuracy)
        self.assertAlmostEqual(mlon,58.259686,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,2.121862,accuracy)
        self.assertAlmostEqual(mslong,-153.568237,accuracy)

        # /* pick a different lat/lon; should not need to do any interpolations */
        lat = 65.5
        lon = 93.5
        aacgm2.AACGM_v2_SetDateTime(year, month, day, hour, minute, second)
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,62.251076,accuracy)
        self.assertAlmostEqual(mlon,166.990581,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,9.370588,accuracy)
        self.assertAlmostEqual(mslong,-153.568237,accuracy)

        # /* pick a different height; should only need to do height interpolation */
        hgt = 0.
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,60.799240,accuracy)
        self.assertAlmostEqual(mlon,166.518084,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,9.339088,accuracy)
        self.assertAlmostEqual(mslong,-153.568237,accuracy)

        # /* do another lat/lon; no interpolations */
        lat = 75.5
        lon = 73.5
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,70.420669,accuracy)
        self.assertAlmostEqual(mlon,150.743259,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,8.287433,accuracy)
        self.assertAlmostEqual(mslong,-153.568237,accuracy)

        # /* pick another year; should require loading new coeffs and both interps */
        year   = 2004
        month  = 3
        day    = 22
        hour   = 3
        minute = 11
        second = 0

        print("Setting time to : {0:04d}{1:02d}{2:02d} {3:02d}{4:02d}{5:02d}\n".format(year, month, day, hour, minute, second))
        aacgm2.AACGM_v2_SetDateTime(year, month, day, hour, minute, second)
        mlat, mlon, r   = aacgm2.AACGM_v2_Convert(lat, lon, hgt, geo)
        mlt, mslong     = aacgm2.AACGM_v2_ConvertMLT(mlon,hgt)
        print("lat = {0:f}, lon = {1:f}, height = {2:f}".format(lat,lon,hgt))
        print("mlat = {0:f}, mlon = {1:f}, r = {2:f}".format(mlat,mlon,r))
        print("mlt = {0:f}, mslong = {1:f}\n".format(mlt,mslong))
        self.assertAlmostEqual(mlat,70.726381,accuracy)
        self.assertAlmostEqual(mlon,150.672892,accuracy)
        self.assertAlmostEqual(r,1.0,accuracy)
        self.assertAlmostEqual(mlt,8.338513,accuracy)
        self.assertAlmostEqual(mslong,-154.404804,accuracy)

if __name__ == '__main__':
    unittest.main()
