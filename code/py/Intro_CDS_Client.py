"""
TETHYS 2026 | Hands-on Training
By GEA Computing Ltd

Browse the CDS catalogue and inspect an ERA5 collection.
"""

import logging
from datetime import datetime, timezone

from ecmwf.datastores import Client


# Show useful progress messages from the client.
logging.basicConfig(level=logging.INFO)

# Create the client using the saved ECMWF Data Stores credentials.
client = Client()

# Confirm that the credentials work.
client.check_authentication()
print("Authentication successful.")

print("")
print("Querying Catalogue...")

# List collection IDs, following all catalogue pages.
collections = client.get_collections(sortby="update")
collection_ids = []

while collections is not None:
    collection_ids.extend(collections.collection_ids)
    collections = collections.next

print("\nCatalogue collections:")
c= 1
for collection_id in collection_ids:
    print(f"{c}) {collection_id}")
    c = c+1


# Select a collection and inspect its metadata.
collection_id = "reanalysis-era5-pressure-levels"
print(3*"\n")
print(25*"-")
print(2*"\n")
print(f"Inspecting {collection_id}:")
collection = client.get_collection(collection_id)


attributes = [
    "title",
    "published_at",
    "updated_at",
    "begin_datetime",
    "end_datetime",
    "bbox",
]

for attribute in attributes:
    value = getattr(collection, attribute, None)
    print(f"\t[+]{attribute}: {value}")

    # Calculate how many days ago the collection was last updated.
    if attribute == "updated_at" and value is not None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        age_days = (datetime.now(timezone.utc) - value).days
        print(f"\t\t Days since update: {age_days}")


# Optional: set to True to request and download a small ERA5 sample.
DOWNLOAD_EXAMPLE = True

if DOWNLOAD_EXAMPLE:
    fileout= "era5_sample.nc"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["temperature"],
        "year": ["2022"],
        "month": ["01"],
        "day": ["01"],
        "time": ["00:00"],
        "pressure_level": ["1000"],
        "data_format": "netcdf",
        "download_format": "unarchived",
    }

    client.retrieve(
        collection_id,
        request,
        target=fileout, # this is the output file
    )
    print(f"Downloaded: {fileout}")