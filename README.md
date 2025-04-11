# Q-Learning-Ver2-Updated-Struct

Real-time Q-Learning untuk Optimasi VANET (Pendekatan A)
Repository ini berisi implementasi algoritma Q-Learning real-time untuk optimasi parameter VANET (Vehicle Ad-Hoc Network), khususnya untuk parameter:

Beacon Rate (tingkat pengiriman beacon)

Transmission Power (daya transmisi)

dengan tujuan untuk menjaga nilai Channel Busy Ratio (CBR) pada target tertentu (misalnya: 0.65).

Struktur Folder
css
Copy
Edit
Q-Learning opt A/
├── inference_server.py     # Server real-time Q-learning, komunikasi dengan MATLAB
├── vanet_environment.py    # Fungsi Q-learning, Q-table, reward, dll.
├── q_table.npy             # File Q-table (akan dibuat otomatis setelah training)
├── reward_log.npy          # File log reward (dibuat otomatis setelah training)
└── action_log.npy          # File log aksi (dibuat otomatis setelah training)
Kebutuhan & Dependensi
Python ≥ 3.7

Dependensi Python (install dengan pip):

bash
Copy
Edit
pip install numpy
MATLAB (untuk simulasi real-time sebagai environment VANET)

MATLAB harus dapat mengirimkan data JSON ke server Python, dan menerima respons JSON.

Cara Penggunaan
Langkah 1: Jalankan Server Python
Masuk ke folder:

bash
Copy
Edit
cd "Q-Learning opt A"
Jalankan server:

bash
Copy
Edit
python inference_server.py
Server akan berjalan di localhost:5000 dan menunggu koneksi/data dari MATLAB.

Langkah 2: Koneksikan MATLAB ke Python
Di MATLAB, kirimkan data rlData setiap timestep berupa beacon rate, transmission power, dan nilai CBR terkini. Berikut contoh kode MATLAB sederhana:

matlab
Copy
Edit
% contoh data MATLAB
vehID = 'veh0';
currentPower = 10;
currentBeacon = 5;
currentCBR = 0.05; % contoh nilai CBR

rlData = struct( ...
    'vehID', vehID, ...
    'transmissionPower', currentPower, ...
    'beaconRate', currentBeacon, ...
    'CBR', currentCBR ...
);

jsonData = jsonencode(rlData);

% setup koneksi TCP/IP ke Python server
t = tcpip('127.0.0.1', 5000, 'NetworkRole', 'client');
fopen(t);

% kirim data
fprintf(t, jsonData);

% terima response
response = fscanf(t, '%s');
disp(response);  % beacon, power, reward, action dari Python

fclose(t);
Perhatikan:

Data response dari Python berupa power & beacon yang baru, serta reward dan aksi.

MATLAB bisa menggunakan nilai beacon & power yang baru ini untuk menjalankan simulasi di step berikutnya, lalu mengirim kembali hasil CBR baru ke Python.

Langkah 3: Menghentikan Server Python
Setelah proses simulasi selesai (atau ingin berhenti), tekan:

mathematica
Copy
Edit
Ctrl + C
Server otomatis menyimpan:

Model Q-table ke q_table.npy

Log reward ke reward_log.npy

Log aksi ke action_log.npy
