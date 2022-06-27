# Volcanoes & Population - WebMap Project using Folium and Pandas:

import folium
import pandas

data = pandas.read_csv("Assets/Volcanoes.txt")

LAT = list(data["LAT"])
LON = list(data["LON"])
ELEV = list(data["ELEV"])
NAME = list(data["NAME"])

# Adding the HTML variable for styling and redirecting the popup:
HTML = """
Volcano name: <br>
<a href="https://google.com/search?q=%%22%s%%22" target="_blank">%s<a/><br>
Height: %s m
"""


# Creating a function to change the color depending on the elevation:

def color_changer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 < elevation < 3000:
        return "orange"
    else:
        return "red"


my_map = folium.Map(location=[43.92, -120.38], zoom_start=5, tiles="Stamen Terrain")

fg_volcanoes = folium.FeatureGroup(name="Volcanoes")

# Using a for loop to add multiple markers on the map:
for lat, lon, elev, name in zip(LAT, LON, ELEV, NAME):
    iframe = folium.IFrame(html=HTML % (name, name, elev), width=180, height=100)
    fg_volcanoes.add_child(
        folium.CircleMarker(location=(lat, lon), radius=8, popup=folium.Popup(iframe), fill_color=color_changer(elev),
                            color="grey", fill_opacity=1))

fg_population = folium.FeatureGroup(name="Population")

# We add a 2nd polygon layer to our map:
fg_population.add_child(folium.GeoJson(data=open("Assets/world.json", "r", encoding="utf-8-sig").read(),
                                       style_function=lambda x: {
                                           'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                           else 'orange' if 10000000 <= x['properties'][
                                               'POP2005'] < 20000000 else 'red'}))

my_map.add_child(fg_volcanoes)
my_map.add_child(fg_population)

my_map.add_child(folium.LayerControl())

my_map.save("Map.html")
