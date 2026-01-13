sequenceDiagram
    participant User as 👤 Kullanıcı
    participant Frontend as 🌐 Frontend (Nginx:8090)
    participant API as ⚙️ Backend API (Flask:8000)
    participant DB as 🗄️ PostgreSQL DB
    participant Swagger as 📋 Swagger UI

    Note over User,DB: Kullanıcı Kayıt ve Giriş Akışı
    
    User->>Frontend: Tarayıcıdan Uygulama Aç
    Frontend->>User: Login/Register Ekranı Göster
    
    User->>Frontend: Kayıt Ol (username, password)
    Frontend->>API: POST /api/auth/register
    API->>DB: Yeni kullanıcı oluştur
    DB-->>API: Kullanıcı kaydedildi
    API-->>Frontend: {success: true, message: "Kayıt başarılı"}
    Frontend-->>User: "Kayıt başarılı" mesajı
    
    User->>Frontend: Giriş Yap (username, password)
    Frontend->>API: POST /api/auth/login
    API->>DB: Kullanıcı doğrula
    DB-->>API: Kullanıcı bilgileri
    API->>API: JWT Token oluştur
    API-->>Frontend: {success: true, token: "...", level: "A1"}
    Frontend->>Frontend: Token'ı localStorage'a kaydet
    Frontend-->>User: Ana Dashboard'a yönlendir
    
    Note over User,DB: Kelime Öğrenme Akışı
    
    User->>Frontend: Vocabulary sayfasına git
    Frontend->>API: GET /api/words (Bearer Token)
    API->>DB: Kelimeleri getir
    DB-->>API: Kelime listesi
    API-->>Frontend: {success: true, words: [...]}
    Frontend-->>User: Kelimeler kartlar halinde gösterilir
    
    Note over User,Swagger: Swagger Dokümantasyonu
    
    User->>Swagger: /apidocs adresine git
    Swagger-->>User: Tüm API endpoint'lerini göster
    User->>Swagger: Endpoint test et (Try it out)
    Swagger->>API: API isteği gönder
    API-->>Swagger: Yanıt döner
    Swagger-->>User: Sonucu görüntüle