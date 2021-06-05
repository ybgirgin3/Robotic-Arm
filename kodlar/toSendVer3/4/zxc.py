import numpy as np
import matplotlib.pyplot as plt

path = steps = np.random.normal(size=(3600,2))

# pos(n) = pos(n-1) + step(n)
for n in range(path.shape[0]-1):
    path[n+1] += path[n]

# Compact way to plot x and y: (3600,2) -> (2,3600) and the * expand along the first axis
plt.plot(*path.T)
plt.show()
