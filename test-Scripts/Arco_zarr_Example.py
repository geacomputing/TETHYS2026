"""
===============================================================================
TETHYS 2026 | Hands-on Training
By GEA Computing Ltd
===============================================================================

Example: Access ECMWF ERA5 ARCO data using Xarray and Zarr.

This script:
    1. Reads the CDS API key using the existing cdsapi configuration.
    2. Defines two remote Zarr archives with different chunking strategies.
    3. Opens the time-chunked archive as an Xarray Dataset.
    4. Displays the dataset structure without loading all data into memory.

Prerequisites:
    - A configured CDS account and API key, normally in ~/.cdsapirc.
    - Acceptance of the relevant dataset licence on the CDS website.
    - Python packages: xarray, zarr, fsspec, aiohttp, dask and cdsapi.

Documentation:
    https://confluence.ecmwf.int/pages/viewpage.action?pageId=639215345
===============================================================================
"""

# Xarray provides labelled multidimensional arrays and datasets.
# It lets us select and analyse data using named dimensions and coordinates,
# such as time, latitude and longitude.
import xarray as xr

# Import the configuration reader used internally by cdsapi.
# This is an internal helper rather than a guaranteed stable public API.
from cdsapi.api import get_url_key_verify


# ---------------------------------------------------------------------------
# 1. Read the CDS authentication key
# ---------------------------------------------------------------------------

# Passing None asks cdsapi to resolve these settings from its configuration:
#     - CDSAPI_URL and CDSAPI_KEY environment variables, when defined.
#     - Otherwise, the configuration file, normally ~/.cdsapirc.
#       CDSAPI_RC can specify a different configuration-file location.
#
# The function returns three values:
#     (CDS API URL, API key, SSL verification setting)
#
# Only the API key is needed here. The underscore indicates that the other
# returned values are intentionally unused.
#
# Keep the key private: do not print it or put it directly into this script.
_, cdsapi_key, _ = get_url_key_verify(None, None, None)


# ---------------------------------------------------------------------------
# 2. Define the remote Zarr archives
# ---------------------------------------------------------------------------

# Zarr stores multidimensional arrays in independently accessible chunks.
# Accessing a subset retrieves the chunks containing the requested data,
# so the archive's chunk layout strongly affects download efficiency.

# GEO-CHUNKED:
# Optimised for long time series at a single location or over a small area.
# Example: retrieve several years of air temperature near one station.
geochunked_url = (
    "https://arco.datastores.ecmwf.int/"
    "cadl-arco-geo-002/arco/"
    "reanalysis_era5_single_levels/sfc/geoChunked.zarr"
)

# TIME-CHUNKED:
# Optimised for large spatial regions over short time periods.
# Example: retrieve a global temperature map for one hour.
timechunked_url = (
    "https://arco.datastores.ecmwf.int/"
    "cadl-arco-time-002/arco/"
    "reanalysis_era5_single_levels/sfc/timeChunked.zarr"
)


# ---------------------------------------------------------------------------
# 3. Open the time-chunked archive
# ---------------------------------------------------------------------------

# This example selects the archive suited to maps and spatial analysis.
# For long time series at a point, change this to geochunked_url.
selected_url = timechunked_url

# Open the remote archive as an Xarray Dataset.
#
# consolidated=True:
#     Read consolidated metadata, reducing the number of requests needed
#     to discover the archive's variables, dimensions and attributes.
#
# storage_options:
#     Pass connection settings to the underlying storage implementation.
#     The Authorization header authenticates requests using the CDS key.
#
# With the default Dask-backed opening, data variables remain lazy:
# opening the dataset reads metadata and may read coordinate arrays, but
# does not download the entire ERA5 archive.
#
# Later operations such as .compute(), .load() or exporting data trigger
# retrieval of the required chunks. Select your variables, time period
# and geographical subset before triggering these operations.
ds = xr.open_zarr(
    selected_url,
    consolidated=True,
    storage_options={
        "headers": {
            "Authorization": f"Bearer {cdsapi_key}"
        }
    },
)


# ---------------------------------------------------------------------------
# 4. Inspect the dataset
# ---------------------------------------------------------------------------

# Display dimensions, coordinates, available variables and attributes.
# Printing the dataset does not load all of its data variables into memory.
print(ds)