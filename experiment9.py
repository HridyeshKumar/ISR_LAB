import numpy as np
import matplotlib.pyplot as plt

state = np.array([0.0, 10.0]) # Robot at 0, Landmark truly at 10
cov = np.array([[0.0, 0.0], 
                [0.0, 100.0]]) # Landmark highly uncertain

robot_history = []
landmark_history = []
landmark_variance = []

for step in range(10):
    # Predict (Robot moves forward by 1 unit)
    u, u_noise = 1.0, 0.1
    state[0] += u
    cov[0, 0] += u_noise
    
    # Simulate a measurement of the landmark
    true_dist = 10.0 - state[0]
    z = true_dist + np.random.normal(0, 0.5) 
    
    # Update (Observe Landmark)
    expected_z = state[1] - state[0]
    y = z - expected_z
    H = np.array([-1.0, 1.0])
    R = 1.0 
    
    S = H.dot(cov).dot(H.T) + R
    K = cov.dot(H.T) / S
    
    state = state + K * y
    cov = cov - np.outer(K, H.dot(cov))
    
    robot_history.append(state[0])
    landmark_history.append(state[1])
    landmark_variance.append(cov[1, 1])

# Visualization
steps = range(1, 11)
plt.figure(figsize=(8, 5))
plt.plot(steps, robot_history, 'bo-', label="Robot Position")
plt.plot(steps, landmark_history, 'r^-', label="Estimated Landmark Position")

# Plot uncertainty bounds for the landmark
std_dev = np.sqrt(landmark_variance)
upper_bound = np.array(landmark_history) + std_dev
lower_bound = np.array(landmark_history) - std_dev
plt.fill_between(steps, lower_bound, upper_bound, color='red', alpha=0.2, label='Landmark Uncertainty (±1 Std Dev)')

plt.axhline(10.0, color='k', linestyle='--', label='True Landmark Position')
plt.title("1D EKF SLAM: Mapping a Landmark")
plt.xlabel("Time Step")
plt.ylabel("Position Map")
plt.legend()
plt.grid(True)
plt.show()
