# libraries
import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 1/4

# set height of bar
bars1 = np.random.random_integers(1,100,10)
print(bars1)
bars2 = np.random.random_integers(1,100,10)
bars3 = np.random.random_integers(1,100,10)
bars4 = np.random.random_integers(1,100,10)

# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='var1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='var2')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
plt.bar(r4, bars4, color='#2d7f5e', width=barWidth, edgecolor='white', label='var4')

# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(bars1))], ['A', 'B', 'C', 'D', 'E'])

# Create legend & Show graphic
plt.legend()
plt.show()
