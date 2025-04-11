# Q-Learning-Ver2-Updated-Struct

# Real-time Q-Learning untuk Optimasi VANET (Pendekatan A)

Repository ini berisi implementasi algoritma **Q-Learning real-time** untuk optimasi parameter VANET (Vehicular Ad-Hoc Networks), khususnya:

- **Beacon Rate**
- **Transmission Power**

dengan tujuan menjaga **Channel Busy Ratio (CBR)** pada target tertentu (default: `0.65`).

## 📁 Struktur Folder

Q-Learning opt A/ ├── inference_server.py 
# Server komunikasi real-time dengan MATLAB 
├── vanet_environment.py 
# Logika Q-learning (Q-table, aksi, reward, dll.) 
├── q_table.npy 
# Model Q-table (tersimpan otomatis) 
├── reward_log.npy 
# Log reward per timestep (tersimpan otomatis) 
└── action_log.npy 
# Log aksi per timestep (tersimpan otomatis)


## 🚀 Cara Menjalankan

### 1. Install dependensi

```bash
pip install numpy

### 2. Jalankan server 
python inference_server.py

