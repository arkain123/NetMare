import math
import subprocess
import folium
import requests
from model.MapGenerator import MapGenerator as mg


class Traceroute:
    def __init__(self, destination, timeout=1, maxhops=30):
        self.destination = destination
        self.timeout = math.floor(float(timeout))
        self.maxhops = maxhops

    def trace(self):
        command = f"tracert -h {self.maxhops} -w {self.timeout} {self.destination}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            hops = []
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith(' '):
                    try:
                        hop_info = line.split()
                        hop_ip = hop_info[7]
                        hop_rtt = hop_info[1]
                        hops.append({"ip": hop_ip, "rtt": hop_rtt})
                    except:
                        hop_ip = "*"
                        hop_rtt = "*"
                        hops.append({"ip": hop_ip, "rtt": hop_rtt})
            return {"host": self.destination, "hops": hops}
        else:
            return None

    def add_marker(self, location, popup):
        folium.Marker(location, popup=popup).add_to(self.map)

    def show(self):
        self.map.save('map.html')