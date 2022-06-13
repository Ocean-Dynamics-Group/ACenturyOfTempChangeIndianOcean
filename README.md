# ACenturyOfTempChangeIndianOcean

This repository contains analysis code for the manuscript:

> Wenegrat, J.O., E. Bonanno, U. Rack, and G. Gebbie, 2022: A century of observed temperature change in the Indian Ocean. _Geophysical Research Letters_, doi:10.1029/2022GL098217

Code for reproducing figures can be found in /notebooks/. Raw data (as digitized from the historical cruise reports) can be found in /data/ in pickle format, along with scrips used in loading and processing the historical and modern datasets. A reduced netcdf file containing only the quality controlled historical data is also provided. Information on which observations are included in the final analysis can be found in /src/loadPickle.py.

Note that these notebooks are set up as Google Colaboratory notebooks, but can easily be adapted for use in a standard python environment. 

Code for the least-squares analysis of modern minus historical temperature changes can be found at: https://github.com/ggebbie/HistoricalIndianOcean.
