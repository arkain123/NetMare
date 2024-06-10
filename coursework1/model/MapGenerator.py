import folium


class MapGenerator:
    def __init__(self):
        self.map = folium.Map()

    def add_marker(self, location, popup):
        folium.Marker(location, popup=popup).add_to(self.map)

    def show(self):
        self.map.save('map.html')