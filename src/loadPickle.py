#loadPickle.py
import pandas as pd
import xarray as xr
import numpy as np


## This function is called everywhere the pickle is loaded.
## It both loads the pickle and converts to xarray,
## AND FILTERS DATA that is not included in analysis
## It takes as input the path to the pickle, and culat (the southern most latitude to include)
def loadPickle(path, cutlat=-50):
    # load dataframe
    cruises_df = pd.read_pickle(path)
    # Filter dataframe for the geographic region we want
    cruise_dfilt = cruises_df[cruises_df.lat<30] # Ignore spurious N Atlantic data point
    cruise_dfilt = cruise_dfilt[cruise_dfilt.lon>20] # Cut off Agulhas region
    cruise_dfilt = cruise_dfilt[cruise_dfilt.lat>cutlat] # Cut off SO
    cruises_dset = cruise_dfilt.to_xarray()


    # Other data points/stations are removed as described in DataQualityCheck.ipynb
    # The list below uses tuples that are passed to filterStation below.
    # A tuple like ['45', None] removes the entire station 45
    # A tuple like ['71', 2195] removes the obs at depth 2195 m from station 71
    GazelleStations = [
                        # Stations removed due to WOA inversions
                        ['45', None],
                        ['55', None],
                        ['56', None],
                        # Stations removed due to Gazelle inversions
                        ['43', 366],
                        ['43', 914],
                        ['48', 183],
                        #['55', 640], #already dropped (above)
                        ['71', 2195],
                        ['73', 1646],
                        ['74', 2195],
                        ['76', 1646],
                        ['79', 1646],
                        ['80', 1646],
                        ['81', 1646],
                        ['83', 1646],
                        ['84', 1280]]

    # Remove all suspect Valdivia stations
    ValdiviaStations = [
                        # Station 102 was in the Agulhas, and they note very large (30°)
                        # wire deflections. This value also ends up indicating anomalous
                        # strong cooling, consistent with deflection errors.
                        ['102', None],

                        # Some of the station 168 values have this note:
                        # 'The numbers marked with * are obtained from Lotangen,
                        #  mostly near St. Paul and New Amsterdam, and are
                        #  therefore ground temperatures'
                        ['168', 158], ['168', 496], ['168', 672], ['168', 1463], ['168', 2412],

                        # There are some duplicate station values in the Valdivia profiles
                        ['190', 903], ['190', 1671],

                        # Some of the Valdivia data is reported as combined stations, we remove these:
                        ['200-206', None],

                        # Profile 221 duplicates some of station 218 (which is already included)
                        ['221', 500], ['221', 1000], ['221', 2000],

                        # This one appears to be interpolated from another station
                        ['236', 1000],

                        # Station 261 is messy, with everything below 628 m reported
                        # as a bottom temperature. Not clear what is meant, so we drop them.
                        ['261', 628], ['261', 638], ['261', 693], ['261', 741],
                        ['261', 977], ['261', 1079], ['261', 1134], ['261', 1213],
                        ['261', 1242], ['261', 1289], ['261', 1362], ['261', 1644],
                        ['261', 1668]]

    # Remove suspect Planet Obs:
    PlanetStations = [
                        # 'Several values are estimated due to limit of thermometer scale'
                        ['144', 50], ['144', 80], ['158', 100]]

    for s, d in GazelleStations:
        cruises_dset = filterStation('Gazelle',s, cruises_dset, depth=d )

    for s, d in ValdiviaStations:
        cruises_dset = filterStation('Valdivia',s, cruises_dset, depth=d )

    for s, d in PlanetStations:
        cruises_dset = filterStation('Planet',s, cruises_dset, depth=d )


    ##### Patch together seasonal and monthly WOA18 data
    # Monthly values are best (removes seasonal cycle), but they don't extend deeper
    # than 1500 m. Here we fill in below this with seasonal data.
    #
    # Use the seasonal values in place of monthly values as necessary.
    # Make new 'merged' variables
    temp_dset = cruises_dset.copy()
    mask = np.logical_or(np.isfinite(temp_dset['delta_T_monthly_rgrd']), temp_dset.Depth<1500)
    temp_dset['delta_T_merged'] = xr.where(mask, temp_dset['delta_T_monthly_rgrd'], temp_dset['delta_T_seasonal_rgrd'])
    temp_dset['WOA_temp'] = temp_dset.WOA_temp_monthly_rgrd
    temp_dset['WOA_temp'] = xr.where(mask, temp_dset['WOA_temp'], temp_dset['WOA_temp_seasonal_rgrd'] )

    mask = np.logical_or(np.isfinite(temp_dset['delta_T_monthly_5564']), temp_dset.Depth<1500)
    temp_dset['delta_T_merged_5564'] = xr.where(mask, temp_dset['delta_T_monthly_5564'], temp_dset['delta_T_seasonal_5564'])
    temp_dset['WOA_temp_5564'] = temp_dset.WOA_temp_monthly_5564
    temp_dset['WOA_temp_5564'] = xr.where(mask, temp_dset['WOA_temp_5564'], temp_dset['WOA_temp_seasonal_5564'] )
    
    return temp_dset


# Helper function to filter out stations that have compromised dataframe
# Inputs:
#           cruise     -    name of cruise (str)
#           station    -    station number
#           ds         -    xarray dataset
#           Depth      -    Optional depth to remove, if no depth given, remove entire station

def filterStation(cruise, station, ds, depth=None):
    if depth==None: # Remove entire station
      ds = ds.where(np.logical_or(ds.cruise!=cruise, ds.Station!=station), drop=True)
    else: # Remove a single observation at a particular depth
      ds = ds.where(np.logical_or(ds.cruise!=cruise, np.logical_or(ds.Station!=station, ds.Depth !=depth)), drop=True)
    return ds
