import pandas as pd
import requests

#Caltrans traffic counts, arcGis rest api doesnt need an api key

AADT_URL = "https://gisdata.dot.ca.gov/arcgis/rest/services/CHhighway/Traffic_AADT/MapServer/0/query"

# only get orange county records

params = {"where": "CNTY='ORA'", "outFields": "*", "f": "json", "outSR": "4326"}

response = requests.get(AADT_URL, params=params)
response.raise_for_status()
data = response.json()


records = []
for feature in data["features"]:
    row = feature["attributes"]
    row["longitude"] = feature["geometry"]["x"]
    row["latitude"] = feature["geometry"]["y"]
    records.append(row)


aadt_df = pd.DataFrame(records)
print(f"found {len(aadt_df)} traffic count locations in orange county")


#original results have duplicates, dropping...
aadt_df = aadt_df.drop_duplicates(subset=aadt_df.columns.difference(["OBJECTID"]))
print(f"{len(aadt_df)} unique traffic count locations after dropping duplicates")


aadt_df.to_csv("../../data/raw/oc_aadt_traffic.csv", index=False)
print("saved to oc_aadt_traffic.csv")