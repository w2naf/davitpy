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

def mltFromYmdhms(year,month,day,hour,minute,second,mlon,height=350.):
    
    year_arr    = np.array(year)
    month_arr   = np.array(month)
    day_arr     = np.array(day)
    hour_arr    = np.array(hour)
    minute_arr  = np.array(minute)
    second_arr  = np.array(second)

    sizes = np.array([year_arr.size,month_arr.size,day_arr.size,hour_arr.size,minute_arr.size, second_arr.size])

    if np.unique(sizes).size != 1:
        print('All date/time elements must be the same length.')
        return None

    if year_arr.shape   == (): year_arr.shape   = (1,)
    if month_arr.shape  == (): month_arr.shape  = (1,)
    if day_arr.shape    == (): day_arr.shape    = (1,)
    if hour_arr.shape   == (): hour_arr.shape   = (1,)
    if minute_arr.shape == (): minute_arr.shape = (1,)
    if second_arr.shape == (): second_arr.shape = (1,)

    dt_tups = zip(year_arr,month_arr,day_arr,hour_arr,minute_arr,second_arr)
    dtimes = [datetime.datetime(*x) for x in dt_tups]

    return aacgm2_convert_mlt(mlon, height, dtimes, return_mslong=False)
    
def mltFromEpoch(unix_epoch,mlon,height=350.):
    epoch_arr = np.array(unix_epoch)
    if epoch_arr.shape == (): epoch_arr.shape = (1,)

    dtimes = [datetime.datetime.utcfromtimestamp(x) for x in epoch_arr]
    return aacgm2_convert_mlt(mlon, height, dtimes, return_mslong=False)

def mltFromYrsec(year,year_sec,mlon,height=350.):
    year_arr     = np.array(year)
    year_sec_arr = np.array(year_sec)

    sizes = np.array([year_arr.size,year_sec_arr.size])

    if np.unique(sizes).size != 1:
        print('All date/time elements must be the same length.')
        return None

    if year_arr.shape     == (): year_arr.shape       = (1,)
    if year_sec_arr.shape == (): year_sec_arr.shape   = (1,)

    dt_tups = zip(year_arr, year_sec_arr)
    dtimes = [datetime.datetime(x[0],1,1)+datetime.timedelta(seconds=x[1]) for x in dt_tups]
    return aacgm2_convert_mlt(mlon, height, dtimes, return_mslong=False)
