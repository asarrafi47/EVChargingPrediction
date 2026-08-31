import pandas as pd

#load datasets
dmv = pd.read_csv("DataCSV/ocDmvFuelTypeByZip.csv", dtype=str)
stations = pd.read_csv("afdc_charging_stations_oc.csv", dtype=str)

zip_to_city = stations.groupby("zip")["city"].first()
zip_to_city.name = "city"

#count of evs / zip code
ev_only = dmv[dmv["Fuel"] == "Battery Electric"].copy()
ev_only["Vehicles"] = ev_only["Vehicles"].astype(int)

#group by zip, sum vehicle counts
ev_by_zip = ev_only.groupby("ZIP Code")["Vehicles"].sum()
ev_by_zip.name = "ev_count"

#count of charging stations / zip
station_by_zip = stations.groupby("zip").size()
station_by_zip.name = "station_count"

#join demand and competition together by zip code
gap = pd.merge(ev_by_zip, station_by_zip, left_index=True, right_index=True, how="left")

#if theres a zip code with no stations, set station_count to 0
gap["station_count"] = gap["station_count"].fillna(0)

#actual gap is the difference between the number of evs and the number of stations
gap["evs_per_station"] = gap["ev_count"] / (gap["station_count"] + 1)

#sort so biggest gaps at the top
gap = gap.sort_values(by="evs_per_station", ascending=False)

#join city names
gap = pd.merge(gap, zip_to_city, left_index=True, right_index=True, how="left")

print(gap.head(15))
gap.to_csv("DataCSV/oc_charger_gap_analysis.csv", index=True)
print("saved to oc_charger_gap_analysis.csv")
