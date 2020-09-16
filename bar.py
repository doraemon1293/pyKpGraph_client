# libraries
import numpy as np
import matplotlib.pyplot as plt

# set width of bar
# barWidth = 1/

# set height of bar
bars = np.random.random_integers(1,100,50)


# Set position of bar on X axis


# Make the plot
plt.bar(range(len(bars)),bars, color='#7f6d5f',  label='var1')

# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r for r in range(len(bars))], ['A', 'B', 'C', 'D', 'E'])

# Create legend & Show graphic
plt.legend()
plt.show()
