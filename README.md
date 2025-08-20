# Sistem Pakar Rekomendasi Tanaman 🌱

Sistem pakar berbasis Decision Tree untuk merekomendasikan tanaman yang cocok berdasarkan kondisi tanah, pH, kelembaban, dan suhu.

## 📋 Deskripsi

Sistem ini menggunakan algoritma Decision Tree Classifier untuk menganalisis kondisi lahan dan memberikan rekomendasi tanaman yang paling sesuai. Sistem dapat merekomendasikan lebih dari 40 jenis tanaman dengan tingkat confidence dan informasi detail tentang setiap tanaman.

## ✨ Fitur

- **Analisis Kondisi Lahan**: Input parameter tanah, pH, kelembaban, dan suhu
- **Rekomendasi Cerdas**: 6 rekomendasi tanaman teratas dengan tingkat confidence
- **Informasi Detail**: Waktu tanam dan tips budidaya untuk setiap tanaman
- **Web Interface**: Antarmuka web yang user-friendly
- **Data Augmentation**: Sistem otomatis memperkaya data untuk akurasi yang lebih baik

## 🚀 Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn (Decision Tree Classifier)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript
- **Data Format**: CSV

## 📦 Instalasi

1. **Clone repository**
```bash
git clone https://github.com/username/sistem-pakar-rekomendasi-tanaman.git
cd sistem-pakar-rekomendasi-tanaman
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Pastikan file data tersedia**
```
plant_data_cleaned.csv
```

4. **Jalankan aplikasi**
```bash
python app.py
```

5. **Akses aplikasi**
```
http://localhost:5000
```

## 📁 Struktur Project

```
sistem-pakar-rekomendasi-tanaman/
│
├── app.py                      # Main Flask application
├── plant_data_cleaned.csv      # Dataset tanaman
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Frontend template
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── README.md                   # Documentation
```

## 🛠️ Dependencies

```txt
Flask==2.3.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
```

## 📊 Dataset

Dataset mencakup informasi tentang:
- **Jenis Tanah**: lempung, pasir, liat, humus, gambut, dll
- **Kategori pH**: asam (<6.0), netral (6.0-7.5), basa (>7.5)
- **Kelembaban**: rendah (<40%), sedang (40-70%), tinggi (>70%)
- **Suhu**: sejuk (<20°C), hangat (≥20°C)

## 🌿 Tanaman yang Didukung

Sistem dapat merekomendasikan 40+ jenis tanaman, termasuk:

**Tanaman Pangan**: Padi, Jagung, Kedelai, Kentang, Ubi Jalar, Singkong

**Sayuran**: Bayam, Kangkung, Selada, Brokoli, Kubis, Wortel, Tomat, Cabai

**Buah-buahan**: Nanas, Pepaya, Mangga, Strawberry, Blueberry

**Tanaman Komersial**: Kelapa Sawit, Kopi, Teh, Karet, Tebu

**Herba & Bumbu**: Jahe, Bawang Putih, Bawang Merah, Oregano, Lavender

## 🔧 Penggunaan API

### POST /recommend

**Request Body:**
```json
{
    "soil_type": "lempung",
    "ph": 6.5,
    "moisture": 60,
    "temperature": 25
}
```

**Response:**
```json
{
    "success": true,
    "recommendations": [
        {
            "name": "Padi",
            "confidence": "85.2%",
            "waktu_tanam": "3-4 bulan",
            "tips": "Butuh genangan air, cocok untuk sawah"
        }
    ],
    "input_summary": {
        "soil_type": "lempung",
        "ph": 6.5,
        "moisture": 60,
        "temperature": 25,
        "ph_category": "netral",
        "moisture_category": "sedang",
        "temperature_category": "hangat"
    }
}
```

## 🎯 Cara Kerja Sistem

1. **Input Processing**: Kategorisasi nilai pH, kelembaban, dan suhu
2. **Feature Encoding**: Konversi data kategorikal menggunakan Label Encoder
3. **Prediction**: Menggunakan Decision Tree Classifier yang telah dilatih
4. **Ranking**: Mengurutkan rekomendasi berdasarkan confidence score
5. **Output**: Menampilkan top 6 rekomendasi dengan informasi detail

## 📈 Akurasi Model

- Menggunakan train-test split dengan rasio 80:20
- Stratified sampling untuk memastikan distribusi yang seimbang
- Data augmentation untuk kelas dengan sampel sedikit
- Akurasi model dapat bervariasi tergantung dataset

## 📝 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Tim Pengembang

- **Developer**: [Veros ariferdinand]
- **Email**: [verosariferdinand987@example.com]
- **GitHub**: [@username](https://github.com/Verosariferdinand)

## 🐛 Bug Reports & Feature Requests

Silakan laporkan bug atau request fitur baru melalui [GitHub Issues](https://github.com/username/sistem-pakar-rekomendasi-tanaman/issues).

## 📚 Referensi

- Scikit-learn Documentation
- Flask Documentation
- Decision Tree Algorithm
- Plant Cultivation Guidelines

---

⭐ **Jangan lupa untuk memberikan star jika project ini bermanfaat!**
