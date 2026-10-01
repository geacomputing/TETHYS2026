"""
TETHYS 2026 | Hands-on Training
By GEA Computing Ltd

Xarray basics: load NetCDF, inspect metadata, subset, aggregate,
resample, group and plot.

Install:
    pip install xarray netCDF4 pooch numpy matplotlib

Optional map support:
    pip install cartopy
"""

from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


# Map options:
#   cartopy = False                  -> regular longitude/latitude plot
#   cartopy = True, "planar"         -> flat map with coastlines
#   cartopy = True, "orthographic"   -> globe view
cartopy = True
map_projection = "orthographic"  # "planar" or "orthographic"


# 1. LOAD A NETCDF FILE
# Download Xarray's example dataset once and save it locally.
filename = Path("air_temperature.nc")

if not filename.exists():
    xr.tutorial.load_dataset("air_temperature").to_netcdf(filename)

ds = xr.open_dataset(filename)


# 2. INSPECT DATA AND METADATA
print("\nDATASET")
print(ds)

print("\nGLOBAL METADATA")
for name, value in ds.attrs.items():
    print(f"{name}: {value}")

print("\nAIR VARIABLE METADATA")
for name, value in ds["air"].attrs.items():
    print(f"{name}: {value}")

print("\nSMALL DATA SAMPLE")
print(ds["air"].isel(time=0, lat=slice(0, 3), lon=slice(0, 3)))

# Convert from Kelvin to Celsius.
temperature = ds["air"] - 273.15
temperature.attrs = {"long_name": "Air temperature", "units": "°C"}


# 3. SLICE AND SUBSET
first_map = temperature.isel(time=0)


january = temperature.sel(
    time=slice("2013-01-01", "2013-01-31")
)

# Latitude is ordered north-to-south in this dataset.
# Longitudes 230–250° correspond to 130–110°W.
region = temperature.sel(
    lat=slice(50, 30),
    lon=slice(230, 250),
)


# Select the nearest grid point (eg to 40°N, 120°W).
myLon, myLat = 240, 40
point = temperature.sel(lat=myLat, lon=myLon, method="nearest")

print("\nSUBSET SIZES")
print("First map:", dict(first_map.sizes))
print("January:", dict(january.sizes))
print("Region:", dict(region.sizes))
print("Point:", dict(point.sizes))


# 4. AGGREGATE
# Average across time to create a map.
mean_map = temperature.mean(dim="time", keep_attrs=True)

# Average across the region, weighting by latitude to account for
# the different areas represented by grid cells.
weights = np.cos(np.deg2rad(region.lat))
regional_mean = region.weighted(weights).mean(
    dim=("lat", "lon"),
    keep_attrs=True,
)

print(f"\nPoint minimum: {point.min().item():.1f} °C")
print(f"Point maximum: {point.max().item():.1f} °C")
print(f"Point mean:    {point.mean().item():.1f} °C")


# 5. RESAMPLE
# Calculate daily and monthly averages at the selected point.
daily = point.resample(time="1D").mean(keep_attrs=True)
monthly = point.resample(time="MS").mean(keep_attrs=True)

print("\nFIRST SIX MONTHLY AVERAGES")
print(monthly.isel(time=slice(0, 6)).to_pandas())


# 6. GROUP
# Average all Januaries together, all Februaries together, and so on.
monthly_cycle = point.groupby("time.month").mean(
    dim="time",
    keep_attrs=True,
)

print("\nMEAN ANNUAL CYCLE")
print(monthly_cycle.to_pandas())


# 7. PLOT
fig = plt.figure(figsize=(13, 9))

if cartopy:
    # Import Cartopy only when requested, so it is not required otherwise.
    import cartopy.crs as ccrs

    data_crs = ccrs.PlateCarree()

    if map_projection == "planar":
        projection = ccrs.PlateCarree(central_longitude=-110)
        map_title = f"Mean temperature: planar map \nfor time: {first_map.time.values} UTC"
    elif map_projection == "orthographic":
        projection = ccrs.Orthographic(
            central_longitude=-110,
            central_latitude=40,
        )
        map_title = f"Mean temperature: globe \nfor time: {first_map.time.values} UTC"
    else:
        raise ValueError(
            "map_projection must be 'planar' or 'orthographic'."
        )

    ax1 = fig.add_subplot(2, 2, 1, projection=projection)
    map_options = {"transform": data_crs}
else:
    ax1 = fig.add_subplot(2, 2, 1)
    map_options = {}
    map_title = f"Mean temperature: longitude-latitude plot\nfor time: {first_map.time.values} UTC"

# Xarray uses the same plotting method with or without Cartopy.
mean_map.plot(
    ax=ax1,
    cmap="seismic",
    cbar_kwargs={
        "label": "Air temperature (°C)",
        "shrink": 0.75,
    },
    **map_options,
)

if cartopy:
    ax1.coastlines(resolution="50m", linewidth=0.7)

    if map_projection == "orthographic":
        ax1.set_global()
        ax1.gridlines(
            linewidth=0.5,
            linestyle="--",
            color="gray",
            alpha=0.6,
        )
    else:
        ax1.set_extent([-160, -30, 15, 75], crs=data_crs)
        grid = ax1.gridlines(
            draw_labels=True,
            linewidth=0.5,
            linestyle="--",
            alpha=0.6,
        )
        grid.top_labels = False
        grid.right_labels = False
else:
    ax1.grid(linestyle="--", alpha=0.5)


point_options = {"transform": data_crs} if cartopy else {}

ax1.scatter(
    myLon,
    myLat,
    color="black",
    marker="o",
    s=60,
    edgecolor="white",
    linewidth=1,
    zorder=10,
    **point_options,
)


ax1.set_title(map_title)

# Daily and monthly averages at the selected point.
ax2 = fig.add_subplot(2, 2, 2)
daily.plot(ax=ax2, label="Daily", alpha=0.5)
monthly.plot(ax=ax2, label="Monthly", linewidth=2)
ax2.set_title("Point temperature: nearest to 40°N, 120°W")
ax2.legend()
ax2.grid(alpha=0.3)

# Mean annual cycle at the selected point.
ax3 = fig.add_subplot(2, 2, 3)
monthly_cycle.plot(ax=ax3, marker="o")
ax3.set_title("Mean annual cycle at the point")
ax3.set_xticks(range(1, 13))
ax3.grid(alpha=0.3)

# Area-weighted regional average through time.
ax4 = fig.add_subplot(2, 2, 4)
regional_mean.plot(ax=ax4)
ax4.set_title("Area-weighted regional temperature")
ax4.grid(alpha=0.3)

plt.tight_layout()
plt.show()

ds.close()