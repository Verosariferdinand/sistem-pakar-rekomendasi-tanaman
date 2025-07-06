from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Knowledge Base - Aturan untuk Forward Chaining
class PlantExpertSystem:
    def __init__(self):
        self.knowledge_base = {
            # Format: (jenis_tanah, ph_range, kelembaban_range, suhu_range): [tanaman1, tanaman2, ...]
            ('lempung', 'netral', 'sedang', 'hangat'): ['Padi', 'Jagung', 'Kedelai', 'Bayam'],
            ('lempung', 'netral', 'tinggi', 'hangat'): ['Padi', 'Kangkung', 'Selada Air'],
            ('lempung', 'asam', 'tinggi', 'hangat'): ['Ubi Jalar', 'Singkong', 'Jahe'],
            ('lempung', 'basa', 'sedang', 'hangat'): ['Brokoli', 'Kembang Kol', 'Kubis'],
            
            ('pasir', 'netral', 'rendah', 'hangat'): ['Wortel', 'Lobak', 'Kacang Tanah'],
            ('pasir', 'netral', 'sedang', 'hangat'): ['Tomat', 'Cabai', 'Terong'],
            ('pasir', 'asam', 'rendah', 'hangat'): ['Nanas', 'Pepaya', 'Mangga'],
            ('pasir', 'basa', 'sedang', 'hangat'): ['Asparagus', 'Bit', 'Turnip'],
            
            ('gambut', 'asam', 'tinggi', 'hangat'): ['Kelapa Sawit', 'Nanas', 'Kopi'],
            ('gambut', 'asam', 'tinggi', 'sejuk'): ['Teh', 'Kentang', 'Strawberry'],
            ('gambut', 'netral', 'tinggi', 'hangat'): ['Padi Rawa', 'Kangkung', 'Eceng Gondok'],
            
            ('humus', 'netral', 'sedang', 'hangat'): ['Tomat', 'Cabai', 'Terong', 'Mentimun'],
            ('humus', 'netral', 'tinggi', 'hangat'): ['Selada', 'Bayam', 'Kangkung', 'Sawi'],
            ('humus', 'asam', 'sedang', 'sejuk'): ['Strawberry', 'Blueberry', 'Raspberry'],
            ('humus', 'basa', 'sedang', 'hangat'): ['Brokoli', 'Kembang Kol', 'Kubis', 'Wortel'],
            
            ('liat', 'netral', 'tinggi', 'hangat'): ['Padi', 'Tebu', 'Jagung'],
            ('liat', 'asam', 'tinggi', 'hangat'): ['Kelapa', 'Kelapa Sawit', 'Karet'],
            ('liat', 'basa', 'sedang', 'hangat'): ['Gandum', 'Barley', 'Oat'],
            
            ('kapur', 'basa', 'rendah', 'hangat'): ['Lavender', 'Rosemary', 'Thyme'],
            ('kapur', 'basa', 'sedang', 'hangat'): ['Bawang Putih', 'Bawang Merah', 'Oregano'],
            ('kapur', 'netral', 'sedang', 'hangat'): ['Kacang Polong', 'Kacang Hijau', 'Buncis']
        }
        
        self.plant_details = {
            'Padi': {'waktu_tanam': '3-4 bulan', 'tips': 'Butuh genangan air, cocok untuk sawah'},
            'Jagung': {'waktu_tanam': '3-4 bulan', 'tips': 'Butuh sinar matahari penuh, drainase baik'},
            'Kedelai': {'waktu_tanam': '2-3 bulan', 'tips': 'Rotasi tanaman yang baik, fiksasi nitrogen'},
            'Bayam': {'waktu_tanam': '30-40 hari', 'tips': 'Tumbuh cepat, bisa dipanen berkali-kali'},
            'Kangkung': {'waktu_tanam': '25-30 hari', 'tips': 'Suka air, tumbuh sangat cepat'},
            'Selada Air': {'waktu_tanam': '20-30 hari', 'tips': 'Butuh air mengalir, sayuran hijau segar'},
            'Ubi Jalar': {'waktu_tanam': '3-4 bulan', 'tips': 'Tahan kekeringan, kaya vitamin A'},
            'Singkong': {'waktu_tanam': '6-10 bulan', 'tips': 'Sangat tahan kekeringan, mudah dibudidayakan'},
            'Jahe': {'waktu_tanam': '8-10 bulan', 'tips': 'Butuh naungan, tanaman rimpang bernilai tinggi'},
            'Brokoli': {'waktu_tanam': '2-3 bulan', 'tips': 'Butuh iklim sejuk, kaya nutrisi'},
            'Kembang Kol': {'waktu_tanam': '2-3 bulan', 'tips': 'Butuh iklim sejuk, perlu penyiraman teratur'},
            'Kubis': {'waktu_tanam': '2-3 bulan', 'tips': 'Tahan dingin, butuh pupuk organik'},
            'Wortel': {'waktu_tanam': '2-3 bulan', 'tips': 'Butuh tanah gembur, kaya beta karoten'},
            'Lobak': {'waktu_tanam': '1-2 bulan', 'tips': 'Tumbuh cepat, bagus untuk tanah berpasir'},
            'Kacang Tanah': {'waktu_tanam': '3-4 bulan', 'tips': 'Fiksasi nitrogen, butuh kalsium'},
            'Tomat': {'waktu_tanam': '3-4 bulan', 'tips': 'Butuh penyangga, penyiraman teratur'},
            'Cabai': {'waktu_tanam': '3-5 bulan', 'tips': 'Butuh sinar matahari penuh, bernilai ekonomi tinggi'},
            'Terong': {'waktu_tanam': '3-4 bulan', 'tips': 'Tahan panas, butuh pupuk organik'},
            'Nanas': {'waktu_tanam': '12-18 bulan', 'tips': 'Tanaman tropis, butuh drainase baik'},
            'Pepaya': {'waktu_tanam': '6-12 bulan', 'tips': 'Cepat berbuah, butuh sinar matahari'},
            'Mangga': {'waktu_tanam': '3-5 tahun', 'tips': 'Investasi jangka panjang, buah bernilai tinggi'},
            'Asparagus': {'waktu_tanam': '2-3 tahun', 'tips': 'Tanaman tahunan, bernilai ekonomi tinggi'},
            'Bit': {'waktu_tanam': '2-3 bulan', 'tips': 'Kaya antioksidan, daun juga bisa dimakan'},
            'Turnip': {'waktu_tanam': '1-2 bulan', 'tips': 'Tumbuh cepat, bagus untuk rotasi tanaman'},
            'Kelapa Sawit': {'waktu_tanam': '3-4 tahun', 'tips': 'Tanaman komersial, butuh lahan luas'},
            'Kopi': {'waktu_tanam': '3-4 tahun', 'tips': 'Butuh naungan, komoditas ekspor'},
            'Teh': {'waktu_tanam': '3-4 tahun', 'tips': 'Butuh iklim sejuk, ketinggian ideal'},
            'Kentang': {'waktu_tanam': '3-4 bulan', 'tips': 'Butuh iklim sejuk, tanaman umbi'},
            'Strawberry': {'waktu_tanam': '3-4 bulan', 'tips': 'Butuh iklim sejuk, buah bernilai tinggi'},
            'Padi Rawa': {'waktu_tanam': '4-5 bulan', 'tips': 'Adaptasi khusus untuk lahan rawa'},
            'Eceng Gondok': {'waktu_tanam': '1-2 bulan', 'tips': 'Tanaman air, bisa untuk kerajinan'},
            'Mentimun': {'waktu_tanam': '2-3 bulan', 'tips': 'Butuh penyangga, kandungan air tinggi'},
            'Selada': {'waktu_tanam': '1-2 bulan', 'tips': 'Sayuran sejuk, butuh penyiraman teratur'},
            'Sawi': {'waktu_tanam': '30-40 hari', 'tips': 'Tumbuh cepat, mudah dibudidayakan'},
            'Blueberry': {'waktu_tanam': '2-3 tahun', 'tips': 'Butuh tanah asam, buah super food'},
            'Raspberry': {'waktu_tanam': '1-2 tahun', 'tips': 'Tanaman semak, buah bernilai tinggi'},
            'Tebu': {'waktu_tanam': '12-18 bulan', 'tips': 'Tanaman komersial, butuh air banyak'},
            'Kelapa': {'waktu_tanam': '5-7 tahun', 'tips': 'Tanaman serbaguna, tahan angin'},
            'Karet': {'waktu_tanam': '5-7 tahun', 'tips': 'Tanaman industri, penghasil lateks'},
            'Gandum': {'waktu_tanam': '4-6 bulan', 'tips': 'Tanaman sereal, butuh iklim sejuk'},
            'Barley': {'waktu_tanam': '3-4 bulan', 'tips': 'Tanaman sereal, tahan kekeringan'},
            'Oat': {'waktu_tanam': '3-4 bulan', 'tips': 'Tanaman sereal bergizi tinggi'},
            'Lavender': {'waktu_tanam': '1-2 tahun', 'tips': 'Tanaman aromatik, tahan kekeringan'},
            'Rosemary': {'waktu_tanam': '1-2 tahun', 'tips': 'Herba aromatik, tahan kekeringan'},
            'Thyme': {'waktu_tanam': '3-4 bulan', 'tips': 'Herba kuliner, mudah dirawat'},
            'Bawang Putih': {'waktu_tanam': '4-6 bulan', 'tips': 'Bumbu dapur, bernilai ekonomi'},
            'Bawang Merah': {'waktu_tanam': '2-3 bulan', 'tips': 'Bumbu dapur, mudah dibudidayakan'},
            'Oregano': {'waktu_tanam': '2-3 bulan', 'tips': 'Herba kuliner, tahan kekeringan'},
            'Kacang Polong': {'waktu_tanam': '2-3 bulan', 'tips': 'Fiksasi nitrogen, sayuran bergizi'},
            'Kacang Hijau': {'waktu_tanam': '2-3 bulan', 'tips': 'Rotasi tanaman baik, protein tinggi'},
            'Buncis': {'waktu_tanam': '2-3 bulan', 'tips': 'Sayuran segar, butuh penyangga'}
        }
    
    def categorize_ph(self, ph_value):
        if ph_value < 6.0:
            return 'asam'
        elif ph_value > 7.5:
            return 'basa'
        else:
            return 'netral'
    
    def categorize_moisture(self, moisture_value):
        if moisture_value < 40:
            return 'rendah'
        elif moisture_value > 70:
            return 'tinggi'
        else:
            return 'sedang'
    
    def categorize_temperature(self, temp_value):
        if temp_value < 20:
            return 'sejuk'
        else:
            return 'hangat'
    
    def forward_chaining(self, soil_type, ph, moisture, temperature):
        # Kategorikan input
        ph_category = self.categorize_ph(ph)
        moisture_category = self.categorize_moisture(moisture)
        temp_category = self.categorize_temperature(temperature)
        
        # Cari aturan yang tepat
        key = (soil_type.lower(), ph_category, moisture_category, temp_category)
        
        if key in self.knowledge_base:
            plants = self.knowledge_base[key]
            recommendations = []
            
            for plant in plants:
                if plant in self.plant_details:
                    recommendations.append({
                        'name': plant,
                        'waktu_tanam': self.plant_details[plant]['waktu_tanam'],
                        'tips': self.plant_details[plant]['tips']
                    })
            
            return recommendations
        
        # Jika tidak ada aturan yang tepat, cari yang paling mirip
        return self.find_similar_recommendations(soil_type, ph_category, moisture_category, temp_category)
    
    def find_similar_recommendations(self, soil_type, ph_cat, moisture_cat, temp_cat):
        # Cari rekomendasi dengan kriteria yang paling mirip
        similar_plants = []
        
        for key, plants in self.knowledge_base.items():
            match_score = 0
            if key[0] == soil_type.lower():
                match_score += 3
            if key[1] == ph_cat:
                match_score += 2
            if key[2] == moisture_cat:
                match_score += 1
            if key[3] == temp_cat:
                match_score += 1
            
            if match_score >= 3:  # Minimal cocok tanah + 1 kriteria lain
                for plant in plants:
                    if plant in self.plant_details:
                        similar_plants.append({
                            'name': plant,
                            'waktu_tanam': self.plant_details[plant]['waktu_tanam'],
                            'tips': self.plant_details[plant]['tips'],
                            'match_score': match_score
                        })
        
        # Urutkan berdasarkan skor kecocokan
        similar_plants.sort(key=lambda x: x['match_score'], reverse=True)
        return similar_plants[:6]  # Ambil 6 rekomendasi teratas

# Inisialisasi sistem pakar
expert_system = PlantExpertSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        soil_type = data.get('soil_type')
        ph = float(data.get('ph'))
        moisture = float(data.get('moisture'))
        temperature = float(data.get('temperature'))
        
        recommendations = expert_system.forward_chaining(soil_type, ph, moisture, temperature)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'input_summary': {
                'soil_type': soil_type,
                'ph': ph,
                'moisture': moisture,
                'temperature': temperature,
                'ph_category': expert_system.categorize_ph(ph),
                'moisture_category': expert_system.categorize_moisture(moisture),
                'temperature_category': expert_system.categorize_temperature(temperature)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Buat folder templates jika belum ada
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)