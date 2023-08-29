import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Use seaborn-whitegrid style
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "Times New Roman"  

# Data
data_raw_1 = {
    "Bose_speaker": {
        "data.api.bose.io": 20.37,
        "iot.api.bose.io": 0.43,
        "users.api.bose.io": 0.54,
        "0.bose.pool.ntp.org": 0.02,
        "media.bose.io": 0.09,
        "ota.cdn.bose.io": 76.53,
        "adhj3uk4ouxyr.iot.us-east-1.amazonaws.com": 2.03
    },
    "Furbo": {
        "ai.furbo.co": 72.03,
        "product.furbo.co": 26.24,
        "firehose.us-east-1.amazonaws.com": 0.48,
        "cloud-recording-de.s3.amazonaws.com": 1.16,
    },
    "Blink": {
        "ccs-e002.immedia-semi.com": 5.27,
        "IS-cam-e002.immedia-semi.com": 11.83,
        "rest-hw-e002.immedia-semi.com": 1.16,
        "MS-cam-e002.immedia-semi.com": 81.75
    },
    "Google_nest": {
        "nest-camera-media.googleapis.com": 16.92,
        "time.google.com": 0.54,
        "clients1.google.com": 0.77,
        "lycraservice-pa-cam-prod.googleapis.com": 1.61,
        "connectivitycheck.gstatic.com": 7.66,
        "69.101.228.35.bc.googleusercontent.com": 57.46,
        "clients3.google.com": 0.56,
        "56.128.205.35.bc.googleusercontent.com": 7.35,
        "251.10.228.35.bc.googleusercontent.com": 6.37,
        "199.159.88.34.bc.googleusercontent.com": 0.19,
        "154.27.233.35.bc.googleusercontent.com": 0.15,
        "238.118.88.34.bc.googleusercontent.com": 0.16,
        "122.130.76.34.bc.googleusercontent.com": 0.25,
    },
    "govee_strip_light": {
        "pool.ntp.org": 5.89,
        "app.govee.com": 16.36,
        "aqm3wd1qlc3dy.iot.us-east-1.amazonaws.com": 76.67
    }
}

data_raw_2 = {
    "google_pixel_watch": {
        "connectivitycheck.gstatic.com": 4.46,
        "time.android.com": 0.01,
        "play.googleapis.com": 89.56,
        "www.google.com": 5.97,
    },
    "cosori_air_fryer": {
        "vdmpmqtt.vesync.com": 99.72,
        "ntp.vesync.com": 0.28,
        "time.nist.gov": 0.00,
        "cn.pool.ntp.org": 0.00,
    },
    "boifun_baby": {
        "meari-eu.oss-eu-central-1.aliyuncs.com": 94.72,
        "apis.cloudedge360.com": 0.03,
        "euce.mearicloud.com": 0.02,
        "apis-eu-frankfurt.cloudedge360.com": 5.23,
    },
    "eufy_roboyac": {
        "m2.tuyaus.com": 95.80,
        "a3.tuyaus.com": 4.06,
        "fireware-ttls.tuyaus.com": 0.14,
    },
    "lifx_mini": {
        "v2.broker.lifx.co": 100.00,
    }
}

def filter_and_plot_data(ax, data_raw, color_mapping):
# Filter the domain names whose Packet Ratio is less than 0.1%, and sort them in descending order
    filtered_data = {}
    for device, domains in data_raw.items():
        sorted_domains = {k: v for k, v in sorted(domains.items(), key=lambda item: item[1], reverse=True)}
        filtered_data[device] = {domain: ratio for domain, ratio in sorted_domains.items() if ratio >= 0.1}
    
    bar_width = 0.7
    small_gap = 0.2
    group_gap = 1.5
    num_domains = max(len(domains) for _, domains in filtered_data.items())
    device_width = (bar_width + small_gap) * num_domains + group_gap - small_gap

    for idx, (device_name, domains) in enumerate(filtered_data.items()):
        ratios = list(domains.values())
        domain_names = list(domains.keys())
        positions = [device_width * idx + i * (bar_width + small_gap) for i in range(len(domain_names))]
        ax.bar(positions, ratios, width=bar_width, label=device_name, color=color_mapping[device_name])

        for position, domain in zip(positions, domain_names):
            ax.text(position, -1.5, domain, ha='center', va='top', rotation=90, fontsize=10)

    ax.set_xticks([])
    ax.set_ylabel('Communication Times (%)')
    ax.set_ylim(0, 110)

# Generate a palette for all devices (both groups)
all_devices = list(data_raw_1.keys()) + list(data_raw_2.keys())
color_palette = sns.color_palette("husl", n_colors=len(all_devices))
color_mapping = {device: color for device, color in zip(all_devices, color_palette)}


fig, axs = plt.subplots(2, 1, figsize=(15, 16))

filter_and_plot_data(axs[0], data_raw_1, color_mapping)
axs[0].set_title('Communication Times in Percentage of Domains(1)')

filter_and_plot_data(axs[1], data_raw_2, color_mapping)
axs[1].set_title('Communication Times in Percentage of Domains(2)')

# Adding unified legend
handles = [plt.Line2D([0], [0], color=color_mapping[device], lw=4) for device in all_devices]
plt.legend(handles=handles, labels=all_devices, loc="upper left", bbox_to_anchor=(1, 2.3), title="Devices")

plt.tight_layout()
plt.show()
