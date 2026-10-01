"""
===============================================================================
TETHYS 2026 | Hands-on Training
By GEA Computing Ltd
===============================================================================

Compare geo-chunked and time-chunked ERA5 ARCO access.

Both archives are tested using the same variable and timestamp.
Times depend on network speed, server load and caching.

Install:
    pip install xarray zarr fsspec aiohttp dask ecmwf-datastores-client
===============================================================================
"""

from time import perf_counter

import xarray as xr
from ecmwf.datastores.config import get_config


# 1. READ THE STORED API KEY
api_key = get_config("key")

if not api_key:
    raise RuntimeError(
        "No CDS API key was found. Follow the CDS credential guide, then run "
        "this script again."
    )

storage_options = {
    "headers": {"Authorization": f"Bearer {api_key}"}
}


# 2. DEFINE THE ARCHIVES
archives = {
    "Time-chunked": (
        "https://arco.datastores.ecmwf.int/"
        "cadl-arco-time-002/arco/"
        "reanalysis_era5_single_levels/sfc/timeChunked.zarr"
    ),
    "Geo-chunked": (
        "https://arco.datastores.ecmwf.int/"
        "cadl-arco-geo-002/arco/"
        "reanalysis_era5_single_levels/sfc/geoChunked.zarr"
    ),
}

# A fixed historical timestamp ensures both tests request identical data.
variable = "d2m"
timestamp = "2024-01-01T00:00:00"

results = []


# 3. TEST BOTH ARCHIVES
for name, url in archives.items():
    print(f"\nTesting {name}...", flush=True)

    # Opening reads metadata and coordinate information.
    start = perf_counter()
    ds = xr.open_zarr(
        url,
        consolidated=True,
        storage_options=storage_options,
    )
    open_seconds = perf_counter() - start

    try:
        # Selection is lazy: it describes the map we want.
        temperature = ds[variable].sel(time=timestamp)

        # load() actually fetches and decodes the required data chunks.
        start = perf_counter()
        temperature.load()
        load_seconds = perf_counter() - start

        results.append((name, open_seconds, load_seconds))

        print(f"Open archive: {open_seconds:.2f} seconds")
        print(f"Load map:     {load_seconds:.2f} seconds")
        print(f"Map shape:    {temperature.shape}")

    finally:
        ds.close()


# 4. COMPARE THE RESULTS
print("\nRESULTS: ONE GLOBAL TEMPERATURE MAP")
print(f"{'Archive':<16} {'Open (s)':>10} {'Load (s)':>10} {'Total (s)':>11}")

for name, open_seconds, load_seconds in results:
    print(
        f"{name:<16} {open_seconds:>10.2f} "
        f"{load_seconds:>10.2f} {open_seconds + load_seconds:>11.2f}"
    )

fastest = min(results, key=lambda result: result[2])
print(f"\nFastest map loading in this run: {fastest[0]}")
