import matplotlib.pyplot as plt
import numpy as np

# Dijkstra's: no preprocessing
# Dijkstra: O((V + E)logV)
def f1(x):
    return x * 0

# Contraction Hierarchies: O(V^2 E)
def f2(x):
    return x ** 2

# Hub-labeling: O(VE)
# Hub-labeling: O(|L_f(s)| + |L_b(t)|)
def f3(x):
    return x

# Arc-flags: O(knlogn) = O(kVlogV)
def f4(x):
    return x * np.log2(x)

x = np.linspace(0, 50, 10000)

y1 = f1(x)
y2 = f2(x)
y3 = f3(x)
y4 = f4(x)

# Create plot
plt.figure()

# Plot each function as a separate series
plt.plot(x, y1, label='Dijkstra')
plt.plot(x, y2, label='Contraction Hierarchies')
plt.plot(x, y3, label='Hub-Labeling')
plt.plot(x, y4, label='Arc-flags')

# Add labels and legend
plt.xlabel('Number of Nodes')
plt.ylabel('Running Time')
plt.title('Preprocessing Time for Transportation Routing Algorithms')
plt.legend()

plt.grid(True)
plt.show()