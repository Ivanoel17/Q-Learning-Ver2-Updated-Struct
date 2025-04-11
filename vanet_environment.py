import numpy as np
import random

# Constants
CBR_TARGET = 0.65
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EPSILON = 0.1  # Probability of random exploration

# Bins for discretization
POWER_BINS = [5, 15, 25, 30]
BEACON_BINS = [1, 5, 10, 20]
CBR_BINS = [0.0, 0.3, 0.6, 1.0]

# Q-table (power_bins x beacon_bins x cbr_bins x 2)
# 2 di ujung menandakan 2 aksi: 0 => decrease, 1 => increase
q_table = np.zeros((len(POWER_BINS), len(BEACON_BINS), len(CBR_BINS), 2))

def discretize(value, bins):
    """
    Mengubah nilai continuous menjadi index bin.
    Pastikan index dalam rentang valid.
    """
    idx = np.digitize(value, bins) - 1
    return max(0, min(idx, len(bins) - 1))

def calculate_reward(cbr):
    """
    Menghitung reward berdasar jarak CBR dari target (CBR_TARGET).
    Makin jauh dari target, makin negatif.
    """
    return -abs(cbr - CBR_TARGET) * 100

def select_action(state):
    """
    Menggunakan epsilon-greedy:
    - dgn probabilitas EPSILON -> random action
    - selain itu, pilih aksi yang memaksimalkan Q-value
    """
    power_idx = discretize(state[0], POWER_BINS)
    beacon_idx = discretize(state[1], BEACON_BINS)
    cbr_idx = discretize(state[2], CBR_BINS)

    if random.random() < EPSILON:
        return random.choice([0, 1])  # 0 => decrease, 1 => increase

    return np.argmax(q_table[power_idx, beacon_idx, cbr_idx])

def apply_action(state, action):
    """
    Pendekatan A (One-Step):
    state => (power, beacon, cbr)
    Aksi 0 => decrease, 1 => increase
    """
    power, beacon, cbr = state

    # update power & beacon +/-1 (bounded)
    new_power = max(5, min(30, power + (-1 if action == 0 else 1)))
    new_beacon = max(1, min(20, beacon + (-1 if action == 0 else 1)))
    
    # new_cbr = cbr (tetap)
    # di real environment, cbr akan berubah, tapi disini disederhanakan
    new_cbr = cbr

    return (new_power, new_beacon, new_cbr)

def update_q_table(state, action, reward, new_state):
    """
    One-step Q-Learning update:
    Q(s,a) := Q(s,a) + alpha * [ r + gamma * maxQ(s') - Q(s,a) ]
    """
    p_idx  = discretize(state[0], POWER_BINS)
    b_idx  = discretize(state[1], BEACON_BINS)
    c_idx  = discretize(state[2], CBR_BINS)

    p_idx2 = discretize(new_state[0], POWER_BINS)
    b_idx2 = discretize(new_state[1], BEACON_BINS)
    c_idx2 = discretize(new_state[2], CBR_BINS)

    old_q  = q_table[p_idx, b_idx, c_idx, action]
    max_q2 = np.max(q_table[p_idx2, b_idx2, c_idx2])

    q_table[p_idx, b_idx, c_idx, action] = old_q + LEARNING_RATE * (
        reward + DISCOUNT_FACTOR * max_q2 - old_q
    )
