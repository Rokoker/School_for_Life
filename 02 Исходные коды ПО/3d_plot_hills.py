import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def lorenz(t, state, sigma, beta, rho):
    x, y, z = state
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return [dx_dt, dy_dt, dz_dt]

# Parameters
sigma = 10.0
beta = 8.0 / 3.0
rho = 28.0

# Initial conditions
initial_state = [1.0, 1.0, 1.0]

# Time span
t_span = [0, 25]
num_points = 10000
t_values = np.linspace(t_span[0], t_span[1], num_points)

# Solve the ODE
solution = solve_ivp(lorenz, t_span, initial_state, args=(sigma, beta, rho), t_eval=t_values)

# Extract solution
x_values = solution.y[0]
y_values = solution.y[1]
z_values = solution.y[2]

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_values, y_values, z_values)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz Attractor')

plt.show()
