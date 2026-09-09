import folium
import pandas as pd


#load data
gap = pd.read_csv("../../data/processed/oc_charger_gap_analysis.csv", dtype=str)
centroids = pd.read_csv("../../data/raw/oc_zip_centroids.csv", dtype=str)
stations = pd.read_csv("../../data/raw/afdc_charging_stations_oc.csv", dtype=str)

#convert to floasts
gap["evs_per_station"] = gap["evs_per_station"].astype(float)

#join gap analysis to zip coordinates
gap_with_coords = pd.merge(gap, centroids[["GEOID", "INTPTLAT", "INTPTLONG"]], 
left_on="ZIP Code", right_on="GEOID", how="left")

#from traffic check falso positives
false_positives = ["Coto De Caza", "Rancho Santa Margarita"]

# base map
m = folium.Map(location = [33.7, -117.8], zoom_start=10)

# satellite view
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri, Maxar, Earthstar Geographics",
    name="Satellite",
).add_to(m)

m.save("../../results/oc_ev_map.html")
print("saved ../../results/oc_ev_map.html")








