from dotenv import load_dotenv
import os
import pandas as pd
import requests

load_dotenv()
api_key = os.environ["NREL_API_KEY"]

AFDC_URL = "https://developer.nlr.gov/api/alt-fuel-stations/v1.json"

# same fips code as in pullEvData.py
Orange_County_FIPS = "06059"

print("Downloading AFDC charging station data")
params = {
    "api_key": api_key,
    "fuel_type": "ELEC",
    "state": "CA",
    "limit": "all",
}
afdc_response = requests.get(AFDC_URL, params=params)
afdc_response.raise_for_status()

#json has key holding list of stations
stations = afdc_response.json()["fuel_stations"]
stations_df = pd.DataFrame(stations)
stations_df["zip"] = stations_df["zip"].astype(str)
print(f"found {len(stations_df)} charging stations")

#which zips in OC?
zcta = pd.read_csv("DataTXT/zcta_county_2020.txt", sep="|", dtype=str)
is_orange_county = zcta["GEOID_COUNTY_20"] == Orange_County_FIPS
oc_zip_codes = zcta.loc[is_orange_county, "GEOID_ZCTA5_20"].unique()


#filter down to only OC zip codes
is_in_oc = stations_df["zip"].isin(oc_zip_codes)
stations_oc = stations_df[is_in_oc]
print(f"found {len(stations_oc)} charging stations in Orange County")

#save to csv
stations_oc.to_csv("afdc_charging_stations_oc.csv", index=False)
print("saved to afdc_charging_stations_oc.csv")

