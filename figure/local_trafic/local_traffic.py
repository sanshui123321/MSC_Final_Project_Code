import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams['font.family'] = 'Times New Roman'

# Data
data = {
    'Bose_speaker': {'DHCP': 11.15, 'ICMP': 83.96, 'TCP': 3.69, 'UDP': 0.58, 'Other': 0.62},
    'Furbo': {'DHCP': 28.15, 'UDP': 63.83, 'ICMP': 5.47, 'TCP': 2.34, 'Other': 0.21},
    'Blink': {'DHCP': 70.22, 'ICMP': 29.78, 'Other': 0},
    'Google_nest': {'DHCP': 2.98, 'TCP': 9.05, 'TLSv1.2': 5.98, 'CLASSIC-STUN': 81.66, 'Other': 0.33},
    'Govee_strip_light': {'DHCP': 95.92, 'TCP': 3.70, 'Other': 0.37},
    'Google_pixel_watch': {'DHCP': 99.86, 'ICMP': 0.11, 'Other': 0.03},
    'Cosori_air_fryer': {'DHCP': 99.58, 'Other': 0.42},
    'Boifun_baby': {'ICMP': 89.13, 'DHCP': 4.65, 'UDP': 2.64, 'STUN': 3.03, 'Other': 0.54},
    'Eufy_roboyac': {'DHCP': 80.18, 'TCP': 18.64, 'IPDC': 1.11, 'Other': 0.07},
    'Lifx_mini': {'DHCP': 81.13, 'TCP': 16.55, 'UDP': 2.28, 'Other': 0.04},
}

df = pd.DataFrame(data).T
df = df.fillna(0)

# Move the 'Other' column to the end
order = [column for column in df if column != 'Other'] + ['Other']
df = df[order]

df = df.sort_values(by=df.columns[0], ascending=False)

# Use seaborn-whitegrid style and light colors
plt.style.use("seaborn-whitegrid")
cmap = plt.cm.get_cmap("Pastel1", len(df.columns))

# resize the image
fig, ax = plt.subplots(figsize=(10, 8))

# Draw a stacked histogram
bottom = [0] * len(df)
bars = []
for idx, column in enumerate(df.columns):
    bar = plt.barh(df.index, df[column], left=bottom, color=cmap(idx), label=column)
    bars.append(bar)
    bottom += df[column]

# Show legend
plt.legend(handles=bars, title='Protocols', bbox_to_anchor=(1.05, 0.5), loc='center left')


plt.xlabel("Percentage")
plt.ylabel("Devices")
plt.title("Protocol Distribution by Device in Local Traffic")
plt.tight_layout()
plt.show()
