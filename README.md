# generative-poster
# Generative Abstract Poster
# Concepts: randomness, lists, loops, functions, matplotlib

import random
import math
import numpy as np
import matplotlib.pyplot as plt

def random_palette(k=5):
    # return k random warm colors
    warm_colors = [
        (0.8, 0.2, 0.2),  # Reddish
        (0.9, 0.5, 0.1),  # Orangeish
        (0.9, 0.7, 0.2),  # Yellowish
        (0.7, 0.3, 0.1),  # Darker Orange
        (0.6, 0.1, 0.1)   # Darker Red
    ]
    return random.sample(warm_colors, k)

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    # generate a wobbly closed shape
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

random.seed()  # different art each run
plt.figure(figsize=(7,10))
plt.axis('off')

# background
plt.gca().set_facecolor((0.98,0.98,0.97))

palette = random_palette(5)
n_layers = 8
for i in range(n_layers):
    cx, cy = random.random(), random.random()
    rr = random.uniform(0.15, 0.45)
    x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(0.1,0.35))
    color = random.choice(palette)
    alpha = random.uniform(0.25, 0.6)
    plt.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

# simple typographic label
plt.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=plt.gca().transAxes)
plt.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=plt.gca().transAxes)

plt.xlim(0,1); plt.ylim(0,1)
plt.show()
