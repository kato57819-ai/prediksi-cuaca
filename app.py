import os
from flask import Flask, render_template, request
import requests
import joblib

app = Flask(__name__)

# Load Model Machine Learning
model = joblib.load('model.pkl')

# API OpenWeather
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
if API_KEY is None:
    raise RuntimeError('OPENWEATHER_API_KEY environment variable is required')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    kota = request.form['kota']

    try:

        # ==========================
        # CUACA SAAT INI
        # ==========================

        current_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={kota}&appid={API_KEY}&units=metric"
        )

        current_response = requests.get(current_url)
        current_data = current_response.json()

        if 'main' not in current_data:

            return render_template(
                'index.html',
                error=f'Data cuaca untuk {kota} tidak ditemukan'
            )

        # ==========================
        # FORECAST
        # ==========================

        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={kota}&appid={API_KEY}&units=metric"
        )

        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        # ==========================
        # DATA REALTIME
        # ==========================

        suhu = current_data['main']['temp']
        kelembapan = current_data['main']['humidity']
        angin = current_data['wind']['speed']

        deskripsi = current_data['weather'][0]['description']
        icon = current_data['weather'][0]['icon']

        # ==========================
        # PREDIKSI MACHINE LEARNING
        # ==========================

        hasil = model.predict([
            [suhu, kelembapan, angin]
        ])

        print("HASIL ML =", hasil[0])
        # ==========================
        # PREDIKSI PER JAM
        # ==========================

        forecast_jam = forecast_data['list'][:8]

        # ==========================
        # PREDIKSI 5 HARI
        # ==========================

        forecast_harian = []

        tanggal_terpakai = set()

        for item in forecast_data['list']:

            tanggal = item['dt_txt'].split(' ')[0]

            if tanggal not in tanggal_terpakai:

                forecast_harian.append({

                    'tanggal': tanggal,
                    'suhu': round(item['main']['temp']),
                    'cuaca': item['weather'][0]['main'],
                    'icon': item['weather'][0]['icon']

                })

                tanggal_terpakai.add(tanggal)

            if len(forecast_harian) == 5:
                break

        # ==========================
        # TAMPILKAN KE HALAMAN
        # ==========================
        tema = "normal"

        if hasil[0] == "Cerah":
            tema = "cerah"

        elif hasil[0] == "Berawan":
            tema = "berawan"

        elif hasil[0] == "Hujan":
            tema = "hujan"


        return render_template(

            'index.html',

            kota=kota,

            suhu=suhu,
            kelembapan=kelembapan,
            angin=angin,

            deskripsi=deskripsi,
            icon=icon,

            hasil=hasil[0],

            forecast_jam=forecast_jam,
            forecast_harian=forecast_harian,

            tema=tema

        )

    except Exception as e:

        return render_template(
            'index.html',
            error=str(e)
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)