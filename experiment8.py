import numpy as np
import random
import matplotlib.pyplot as plt

n_states = 6
n_actions = 2 # 0: Left, 1: Right
q_table = np.zeros((n_states, n_actions))
alpha, gamma, epsilon = 0.1, 0.9, 0.1

# Training
for episode in range(300):
    state = 0
    while state != 5:
        action = random.choice([0, 1]) if random.uniform(0, 1) < epsilon else np.argmax(q_table[state])
        next_state = max(0, min(5, state - 1 if action == 0 else state + 1))
        reward = 10 if next_state == 5 else -1
        
        q_table[state, action] = q_table[state, action] + alpha * \
            (reward + gamma * np.max(q_table[next_state]) - q_table[state, action])
        state = next_state

# Visualization
fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.matshow(q_table, cmap='YlGn')
fig.colorbar(cax, label='Q-Value')

for (i, j), val in np.ndenumerate(q_table):
    ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')

ax.set_xticks([0, 1])
ax.set_xticklabels(['Left', 'Right'])
ax.set_yticks(range(6))
ax.set_yticklabels([f'State {i}' for i in range(6)])
plt.title("Q-Learning: State-Action Value Heatmap")
plt.xlabel("Action")
plt.ylabel("Grid State")
plt.show()
