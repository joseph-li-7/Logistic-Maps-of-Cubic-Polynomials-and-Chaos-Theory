import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm

# ---------------------------
# USER INPUT FOR PARAMETERS j AND k
# ---------------------------

# Ask user for j (must be between 0 and 9, then divided by 10)
while True:
    try:
        j = float(input("Enter a value for j (0-9): "))
        if 0 <= j <= 9:
            j /= 10  # Convert to [0, 1]
            break
        else:
            print("Invalid input. Please enter a value between 0 and 9.")
    except ValueError:
        print("Invalid input. Please enter a value.")

# Ask user for k (must be between 0 and 9, then divided by 10)
while True:
    try:
        k = float(input("Enter a value for k (0-9): "))
        if 0 <= k <= 9:
            k /= 10  # Convert to [0, 1]
            break
        else:
            print("Invalid input. Please enter a value between 0 and 9.")
    except ValueError:
        print("Invalid input. Please enter a value.")

print(f"Values chosen: j = {j}, k = {k}")

# ---------------------------
# PARAMETERS AND FUNCTION SETUP
# ---------------------------

def g(x):
    return -2*x**3 + 3*(j + k)*x**2 - 6*j*k*x + 4

# Compute derivative g'(x) to find critical points to help determine max/min values
def g_derivative(x):
    return -6*x**2 + 6*(j + k)*x - 6*j*k

# Solve for critical points
def find_extrema():
    # Finds the maximum (M) and minimum (m) values of g(x) in the range [0,1]
    critical_points = np.roots([-6, 6*(j + k), -6*j*k])  # Solve g'(x) = 0
    valid_critical_points = [x for x in critical_points if 0 <= x <= 1]  # Keep only points in [0,1]
    
    # Evaluate g(x) at the endpoints (0 and 1) and critical points (Extreme Value Theorem)
    values = [g(0), g(1)] + [g(x) for x in valid_critical_points]
    
    return max(values), min(values)  # Return maximum and minimum values

# Compute M (max) and m (min)
M, m = find_extrema()

# Print the max and min values for reference
print(f"The maximum M value is {M} and the minimum m value is {m}.")

def f(x):
    return (g(x) - m) / (M - m)

# ---------------------------
# USER INPUT FOR INITIAL VALUE x_0
# ---------------------------

# Ask user for an initial value x_0 within [0,1]
while True:
    try:
        result = float(input("Enter the initial value x_0 (between 0 and 1): "))
        if 0 <= result <= 1:
            break  # Valid input, exit loop
        else:
            print("Invalid input. Please enter a number between 0 and 1.")
    except ValueError:
        print("Invalid input. Please enter a numerical value between 0 and 1.")

print(f"Initial value chosen: x_0 = {result}")

# ---------------------------
# USER INPUT FOR NUMBER OF ITERATIONS N
# ---------------------------

# Ask user for the number of iterations N (must be a positive integer)
while True:
    try:
        N = int(input("Enter the number of iterations (positive integer): "))
        if N > 0:  # Must be positive
            break  # Valid input, exit loop
        else:
            print("Invalid input. Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

print(f"Number of iterations chosen: N = {N}")

# ---------------------------
# PLOTTING FUNCTION AND COBWEB DIAGRAM, FROM LAB 9
# ---------------------------

# Create figure for visualization
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)

# Plot axes, labels, etc.
ax.plot([0, 1], [0, 1], color='black')
x_vals = np.linspace(0, 1, 100)  # Generate 100 points between 0 and 1
ax.plot(x_vals, f(x_vals), color='black')  # Plot f(x)
plt.title('Assignment 3: Chaos Experiment')
plt.xlabel('x')
plt.ylabel('y')

# ---------------------------
# ITERATION AND SEQUENCE GENERATION
# ---------------------------

x_cache = {}

def x(n):
    if n in x_cache:
        return x_cache[n]  # Return stored value if already computed
    if n == 0:
        result_val = result  # Use user-defined initial condition
    else:
        result_val = f(x(n-1))  # Compute next value in the sequence
    x_cache[n] = result_val  # Store computed value for future use
    return result_val

# ---------------------------
# PRINTING THE SEQUENCE WHILE AVOIDING UNNECESSARY REPETITION
# ---------------------------

# Dictionary to track values that have already appeared
seen_values = {}

for n in range(N):
    value = x(n)

    # Detect if a value starts repeating
    if value in seen_values:  
        print(f"The sequence enters a stable cycle, meaning the function keeps mapping between these values indefinitely:\n{value}\n{x(n+1)}")
        break  # Stop printing further values to avoid messy output
    
    seen_values[value] = n  # Mark this value as seen
    print(value)  # Print the computed sequence value

# ---------------------------
# ANIMATION (COBWEB DIAGRAM)
# ---------------------------

# Create a color gradient for visualization
cm_subsection = np.linspace(0, 1, N)
colours = [cm.jet_r(x) for x in cm_subsection]

def animation_frame(i):
    plt.plot([x(i[0]), x(i[0])], [x(i[0]), x(i[0]+1)], color=i[1])  # Vertical line
    plt.plot([x(i[0]), x(i[0]+1)], [x(i[0]+1), x(i[0]+1)], color=i[1])  # Horizontal line
    return []

animation = FuncAnimation(fig, func=animation_frame, frames=enumerate(colours), interval=100, repeat=False, cache_frame_data=False)

# ---------------------------
# DISPLAY OUTPUT
# ---------------------------

plt.show()  # Show the final plot with animation