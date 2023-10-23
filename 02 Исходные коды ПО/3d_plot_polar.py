import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

# Create data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Increase the size of the plot window
fig = plt.figure(figsize=(10, 8))  # Set width=10 inches, height=8 inches
ax = fig.add_subplot(111, projection='3d')

# Create light source object
light_source = LightSource(azdeg=315, altdeg=45)

# Calculate hillshading
rgb = light_source.shade(Z, cmap=plt.cm.cool)

# Plot the surface with hillshading
surf = ax.plot_surface(X, Y, Z, facecolors=rgb, rstride=1, cstride=1)

# Add a color bar
fig.colorbar(surf)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Custom Hillshading in 3D Surface Plot')

# Enable interactive mode
plt.ion()

# Show the plot
plt.show()

# Keep the plot window open until it is closed
plt.pause(0.001)
input("Press enter to close the plot.")
plt.close()
