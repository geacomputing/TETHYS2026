# Copernicus Marine credentials and Toolbox

## What is Copernicus Marine?

Copernicus Marine provides ocean and sea data, including satellite observations, in-situ measurements, and numerical-model products. It complements CDS, which is primarily used for climate and atmospheric data. A free Marine account is required for authenticated data access.

> **Separate service:** Copernicus Marine uses a different client and different username/password credentials from CDS. Do not use a CDS API key here.

## 1. Create or use a Copernicus Marine account

1. Open [Copernicus Marine](https://marine.copernicus.eu/) and select **LOGIN OR REGISTER** in the header.
2. If you have an account, select **Log in** and enter your username (or account email) and password. Otherwise, select **Register**, complete the form, confirm the verification email, and set a password.

## 2. Install the Copernicus Marine Toolbox

The Toolbox is a different API client from the CDS client. Use a separate environment to avoid dependency conflicts; do not mix `pip` and conda in the same environment.

### Conda

```bash
conda create --name copernicusmarine -c conda-forge copernicusmarine
conda activate copernicusmarine
copernicusmarine --version
```

### Pip

```bash
python -m venv .venv-copernicusmarine
source .venv-copernicusmarine/bin/activate  # Windows: .venv-copernicusmarine\Scripts\activate
python -m pip install --upgrade pip
python -m pip install copernicusmarine
copernicusmarine --version
```

## 3. Sign in from the Toolbox

Do **not** create a credential file by hand. In the Marine environment, run:

```bash
copernicusmarine login
```

Enter your Copernicus Marine username (or email) and password when prompted. The password is not displayed while you type. The Toolbox validates the credentials and creates its own configuration file in `~/.copernicusmarine/`, so future commands can use it automatically.

The generated file is Base64-encoded, not cryptographically encrypted; keep your computer account protected and never commit this file to Git.

To confirm access later:

```bash
copernicusmarine login --check-credentials-valid
```

## References

- [Installation instructions (pip and conda)](https://help.marine.copernicus.eu/en/articles/7970514-copernicus-marine-toolbox-installation)
- [Installation video](https://vimeo.com/1004524687?fl=pl&fe=sh)
- [Credentials configuration](https://help.marine.copernicus.eu/en/articles/8185007-copernicus-marine-toolbox-credentials-configuration)
- [Toolbox login reference](https://toolbox-docs.marine.copernicus.eu/en/stable/usage/login-usage.html)
- [CDS credentials guide](../cds/cds/cds_create_credentials.md)
