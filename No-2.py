import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# Constants
ball_radius = 0.03
g = 9.8
time_step = 0.02
positions = []  # Ensure global positions list exists

# Dome function
def dome_function(r):
    with np.errstate(invalid='ignore'):
        result = (2/3)*(1 - (1 - (3/2)*r)**(2/3))**(3/2)
        result = np.where(r > 2/3, np.nan, result)
    return result

# Dome slope
def dome_slope(r):
    dr = 1e-5
    return (dome_function(r + dr) - dome_function(r - dr)) / (2 * dr)

# Generate dome surface
x = np.linspace(-0.7, 0.7, 300)
y = np.linspace(-0.7, 0.7, 300)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = dome_function(r)
z = np.nanmax(z) - z

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='plasma', alpha=0.95)

# Initial ball position
def initial_ball():
    phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x_ball = ball_radius * np.cos(phi) * np.sin(theta)
    y_ball = ball_radius * np.sin(phi) * np.sin(theta)
    z_ball = ball_radius * np.cos(theta) + np.nanmax(z) + ball_radius
    return x_ball, y_ball, z_ball

# Physics-based simulation
def simulate_motion():
    positions.clear()
    r_pos = 0.0001  # initial perturbation
    velocity = 0

    for _ in range(1000):
        slope = dome_slope(r_pos)
        acceleration = g * slope
        velocity += acceleration * time_step
        r_pos += velocity * time_step

        if r_pos >= 0.65:
            break

        positions.append(r_pos)

# Animation update function
def update(num):
    r_pos = positions[num]
    z_pos = np.nanmax(z) - dome_function(r_pos)

    phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x_ball = ball_radius * np.cos(phi) * np.sin(theta) + r_pos
    y_ball = ball_radius * np.sin(phi) * np.sin(theta)
    z_ball = ball_radius * np.cos(theta) + z_pos + ball_radius

    global ball_surface
    ball_surface.remove()
    ball_surface = ax.plot_surface(x_ball, y_ball, z_ball, color='red')

    if num == len(positions) - 1:
        reset_ball()

# Reset ball position
def reset_ball():
    global ball_surface
    ball_surface.remove()
    x_ball, y_ball, z_ball = initial_ball()
    ball_surface = ax.plot_surface(x_ball, y_ball, z_ball, color='red')

# Trigger physics simulation and animation
def animate(event):
    global ani
    simulate_motion()
    ani = animation.FuncAnimation(fig, update, frames=len(positions), interval=20, repeat=False)

# Initial ball setup
x_ball, y_ball, z_ball = initial_ball()
ball_surface = ax.plot_surface(x_ball, y_ball, z_ball, color='red')

# Button to trigger animation
ax_button = plt.axes([0.7, 0.02, 0.2, 0.05])
button = Button(ax_button, 'Add Perturbation')
button.on_clicked(animate)

# Set plot attributes
ax.set_title('3D Norton Dome with Real Physics-based Ball Roll', fontsize=15)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_box_aspect([1,1,0.5])

plt.show()