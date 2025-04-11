import socket
import json
import numpy as np
import os
from vanet_environment import (
    select_action,
    apply_action,
    calculate_reward,
    update_q_table,
    q_table
)

HOST = '127.0.0.1'
PORT = 5000
MODEL_FILE = 'q_table.npy'
REWARD_LOG_FILE = 'reward_log.npy'
ACTION_LOG_FILE = 'action_log.npy'

class RLServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(1)
        print(f"Server listening on {HOST}:{PORT}")

        self.load_model()
        
        self.rewards_per_step = []
        self.actions_per_step = []

    def load_model(self):
        if os.path.exists(MODEL_FILE):
            print(f"Loading model from {MODEL_FILE}...")
            loaded_q = np.load(MODEL_FILE)
            np.copyto(q_table, loaded_q)
        else:
            print("No model found. Starting with fresh Q-table.")

    def save_model(self):
        print(f"Saving model to {MODEL_FILE}...")
        np.save(MODEL_FILE, q_table)

    def save_logs(self):
        if len(self.rewards_per_step) > 0:
            print(f"Saving rewards to {REWARD_LOG_FILE} ...")
            np.save(REWARD_LOG_FILE, np.array(self.rewards_per_step))
        if len(self.actions_per_step) > 0:
            print(f"Saving actions to {ACTION_LOG_FILE} ...")
            np.save(ACTION_LOG_FILE, np.array(self.actions_per_step))

    def handle_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break

            try:
                rl_data = json.loads(data.decode())
                current_power = rl_data['transmissionPower']
                current_beacon = rl_data['beaconRate']
                current_cbr = rl_data['CBR']

                state = (current_power, current_beacon, current_cbr)

                action = select_action(state)
                print(f"Action selected: {action} (0=decrease, 1=increase) for state={state}")

                new_state = apply_action(state, action)
                reward = calculate_reward(current_cbr)

                self.rewards_per_step.append(reward)
                self.actions_per_step.append(action)

                update_q_table(state, action, reward, new_state)

                # Pastikan konversi ke python int/float
                response = {
                    'power': new_state[0],
                    'beacon': new_state[1],
                    'reward': float(reward),  # konversi ke float
                    'action': int(action)     # konversi ke int
                }

                conn.send(json.dumps(response).encode())

            except Exception as e:
                print(f"Error: {e}")
                break

    def start(self):
        try:
            while True:
                conn, addr = self.server.accept()
                print(f"Connected to: {addr}")
                self.handle_client(conn)
                conn.close()
        except KeyboardInterrupt:
            print("Server stopping. Saving model & logs...")
            self.save_model()
            self.save_logs()

if __name__ == "__main__":
    server = RLServer()
    server.start()
