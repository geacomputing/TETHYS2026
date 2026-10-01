"""
GEA COMPUTING | TETHYS 2026 Hands-on Training Module

Open an authenticated ARCO ERA5 Zarr dataset with xarray.

The example uses the time-chunked store, which is a suitable layout for reading
spatial fields at one or a small number of time steps.
"""

# xarray supplies the ``open_zarr`` reader and represents the remote data as an
# xarray Dataset.  The data remain remote until a variable is explicitly read.
import xarray as xr

# CDS credentials are obtained from the user's configured cdsapi settings (for
# example, ``~/.cdsapirc``).  Do not place an API key directly in this file:
# source-controlled credentials can be exposed accidentally.
from cdsapi.api import get_url_key_verify


# ``get_url_key_verify`` returns the CDS endpoint, API key, and TLS-verification
# setting, in that order.  Only the key is needed here because ARCO expects it
# in an HTTP Bearer authorization header.
_, cdsapi_key, _ = get_url_key_verify(None, None, None)


# %%
# The geo-chunked store is optimized for time series at one or a few locations.
# Keep this URL available if the training exercise later reads point-based data.
geochunked_url = (
    "https://arco.datastores.ecmwf.int/cadl-arco-geo-002/arco/"
    "reanalysis_era5_single_levels/sfc/geoChunked.zarr"
)

# The time-chunked store is optimized for spatial fields such as global maps at
# one time step.  This is the store opened in the example below.
timechunked_url = (
    "https://arco.datastores.ecmwf.int/cadl-arco-time-002/arco/"
    "reanalysis_era5_single_levels/sfc/timeChunked.zarr"
)

# Open only the dataset metadata and Zarr index initially.  ``consolidated``
# tells xarray that the store keeps metadata in its consolidated form, reducing
# remote metadata requests.  Each subsequent array read includes the CDS token
# in its HTTP Authorization header.
ds = xr.open_zarr(
    timechunked_url,
    consolidated=True,
    storage_options={
        "headers": {"Authorization": f"Bearer {cdsapi_key}"},
    },
)

# Display dimensions, coordinates, data variables, and attributes so learners
# can decide which variable and subset to use in the next exercise.
print(ds)
