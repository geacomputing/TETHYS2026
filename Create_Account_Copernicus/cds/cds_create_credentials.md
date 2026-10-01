# Copernicus CDS credentials and the ECMWF Data Stores client

## 1. Create CDS credentials

### Create an account and obtain the key

1. Open the [Climate Data Store](https://cds.climate.copernicus.eu/). In the top-right corner, select **Login – Register**.
2. If you do not have an account, select **Register**, complete registration, and verify the account if requested. Otherwise, select **Login** and sign in.
3. Once signed in, open the [CDSAPI setup page](https://cds.climate.copernicus.eu/how-to-api). You must be logged in to see the personal API-key configuration.
4. Scroll to **Setup the CDS API key** and copy the two lines in the displayed code box: the CDS API URL and your personal access token. The value after `key:` is your API key.



**Important:** do not share the key, include it in screenshots, or commit it to Git.

### Accept the dataset terms of use

For each dataset, open its catalogue page, go to the **Download** form, and use the acceptance control at the bottom to agree to the **Terms of Use**. You can then submit web or API requests. Accepted licences appear in your profile under **Dataset Licences**.

## 2. Install the new client

Use a virtual environment where possible, then install the ECMWF Data Stores client:

```bash
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install ecmwf-datastores-client
```

Alternatively, with conda:

```bash
conda install -c conda-forge ecmwf-datastores-client
```

See **REFERENCES** at the bottom of this file for official links.  

## 3. Configure the client

Create a plain-text file named exactly `.ecmwfdatastoresrc` in your home folder (`~` on Linux/macOS; for example, `C:\Users\<username>` on Windows). Do not use Word or another rich-text editor. Keep the same two-line `url`/`key` layout shown on the logged-in CDS page, replacing the placeholder with your API key:

```yaml
url: https://cds.climate.copernicus.eu/api
key: YOUR-CDS-API-KEY
```

Keep this file private; never add it to Git. The client can also read `ECMWF_DATASTORES_URL` and `ECMWF_DATASTORES_KEY` environment variables.

> **Note:** CDS credentials are different from the credentials for Copernicus Marine. For Copernicus Marine instructions, see [marine_create_credentials.md](../copernicusmarine/marine_create_credentials.md).

## 4. Check access 

```python
from ecmwf.datastores import Client

client = Client()
client.check_authentication() 
```

## References

- [Installation](https://ecmwf.github.io/ecmwf-datastores-client/README.html#installation)
- [Configuration and credentials](https://ecmwf.github.io/ecmwf-datastores-client/README.html#configuration)
- [Data download quick start](https://ecmwf.github.io/ecmwf-datastores-client/README.html#quick-start)
- [Interacting with collections, jobs, and results](https://ecmwf.github.io/ecmwf-datastores-client/_api/datastores/index.html)
- [CDS User Guide](https://confluence.ecmwf.int/spaces/CKB/pages/208483517/Climate+Data+Store+CDS+User+Guide)
