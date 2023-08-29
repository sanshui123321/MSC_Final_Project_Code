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
local = [0.92, 0.21, 0.36, 16.84, 22.94, 8.84, 11.92, 16.07, 2.79, 19.74]
server = [99.08, 99.79, 99.64, 83.16, 77.06, 91.16, 88.08, 83.93, 97.21, 80.26]

# Sort devices based on local traffic
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
plt.title('Local vs Server Traffic for Devices in Data Volume')
plt.xticks(index, devices, rotation=45, ha="right") 
plt.legend(loc='upper right', frameon=True)
plt.tight_layout()  
plt.show()
