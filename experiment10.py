import numpy as np
import matplotlib.pyplot as plt

x = np.array([[0.0], [0.0]])
P = np.array([[1000.0, 0.0], [0.0, 1000.0]])
F = np.array([[1.0, 1.0], [0.0, 1.0]])
Q = np.array([[0.1, 0.0], [0.0, 0.1]])
H = np.array([[1.0, 0.0]])
R = np.array([[5.0]]) 

noisy_measurements = [1.1, 2.8, 3.1, 4.9, 5.2, 6.8, 7.1, 8.9]
true_positions = [1, 2, 3, 4, 5, 6, 7, 8] # Assuming constant velocity of 1
estimates = []

for z_meas in noisy_measurements:
    # Predict
    x = np.dot(F, x)
    P = np.dot(F, np.dot(P, F.T)) + Q
    # Update
    y = np.array([[z_meas]]) - np.dot(H, x)
    S = np.dot(H, np.dot(P, H.T)) + R
    K = np.dot(P, np.dot(H.T, np.linalg.inv(S)))
    x = x + np.dot(K, y)
    P = P - np.dot(K, np.dot(H, P))
    
    estimates.append(x[0,0])

# Visualization
time_steps = range(1, len(noisy_measurements) + 1)
plt.figure(figsize=(8, 4))
plt.plot(time_steps, true_positions, 'g--', label='True Trajectory')
plt.plot(time_steps, noisy_measurements, 'ro-', alpha=0.5, label='Noisy Sensor Data')
plt.plot(time_steps, estimates, 'b*-', linewidth=2, label='Kalman Filter Estimate')
plt.title("1D Robot Localization: Sensors vs Kalman Filter")
plt.xlabel("Time Step")
plt.ylabel("Position")
plt.legend()
plt.grid(True)
plt.show()
