# TETHYS 2026 — hands-on training

Practical materials for exploring climate and ocean data with Python, xarray, Copernicus services, and a browser-based ERA5 map. The course is hosted by the University of Cyprus (UCY) and prepared by GEA Computing Ltd.

## What you will learn

- Work with xarray `Dataset` and `DataArray` objects.
- Open NetCDF and remote Zarr data, inspect metadata, and select data by place and time.
- Calculate spatial and temporal summaries, resample time series, and create climatologies.
- Plot gridded data and time series with Matplotlib; optionally use Cartopy maps.
- Access Copernicus Climate Data Store (CDS) and Copernicus Marine data safely.
- See why a Zarr archive's chunk layout matters for map and time-series workloads.

## Setup and reproducibility

Create the three course environments used for the lessons: `xarray`, `ecmwf-datastores-client`, and `copernicusMarine`. Follow the credential guides before running the CDS or Copernicus Marine lessons.

After creating them, record their installed dependencies with the provided script:

```bash
bash create_envs.sh
```

The script writes a pip requirements file and a Conda YAML export for each environment to [`environments/`](environments/README.md). The YAML files omit machine-specific `prefix` values and can be used to recreate an environment, for example:

```bash
conda env create --file environments/yml_xarray.yml
```

Run the introductory lesson:

```bash
python code/py/Intro_xarray.py
```

Or open any matching notebook:

```bash
jupyter lab code/ipynb/Intro_xarray.ipynb
```

## Course materials

| Material | What it does | Why it matters |
| --- | --- | --- |
| `code/py/Intro_xarray.py` | Loads tutorial NetCDF data, subsets it, calculates statistics, resamples it, and plots results. | Builds the xarray workflow used in later exercises. |
| `code/py/Intro_CDS_Client.py` | Authenticates to CDS, explores the catalogue, and optionally retrieves a small ERA5 sample. | Introduces reproducible, programmatic access to climate data. |
| `code/py/Intro_Zarr.py` | Opens an authenticated ERA5 ARCO Zarr archive and inspects one time step. | Shows lazy remote access without downloading a whole archive. |
| `code/py/Time_Zarr.py` | Compares the time- and geo-chunked ERA5 archives for one global map. | Demonstrates that choosing chunks to match the task improves performance. |
| `code/ipynb/*.ipynb` | Notebook versions of every Python lesson, with matching filenames. | Supports an interactive Jupyter workflow; cells contain no credentials. |
| `simple_web_page_zarr/TETHYS_ERA5_Map.html` | Interactive, browser-only map of ERA5 2 m air temperature. | Makes remote Zarr access and hourly data exploration visible without writing Python. |

## Browser-based ERA5 map

The standalone [ERA5 map](simple_web_page_zarr/TETHYS_ERA5_Map.html) loads a seven-day, hourly window of global 2 m air temperature. It uses ECMWF's **time-chunked** ERA5 ARCO Zarr archive, which is suited to maps covering large areas over a short time period.

Serve the page locally, then open the displayed address in a current browser:

```bash
python -m http.server 8000 --directory simple_web_page_zarr
```

Open <http://localhost:8000/TETHYS_ERA5_Map.html>, enter a CDS API key, choose a UTC start date, and select **Load map**. Drag to pan, use the mouse wheel to zoom, and move the slider through the hourly maps.

### How it works

1. The page requests Zarr metadata and only the chunks needed for the chosen temperature map from ECMWF.
2. It converts temperatures from Kelvin to °C, colours the grid, and draws it with bundled coastline geometry.
3. Moving the slider requests another hourly slice; it does not download the complete ERA5 archive.

This design exists to make the relationship between a data request and remote chunked storage tangible. It is a teaching demonstrator, not a general-purpose map service: network speed, ECMWF service load, browser support, and CDS permissions affect performance.

### API-key safety

The map sends the key directly to ECMWF as an authorization header and does not intentionally store it. Still, treat it as a password: use the page only from a trusted local copy, do not publish a page with a key prefilled, and never commit credentials, tokens, screenshots, or generated configuration files.

## Copernicus access

Complete the applicable account setup before the retrieval exercises:

- [CDS credentials and ECMWF Data Stores client](Create_Account_Copernicus/cds/cds_create_credentials.md)
- [Copernicus Marine credentials and Toolbox](Create_Account_Copernicus/copernicusmarine/marine_create_credentials.md)

CDS and Copernicus Marine are separate services, with separate accounts, credentials, and course environments. Configure them locally using the guides above before running their lessons.

## Repository layout

```text
.
├── code/
│   ├── py/                              # Runnable Python lessons
│   └── ipynb/                           # Equivalent Jupyter notebooks
├── environments/                        # Exports generated by create_envs.sh
│   ├── requirements_<environment>.txt   # pip package snapshots
│   └── yml_<environment>.yml            # Conda environment snapshots
├── Create_Account_Copernicus/           # CDS and Marine authentication guides
└── simple_web_page_zarr/
    └── TETHYS_ERA5_Map.html             # Standalone browser demonstrator
```

## License

See [LICENSE](LICENSE).
