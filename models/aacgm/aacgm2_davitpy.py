import aacgm2
import datetime
import numpy as np

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

def aacgm2_convert_mlt(in_lon, height, dtime, return_mslong=False):
    # Convert to numpy arrays to make it easy to handle both
    # scalars and lists.
    in_lons = np.array(in_lon)
    heights = np.array(height)
    dtimes  = np.array(dtime)

    # Check height, year, and flg to make sure they are the correct length.
    if (heights.size != in_lons.size) and (heights.size == 1):
        heights = heights.repeat(in_lons.size)

    if (dtimes.size != in_lons.size) and (dtimes.size == 1):
        dtimes = dtimes.repeat(in_lons.size)

    #Make sure things actually come out as lists.
    if in_lons.shape == (): in_lons.shape = (1,)
    if heights.shape == (): heights.shape = (1,)
    if dtimes.shape  == (): dtimes.shape  = (1,)

    # Initialize lists for final answers and call AACGM function.
    mlts, mslongs = [], []
    current_datetime = None

    for lon_0, height_0, dt_0 in zip(in_lons,heights,dtimes):
        if dt_0 != current_datetime:
            aacgm2.AACGM_v2_SetDateTime(dt_0.year,dt_0.month,dt_0.day,dt_0.hour,dt_0.minute,dt_0.second)
            current_datetime = dt_0

        mlt_0, mslong_0 = aacgm2.AACGM_v2_ConvertMLT(lon_0,height_0)

        mlts.append(mlt_0)
        mslongs.append(mslong_0)

    # Return a scalar if only one value
    # Return a numpy array if a numpy array was given.
    if in_lons.size == 1:
        ret_mlts    = mlts[0]
        ret_mslongs = mslongs[0]
    else:
        ret_mlts    = np.array(mlts)
        ret_mslongs = np.array(mslongs)

    if return_mslong:
        return ret_mlts, ret_mslongs
    else:
        return ret_mlts

def aacgmConv(inLat, inLon, height, year, flg=0):
    years   = np.array(year)
    if years.shape == (): years.shape = (1,)
    dtimes  = [datetime.datetime(yr,1,1) for yr in years]   
    return aacgm2_convert(inLat, inLon, height, dtimes, flg)

# Define aacgmConvArr for legacy compatibility.
# aacgmConv now can handle everything aacgmConvArr could, so just
# set them equal.
aacgmConvArr = aacgmConv
