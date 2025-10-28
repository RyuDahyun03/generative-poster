# generative-poster
import random, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import ipywidgets as widgets
from ipywidgets import interact
import pandas as pd
import os

# Flower shape
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15, petals=5):
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    # Flower shape formula (adjusting radius based on angle and number of petals)
    radii  = r * (1 + wobble * (np.sin(angles * petals) + 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

    
PALETTE_FILE = "palette.csv"

# Initialize palette.csv if not exists
if not os.path.exists(PALETTE_FILE):
    df_init = pd.DataFrame([
        {"name":"sky", "r":0.4, "g":0.7, "b":1.0},
        {"name":"sun", "r":1.0, "g":0.8, "b":0.2},
        {"name":"forest", "r":0.2, "g":0.6, "b":0.3}
    ])
    df_init.to_csv(PALETTE_FILE, index=False)

def read_palette():
    return pd.read_csv(PALETTE_FILE)

def add_color(name, r, g, b):
    df = read_palette()
    df = pd.concat([df, pd.DataFrame([{"name":name,"r":r,"g":g,"b":b}])], ignore_index=True)
    df.to_csv(PALETTE_FILE, index=False)
    print(f"Added {name}")

def update_color(name, r=None, g=None, b=None):
    df = read_palette()
    if name in df["name"].values:
        idx = df.index[df["name"]==name][0]
        if r is not None: df.at[idx,"r"] = r
        if g is not None: df.at[idx,"g"] = g
        if b is not None: df.at[idx,"b"] = b
        df.to_csv(PALETTE_FILE, index=False)
        print(f"Updated {name}")
    else:
        print(f"{name} not found")

def delete_color(name):
    df = read_palette()
    df = df[df["name"]!=name]
    df.to_csv(PALETTE_FILE, index=False)
    print(f"Deleted {name}")

def load_csv_palette():
    df = read_palette()
    return [(row.r, row.g, row.b) for row in df.itertuples()]

palette_csv = load_csv_palette()
print("Loaded palette:", palette_csv)

import matplotlib.pyplot as plt

def show_palette(palette):
    plt.figure(figsize=(6,2))
    for i, c in enumerate(palette):
        plt.fill_between([i, i+1], 0, 1, color=c)
        plt.text(i+0.5, -0.1, f"{i+1}", ha="center", va="top")
    plt.axis("off")
    plt.show()

# Show the loaded CSV palette
show_palette(palette_csv)


def make_palette(k=6, mode="pastel", base_h=0.60):
    cols = []
    if mode == "csv":
        return load_csv_palette()

    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15,0.35); v = random.uniform(0.9,1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8,1.0);  v = random.uniform(0.8,1.0)
        elif mode == "mono":
            h = base_h;         s = random.uniform(0.2,0.6);   v = random.uniform(0.5,1.0)
        else: # random
            h = random.random(); s = random.uniform(0.3,1.0); v = random.uniform(0.5,1.0)
        cols.append(tuple(hsv_to_rgb([h,s,v])))
    return cols

def draw_poster(n_layers=8, wobble_poster=0.15, palette_mode="pastel", seed=0, blob_r=0.3, blob_wobble=0.15, blob_petals=5):
    random.seed(seed); np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(6,8))
    ax.axis('off')
    ax.set_facecolor((0.97,0.97,0.97))

    palette = make_palette(6, mode=palette_mode)
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        # Use blob_r for the base radius
        rr = random.uniform(blob_r * 0.5, blob_r * 1.5) # Vary radius around the base blob_r
        # Pass blob_wobble and blob_petals to the blob function
        x, y = blob((cx,cy), r=rr, wobble=blob_wobble, petals=blob_petals)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)

        # Simulate blurring by drawing multiple overlapping shapes
        for i in range(5): # Draw 5 layers for blur effect
            offset_x = random.uniform(-0.005, 0.005)
            offset_y = random.uniform(-0.005, 0.005)
            ax.fill(x + offset_x, y + offset_y, color=color, alpha=alpha / (i + 1), edgecolor='none')

    ax.text(0.05, 0.95, f"Interactive Poster • {palette_mode}",
            transform=ax.transAxes, fontsize=12, weight="bold")
    plt.show()

    from ipywidgets import interact
import ipywidgets as widgets

interact(
    draw_poster,
    n_layers=widgets.IntSlider(min=3,max=20,step=1,value=8, description="Layers"),
    wobble_poster=widgets.FloatSlider(min=0.01,max=9.0,step=0.01,value=0.15, description="Poster Wobble"),
    palette_mode=widgets.Dropdown(options=["pastel","vivid","mono","random","csv"], value="pastel"),
    seed=widgets.IntSlider(min=0,max=9999,step=1,value=0, description="Seed"),
    blob_r=widgets.FloatSlider(min=0.05,max=0.8,step=0.01,value=0.3, description="Blob Radius"),
    blob_wobble=widgets.FloatSlider(min=0.01,max=2.0,step=0.01,value=0.15, description="Blob Wobble"),
    blob_petals=widgets.IntSlider(min=1,max=10,step=1,value=5, description="Blob Petals")
);
