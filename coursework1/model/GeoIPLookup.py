import requests


class IPGeolocation:

    def __init(self):
        self.data = {}
    def get_location(self, ip_address):
        url = f"http://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        self.data = response.json()
        if 'loc' in self.data:
            lat, lon = self.data['loc'].split(',')
            return float(lat), float(lon)
        else:
            return None

    def get_result(self):
        return self.data
