import requests
import pandas as pd

#overpassAPi
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"
#set box
OC_BBOX = "33.5, -118.15, 33.95, -117.40"

query = f"""
[out:json];
(
  node["amenity"="restaurant"]({OC_BBOX});
  node["tourism"="attraction"]({OC_BBOX});
);
out body;
"""

print("downloading restaurant/attracton data")
response = requests.post(OVERPASS_URL, data={"data": query})
response.raise_for_status()
data = response.json()

records = []
for element in data["elements"]:
    tags = element.get("tags", {})

    if tags.get("amenity") == "restaurant":
        poi_type = "restaurant"
    else:
        poi_type = "attraction"

    records.append({
        "name" : tags.get("name", ""),
        "poi_type" : poi_type,
        "latitude" : element["lat"],
        "longitude" : element["lon"],
    })

poi_df = pd.DataFrame(records)
print(f"found {len(poi_df)} restaurants / attractions in the area")

poi_df.to_csv("../../data/raw/oc_poi.csv", index=False)
print(f"saved to oc_poi.csv")