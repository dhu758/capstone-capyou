import folium

my_location = [37.498310,127.025232]
map = folium.Map(location=my_location, zoom_start=25)
folium.Marker(my_location, popup='destination').add_to(map)
map.save('./index.html')
map