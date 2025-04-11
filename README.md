# Real-time Q-Learning untuk Optimasi VANET (Pendekatan A)

Repository ini berisi implementasi algoritma **Q-Learning real-time** untuk optimasi parameter VANET (Vehicular Ad-Hoc Networks), khususnya:

- **Beacon Rate**
- **Transmission Power**

dengan tujuan menjaga **Channel Busy Ratio (CBR)** pada target tertentu (default: `0.65`).

## 📁 Struktur Folder

```
Q-Learning opt A/
├── inference_server.py      # Server komunikasi real-time dengan MATLAB
├── vanet_environment.py     # Logika Q-learning (Q-table, aksi, reward, dll.)
├── q_table.npy              # Model Q-table (tersimpan otomatis)
├── reward_log.npy           # Log reward per timestep (tersimpan otomatis)
└── action_log.npy           # Log aksi per timestep (tersimpan otomatis)
```

## 🚀 Cara Menjalankan

### 1. Install dependensi

```bash
pip install numpy
```

### 2. Jalankan server Python

```bash
python inference_server.py
```

Server akan aktif di `localhost:5000`.

---

### 3. Kirim data dari MATLAB (contoh sederhana)

```matlab
rlData = struct( ...
    'vehID', 'veh0', ...
    'transmissionPower', 10, ...
    'beaconRate', 5, ...
    'CBR', 0.05 ...
);

jsonData = jsonencode(rlData);
t = tcpip('127.0.0.1', 5000, 'NetworkRole', 'client');
fopen(t);
fprintf(t, jsonData);
response = fscanf(t, '%s');
disp(response);
fclose(t);
```

MATLAB akan menerima balasan berisi:
- `power`, `beacon` yang dioptimasi
- `reward`, `action` yang dipilih oleh agen

---

### 4. Menghentikan server

Tekan `Ctrl + C` pada terminal. Maka otomatis akan tersimpan:
- Q-table ke `q_table.npy`
- Log reward ke `reward_log.npy`
- Log aksi ke `action_log.npy`

---

## 📈 Plot Reward & Aksi (Offline)

Buat file `plot_reward_action.py`:

```python
import numpy as np
import matplotlib.pyplot as plt

rewards = np.load('reward_log.npy')
actions = np.load('action_log.npy')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,8))

ax1.plot(rewards, label='Reward per Step')
ax1.set_title('Reward vs Timestep')
ax1.set_xlabel('Timestep')
ax1.set_ylabel('Reward')
ax1.grid(True)

ax2.plot(actions, 'o--', color='red', label='Action (0=decrease, 1=increase)')
ax2.set_title('Action vs Timestep')
ax2.set_xlabel('Timestep')
ax2.set_ylabel('Action')
ax2.set_yticks([0, 1])
ax2.grid(True)

plt.tight_layout()
plt.show()
```

Lalu jalankan:

```bash
python plot_reward_action.py
```

---

## ⚙️ Edit Parameter Q-Learning

Semua parameter bisa diubah di file `vanet_environment.py`:

```python
CBR_TARGET = 0.65
EPSILON = 0.1
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
```

---

## 🧠 Catatan Penting

- Server ini hanya mengatur aksi Q-Learning. Perubahan **CBR tergantung simulasi di MATLAB**.
- Agar agent bisa belajar, pastikan MATLAB menghitung ulang CBR berdasarkan parameter (`power`, `beacon`) yang dikembalikan oleh Python.
