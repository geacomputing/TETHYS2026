# TETHYS 2026 — Hands-on Training

Hands-on course for **TETHYS 2026**, held at the **University of Cyprus (UCY)**.

The training uses Python and [xarray](https://xarray.dev/) to explore climate and ocean data: opening datasets, inspecting metadata, selecting data in space and time, aggregating and resampling, plotting results, and retrieving Copernicus data programmatically.

## Repository structure

```text
.
├── code/
│   ├── py/                         # Runnable Python scripts
│   └── ipynb/                      # Equivalent Jupyter notebooks
├── Create_Account_Copernicus/      # Copernicus account and credential starter kit
│   ├── cds/                        # Climate Data Store (CDS) setup
│   └── copernicusmarine/           # Copernicus Marine setup
└── test-Scripts/                   # dev checks - untracked
```

- `code/` contains the course exercises and examples. Wherever possible, each lesson is provided in matching `.py` and `.ipynb` forms. Use the scripts locally or run the notebooks in Jupyter/Google Colab.
- `Create_Account_Copernicus/` is the starter kit for creating and safely configuring the credentials needed during the course. It covers both the Copernicus Climate Data Store (CDS) API and Copernicus Marine Toolbox, including on-the-fly access to Zarr/ARCO data.
- `test-Scripts/` contains lightweight scripts for checking credentials and experimentation; these are not the main teaching materials.

All course code is Python unless a file explicitly says otherwise.

## Learning topics

- Core xarray data structures: `Dataset` and `DataArray`
- NetCDF loading, metadata inspection, and coordinate-aware indexing
- Spatial and temporal subsetting
- Reductions, area-weighted averages, resampling, and grouped climatologies
- Visualising gridded and time-series data with Matplotlib and optional Cartopy maps
- Retrieving and opening Copernicus climate and marine data with APIs, including on-the-fly Zarr access

## Getting started

Clone or download this repository, then create and activate a Python environment:

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install xarray netCDF4 pooch numpy matplotlib jupyter
```

For optional map projections and coastlines, also install Cartopy:

```bash
python -m pip install cartopy
```

Run the introductory script:

```bash
python code/py/Intro_xarray.py
```

Or open the equivalent notebook:

```bash
jupyter notebook code/ipynb/Intro_xarray.ipynb
```

The notebook can also be uploaded to and run from Google Colab. Install any missing dependencies in a first Colab cell as needed.

## Copernicus access

Complete the relevant account setup before the data-retrieval exercises:

- [CDS credentials and ECMWF Data Stores client](Create_Account_Copernicus/cds/cds_create_credentials.md)
- [Copernicus Marine credentials and Toolbox](Create_Account_Copernicus/copernicusmarine/marine_create_credentials.md)

CDS and Copernicus Marine are separate services: they require different credentials and client libraries. Keep all keys, tokens, passwords, and generated configuration files private; never commit them to Git or include them in screenshots.

## Requirements

The introductory xarray material requires Python 3 and the packages listed in the setup section. Copernicus exercises additionally require the appropriate client:

- CDS: `ecmwf-datastores-client`
- Copernicus Marine: `copernicusmarine`

Follow the credential guides above for installation and authentication details.

## License

See [LICENSE](LICENSE).
