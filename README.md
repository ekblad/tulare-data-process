# tulare-data-process
This repository converts data derived from California Pesticide Use Reports into time series data and plots top crops for each irrigation district.

## raw data inputs
This repository builds off of a data repository created by Natalie Mall - @nataliemall - all required data is included in this repository, but it can also be accessed/created here:
(https://github.com/nataliemall/crop_acreages_CA_DPR_reports)

## Step 1: run -
```
raw_data_processing.py
```

## Step 2: run -
```
time_series_plots.py
```

## Output Data Products

This should create the following directories, in order by process:
```
Irrigation District Data
Irrigation District Summary Data
Irrigation District Time Series
Irrigation District Data - Final
Time Series Data Plots
```

### Irrigation District Data:
Compiles data from all locations within an irrigation district into one CSV, for each irrigation district, for each year.

### Irrigation District Summary Data:
Sums data across all locations in a given irrigation district to get the year's distribution of reported crop acreage.

### Irrigation District Time Series:
Constructs time series data within an irrigation district across all years.  Two CSVs per irrigation district because of the change in crop code ID that occurred between 1989 and 1990, which will be fixed in the next step.

### Irrigation District Data - Final:
Connects time series data across 1989-1990 by creating a code equivalency, the output being continuous yearly time-step data sets of crop acreage for all crops (by current crop ID format) for each irrigation district.

### Time Series Data Plots:
A repository with stacked area plots of top crops as their contribution to the total, over the historical period from 1974-2016, for each irrigation district.
