import pandas as pd
import requests
import zipfile
import io


#census fule - turns zip into lat/long
CENTROID_URL = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_zcta_national.zip"

print("Downloading zip file")
response = requests.get(CENTROID_URL)
response.raise_for_status()


#unzip the file
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    inner_filename = z.namelist()[0]
    with z.open(inner_filename) as f:
        centroids = pd.read_csv(f, sep="\t", dtype = str)

#filter out any whitespace
#strip out names

centroids.columns = centroids.columns.str.strip()
print("columns found: ", list(centroids.columns))

#reuse zips from gap analysis
gap = pd.read_csv("../../data/processed/oc_charger_gap_analysis.csv", dtype=str)
oc_zips = gap["ZIP Code"].unique()

is_in_oc = centroids["GEOID"].isin(oc_zips)
oc_centroids = centroids[is_in_oc]
print(f"found  centroids for {len(oc_centroids)} of {len(oc_zips)} OC zips")

#save to csv
oc_centroids.to_csv("../../data/raw/oc_zip_centroids.csv", index=False)
print("saved to oc_zip_centroids.csv")








