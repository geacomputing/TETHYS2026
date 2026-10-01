"""
===============================================================================
TETHYS 2026 | Hands-on Training
By GEA Computing Ltd
===============================================================================

Access ECMWF ERA5 ARCO data using Xarray and Zarr.

This example reads the stored API key, opens a remote Zarr archive,
selects its final time step and displays the dataset structure.

Prerequisites:
    - Credentials in ~/.ecmwfdatastoresrc or ECMWF_DATASTORES_KEY.
    - Acceptance of the relevant dataset licence on the CDS website.

Install:
    pip install xarray zarr fsspec aiohttp dask ecmwf-datastores-client

Documentation:
    https://confluence.ecmwf.int/pages/viewpage.action?pageId=639215345
===============================================================================
"""

import xarray as xr
from ecmwf.datastores.config import get_config


# 1. READ THE AUTHENTICATION KEY
# Check ECMWF_DATASTORES_KEY first, then ~/.ecmwfdatastoresrc.
# This reads local configuration without making a network request.
api_key = get_config("key")


# 2. DEFINE THE ZARR ARCHIVES
# Zarr stores arrays in chunks. The chunk layout affects how efficiently
# a particular geographical or temporal subset can be retrieved.

# Geo-chunked: best for long time series at a point or over a small area.
geochunked_url = (
    "https://arco.datastores.ecmwf.int/"
    "cadl-arco-geo-002/arco/"
    "reanalysis_era5_single_levels/sfc/geoChunked.zarr"
)

# Time-chunked: best for maps or large areas over a short time period.
timechunked_url = (
    "https://arco.datastores.ecmwf.int/"
    "cadl-arco-time-002/arco/"
    "reanalysis_era5_single_levels/sfc/timeChunked.zarr"
)

# This example selects one time step, so use the time-chunked archive.
selected_url = timechunked_url


# 3. OPEN THE ARCHIVE
# consolidated=True reduces metadata requests.
# The HTTP header authenticates access using the stored API key.
# Opening the archive does not load all data variables into memory.
ds = xr.open_zarr(
    selected_url,
    consolidated=True,
    storage_options={
        "headers": {"Authorization": f"Bearer {api_key}"}
    },
)

# 4. SELECT THE FINAL TIME STEP
# isel selects by position; -1 means the final entry in the time axis.
# This limits subsequent calculations to one time step.
# Selection remains lazy: values are fetched when needed.
latest = ds.isel(time=-1)

# 5. INSPECT THE SELECTED DATASET
print("\nFINAL TIME COORDINATE")
print(latest["time"].values)

print("\nDATASET STRUCTURE")
print(latest)

# To retrieve actual values, select a variable first, for example:
# temperature = latest["2m_temperature"].load()

# The context manager closes the dataset automatically.


#Check sizes! 
full_size = ds.nbytes
last_size = ds.isel(time=-1).nbytes

print()
print(25*"-")
print()
print(f"(Full dataset:   {full_size / 10**12:.2f} TB)")
print(f"Last time step: {last_size / 10**6:.2f} MB")

print(ds.isel(time=-1).coords)