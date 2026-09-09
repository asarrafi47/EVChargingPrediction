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

#labels
folium.TileLayer(
tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",    attr="Esri",
    name="Labels: Cities/roads",
    overlay=True,
    control=True,
).add_to(m)



#Charging Stations layer
stations_layer = folium.FeatureGroup(name="Charging Stations")
for _, row in stations.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        continue
    
    popup_text = f"{row.get("station_name", "Unknown")}<br>Network:{row.get("ev_network","Unknown")}"
    
    folium.CircleMarker(
        location = [float(row["latitude"]), float(row["longitude"])],
        radius = 3, 
        color = "red",
        fill = True,
        fill_opacity=0.6,
        popup=popup_text,
    ).add_to(stations_layer)




stations_layer.add_to(m)

#Gap analysis filter (ev demand vs existing chargers)
gap_layer = folium.FeatureGroup(name="EV gap Analysis")

for _, row in gap_with_coords.iterrows():
    if pd.isna(row["INTPTLAT"]) or pd.isna(row["INTPTLONG"]):
        continue
    
    city = row["city"] if pd.notna(row["city"]) else "(unknown)"
    color = "blue" if city in false_positives else "brown"

    popup_text = (
        f"{city} (zip {row['ZIP Code']})<br>"
        f"EVs: {row['ev_count']}<br>"
        f"Stations: {row['station_count']}<br>"
        f"Gap: {row['evs_per_station']:.2f}"
    )

    folium.CircleMarker(
        location = [float(row["INTPTLAT"]), float(row["INTPTLONG"])],
        radius = 8, 
        color = color,
        fill = True,
        fill_opacity=0.7,
        popup=popup_text,
    ).add_to(gap_layer)

gap_layer.add_to(m)

folium.LayerControl().add_to(m)











m.save("../../results/oc_ev_map.html")
print("saved ../../results/oc_ev_map.html")








