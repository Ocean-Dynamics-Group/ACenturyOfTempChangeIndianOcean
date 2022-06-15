# ACenturyOfTempChangeIndianOcean

This repository contains analysis code for the manuscript:

> Wenegrat, J.O., E. Bonanno, U. Rack, and G. Gebbie, 2022: A century of observed temperature change in the Indian Ocean. _Geophysical Research Letters_, doi:10.1029/2022GL098217

## DATA
Raw data (as digitized from the historical cruise reports) can be found in [/data/](https://github.com/Ocean-Dynamics-Group/ACenturyOfTempChangeIndianOcean/tree/main/data) in [pickle](https://docs.python.org/3/library/pickle.html#module-pickle) format, along with scripts used in loading and processing the historical and modern datasets. Information on which observations are included in the final analysis can be found in [/src/loadPickle.py](https://github.com/Ocean-Dynamics-Group/ACenturyOfTempChangeIndianOcean/blob/main/src/loadPickle.py).

A [netcdf file](https://github.com/Ocean-Dynamics-Group/ACenturyOfTempChangeIndianOcean/blob/main/data/GazelleValdiviaPlanet_v1p0.nc) containing only the quality controlled historical measurements is also provided in /data/. This is the recommended starting point if you intend to use the historical data in your own separate analysis.

## ANALYSIS
All code necessary for reproducing figures can be found in the iPython notebooks ([/notebooks/](https://github.com/Ocean-Dynamics-Group/ACenturyOfTempChangeIndianOcean/tree/main/notebooks)).

Note that these notebooks are set up as Google Colaboratory notebooks, but can easily be adapted for use in a standard python environment. To use these in Google Colab, first clone the repository to a google drive account, and then open the notebook using Google Colab. The first code cell of each notebook will configure the necessary environment.

Code for the least-squares analysis of modern minus historical temperature changes can be found at: https://github.com/ggebbie/HistoricalIndianOcean.

## CITATION
A permanent citable doi for this code can be found at: 

[![DOI](https://zenodo.org/badge/502983134.svg)](https://zenodo.org/badge/latestdoi/502983134)

A citable repository containing just the data in netcdf form can be found at:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6646659.svg)](https://doi.org/10.5281/zenodo.6646659)





