import pandas as pd
import requests

#download links
DMV_URL = "https://data.ca.gov/dataset/15179472-adeb-4df6-920a-20640d02b08c/resource/b459d957-5d94-4b10-999d-770419870364/download/vehicle-fuel-type-counts-2025.csv"
ZCTA_COUNTY_URL = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt"


#FIPS code for compliance with the column in ZCTA
#Used to filter for Orange Conty rows.... 06059 = Orange County
Orange_County_FIPS = "06059"

print("Downloading DMV dataset")
dmv_response = requests.get(DMV_URL)
dmv_response.raise_for_status() # if the request fails tell user
with open ("dmv_fuel_type_by_zip_2025.csv", "wb") as f:
    f.write(dmv_response.content)

#download ztc files/save
print("Downloading zip code to county data")
zcta_response = requests.get(ZCTA_COUNTY_URL)
zcta_response.raise_for_status()
with open("zcta_county_2020.txt", "wb") as f:
    f.write(zcta_response.content)


#load files into pandas
#dtype=str keeps zip codes as strings
dmv = pd.read_csv("dmv_fuel_type_by_zip_2025.csv", dtype=str, low_memory=False)
zcta = pd.read_csv("zcta_county_2020.txt", sep="|", dtype=str)

# which zip codes in OC?
is_orange_county = zcta["GEOID_COUNTY_20"] == Orange_County_FIPS
oc_zip_codes = zcta.loc[is_orange_county, "GEOID_ZCTA5_20"].unique()
print(f"found {len(oc_zip_codes)} Orange County zip codes")

#filter dmv data to these zip codes
is_in_oc = dmv["ZIP Code"].isin(oc_zip_codes)
dmv_oc = dmv[is_in_oc]
print(f"{len(dmv_oc)} DMV rows are in orange county")

#save oc zip codes to new file
dmv_oc.to_csv("ocDmvFuelTypeByZip.csv", index=False)
print("saved ocDmvFuelTypeByZip.csv")