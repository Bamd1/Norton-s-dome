import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Corrected dome function (inverted correctly)
def dome_function(r):
    with np.errstate(invalid='ignore'):
        result = (2/3)*(1 - (1 - (3/2)*r)**(2/3))**(3/2)
        result = np.where(r > 2/3, np.nan, result)
    return result

# Generate dome surface
x = np.linspace(-0.7, 0.7, 300)
y = np.linspace(-0.7, 0.7, 300)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = dome_function(r)
z = np.nanmax(z) - z  # Invert dome correctly

# Plotting
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot dome
ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none', antialiased=True, alpha=0.8)

# Adjust ball position correctly (ball sitting exactly on top)
ball_radius = 0.03
phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
x_ball = ball_radius * np.cos(phi) * np.sin(theta)
y_ball = ball_radius * np.sin(phi) * np.sin(theta)
z_ball = ball_radius * np.cos(theta) + np.nanmax(z) + ball_radius  # Ball bottom at dome top

ax.plot_surface(x_ball, y_ball, z_ball, color='red', zorder=10)

# Labels and title
ax.set_title('3D Norton Dome with Ball at Top', fontsize=15)
ax.set_xlabel('X Axis', fontsize=12)
ax.set_ylabel('Y Axis', fontsize=12)
ax.set_zlabel('Z Axis', fontsize=12)

# Set realistic aspect ratio
ax.set_box_aspect([1,1,0.5])

plt.show()
