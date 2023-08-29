import matplotlib.pyplot as plt
import numpy as np


plt.style.use('seaborn-whitegrid')
plt.rcParams["font.family"] = "Times New Roman"

# Data
devices = [
    "Bose_speaker", "Furbo", "Blink", "Google_nest",
    "Govee_strip_light", "Google_pixel_watch", "cosori_air_fryer",
    "Boifun_baby", "eufy_roboyac", "lifx_mini"
]
local = [1.03, 0.64, 0.78, 50.18, 6.49, 13.47, 4.30, 23.16, 2.05, 5.24]
server = [98.97, 99.36, 99.22, 49.82, 93.51, 86.53, 96.60, 76.84, 97.95, 94.76]

# # Sort devices based on local traffic
sorted_indices = np.argsort(local)[::-1]
devices = [devices[i] for i in sorted_indices]
local = [local[i] for i in sorted_indices]
server = [server[i] for i in sorted_indices]

local_color = '#a8dadc'
server_color = '#ffb4a2'

bar_width = 0.5
index = np.arange(len(devices))
plt.bar(index, local, bar_width, label='Local Traffic', color=local_color, edgecolor='black')
plt.bar(index, server, bar_width, bottom=local, label='Server Traffic', color=server_color, edgecolor='black')

# Set the title, abscissa and ordinate labels of the graph
plt.xlabel('Devices')
plt.ylabel('Traffic Percentage (%)')
plt.title('Local vs Server Traffic for Devices in Communication Times')
plt.xticks(index, devices, rotation=45, ha="right")  
plt.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.show()
