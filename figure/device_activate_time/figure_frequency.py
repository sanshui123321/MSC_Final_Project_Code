import matplotlib.pyplot as plt

def transform_y(y):
    """Conversion function: the part less than or equal to 20 remains unchanged, and the part greater than 20 is divided by 10 plus 18"""
    return y if y <= 20 else y/10 + 18

# Data
Bose_speaker = [2.7228, 2.7109, 2.7513, 2.7061, 2.7054, 2.767, 2.7458, 2.7433, 2.7026, 2.7041, 2.8267, 2.8814, 20.7112, 2.8124, 15.7589, 5.5401, 3.0021, 2.9161, 2.7802, 2.7556, 2.6684, 2.7157, 2.6659, 2.706]
Furbo = [4.2977, 4.0425, 1.8966, 0.1915, 0.2028, 0.2098, 0.1887, 0.1938, 0.2607, 0.3318, 4.4206, 7.005, 10.6375, 5.1243, 3.651, 16.6307, 13.1275, 11.5786, 4.1278, 1.5518, 0.3239, 0.441, 5.5567, 4.0077]
Google_nest = [3.2505, 3.851, 3.8048, 4.0974, 3.5455, 3.1253, 2.4089, 2.5896, 0.4404, 0.748, 1.9178, 2.2237, 2.418, 8.6577, 4.8802, 4.6152, 5.1879, 4.6447, 5.6522, 6.8742, 9.962, 9.6012, 2.8989, 2.6049]
Govee_strip_light = [4.3012, 4.1441, 4.2695, 4.1292, 4.2926, 4.0672, 4.2404, 4.2532, 4.1102, 4.1141, 4.2321, 4.1101, 4.1483, 3.9547, 4.03, 4.0616, 4.1584, 4.0105, 4.2405, 4.1485, 4.3039, 4.1802, 4.2154, 4.2839]
Google_pixel_watch = [0.5617, 0.8275, 0.6123, 0.9107, 0.5045, 0.4296, 0.9129, 24.3162, 0.8069, 0.9145, 1.2456, 0.6443, 0.9066, 12.3243, 3.0182, 0.7643, 9.7779, 3.8651, 27.2063, 5.4914, 1.0108, 0.7914, 1.1947, 0.9624]
Cosori_air_fryer = [4.1181, 4.1159, 4.1249, 4.118, 4.1107, 4.1224, 4.1134, 4.1069, 4.118, 4.1457, 4.206, 4.1584, 4.2247, 4.2749, 4.2639, 4.4294, 4.2356, 4.2155, 4.1651, 4.1465, 4.1176, 4.1266, 4.1179, 4.124]
Boifun_baby = [2.4106, 2.3793, 2.3369, 2.2957, 2.28, 2.6217, 2.582, 2.4508, 4.9447, 3.7539, 4.8195, 5.3665, 6.2905, 5.1513, 5.6814, 6.826, 9.4611, 8.7986, 4.38, 3.2948, 3.3978, 2.9774, 2.7848, 2.7146]
eufy_roboyac = [4.1471, 4.1483, 4.1473, 4.1639, 4.1484, 4.1471, 4.1484, 4.1529, 4.1798, 4.2258, 4.2241, 4.1279, 4.154, 4.1893, 4.1845, 4.2549, 4.1837, 4.1465, 4.1505, 4.1477, 4.1549, 4.1681, 4.1596, 4.1456]
Lifx_mini = [4.1166, 4.1233, 4.1123, 4.1085, 4.1176, 4.1161, 4.1131, 4.1195, 4.1363, 4.3471, 4.1454, 4.1192, 4.3288, 4.1129, 4.1428, 4.1642, 4.1921, 4.3311, 4.3832, 4.1473, 4.122, 4.1234, 4.1283, 4.1491]
Blink = [0] * 24
Blink[12] = 84.6262
Blink[15] = 15.3738

# Convert data
transformed_data_lists = [list(map(transform_y, data_list)) for data_list in [Bose_speaker, Furbo, Google_nest, Govee_strip_light, Google_pixel_watch, Cosori_air_fryer, Boifun_baby, eufy_roboyac, Lifx_mini, Blink]]

# Set the overall style
plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(18, 10))

font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
plt.rc('font', **font)

# Create a colormap
colors = plt.get_cmap('tab10')

# Plot data
devices = ["Bose_speaker", "Furbo", "Google_nest", "Govee_strip_light", "Google_pixel_watch", "Cosori_air_fryer", "Boifun_baby", "eufy_roboyac", "Lifx_mini", "Blink"]

# Modify the data points of the x-axis
x_data = [i+0.5 for i in range(24)]

for idx, (device, data_list) in enumerate(zip(devices, transformed_data_lists)):
    plt.plot(x_data, data_list, label=device, color=colors(idx), linewidth=2, marker='o')

# Set title, axis labels and axis ticks
plt.title('Distribution map of communication times in each time period', fontsize=16, fontweight='bold')
plt.xlabel('Time', fontsize=14)
plt.ylabel('Communication Times Percentage', fontsize=14)
hours = [f"{i:02d}:00" for i in range(24)]
plt.xticks(range(24), hours, rotation=45, fontsize=12)

# Set the ticks and labels for the y-axis
y_ticks_transformed = [0, 5, 10, 15, 20, 24, 28]
y_labels = ['0%', '5%', '10%', '15%', '20%', '60%', '100%']
plt.yticks(y_ticks_transformed, y_labels, fontsize=12)
plt.legend(fontsize=12, loc='upper left')
plt.tight_layout()
plt.show()
