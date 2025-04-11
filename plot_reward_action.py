import numpy as np
import matplotlib.pyplot as plt

REWARD_LOG_FILE = 'reward_log.npy'
ACTION_LOG_FILE = 'action_log.npy'

def plot_logs():
    # Load reward
    rewards = np.load(REWARD_LOG_FILE)
    print(f"Loaded {len(rewards)} rewards.")

    # Load action
    actions = np.load(ACTION_LOG_FILE)
    print(f"Loaded {len(actions)} actions.")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8))

    # Plot reward
    ax1.plot(rewards, label='Reward per Step')
    ax1.set_title("Reward vs Timestep")
    ax1.set_xlabel("Timestep")
    ax1.set_ylabel("Reward")
    ax1.grid(True)

    # Plot action
    ax2.plot(actions, 'o--', label='Action (0=decrease, 1=increase)', color='red')
    ax2.set_title("Action vs Timestep")
    ax2.set_xlabel("Timestep")
    ax2.set_ylabel("Action")
    ax2.set_yticks([0, 1])
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_logs()
