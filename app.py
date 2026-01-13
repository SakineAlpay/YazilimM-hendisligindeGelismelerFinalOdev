from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger
import os

# Veritabanı ve Modeller
from db import db
from models import User, Word

# Blueprint'ler
from resources.auth import auth_bp
from resources.content import content_bp

app = Flask(__name__)

# --- SWAGGER AYARLARI (KRİTİK KISIM) ---
# Bu ayar, Flasgger'ın otomatik olarak "swagger: 2.0" eklemesini engeller.
app.config['SWAGGER'] = {
    'title': 'İngilizce Öğrenme API',
    'uiversion': 3,
    'openapi': '3.0.0'  # <--- BU SATIR OLMADAN ÇALIŞMAZ!
}

# Template file yolunu sadece dosya adı olarak veriyoruz
swagger = Swagger(app, template_file='swagger_ingilizce_app.yaml')

# Ayarlar
app.config['SECRET_KEY'] = 'super-secret-key'
# Veritabanı ayarı (Docker/Podman için)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://learnhub:learnhub2024@postgres:5432/learnhub_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Başlatıcılar
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# Blueprint Kayıtları
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(content_bp, url_prefix='/api')

# ANA SAYFA ROTASI
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Veritabanı Başlatma
def init_db():
    with app.app_context():
        try:
            db.create_all()
            if Word.query.count() == 0:
                print("--- Veritabanı hazırlanıyor... ---")
                kelimeler = [
                    Word(word="Ebullient", meaning="Neşeli, coşkulu", level="C2", example="She sounded ebullient and happy."),
                    Word(word="Serene", meaning="Huzurlu", level="B2", example="He remained serene in the midst of chaos."),
                    Word(word="Lucid", meaning="Açık, anlaşılır", level="C1", example="His explanation was lucid.")
                ]
                db.session.add_all(kelimeler)
                db.session.commit()
                print("--- Kelimeler yüklendi! ---")
        except Exception as e:
            print(f"DB Hatası: {e}")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)