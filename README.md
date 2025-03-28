# Django Keycloak Entegrasyonu

Bu proje, Django web uygulamalarında Keycloak ile kimlik doğrulama ve yetkilendirme entegrasyonu için bir referans uygulamadır. Keycloak üzerinden Single Sign-On (SSO) ve rol tabanlı erişim kontrolü (RBAC) sağlar.

## 📋 Özellikler

- **Keycloak ile SSO**: OpenID Connect protokolü üzerinden güvenli kimlik doğrulama
- **Rol Tabanlı Erişim Kontrolü**: Keycloak'tan gelen rollerle Django gruplarını senkronize etme
- **Özel Decorator**: View seviyesinde rol kontrolü için `@roles_required` decorator
- **Şablonlarda Rol Kontrolü**: UI içeriğini rollere göre kontrol eden `{% has_role %}` template etiketi
- **Güvenli Çıkış**: Hem Django hem Keycloak oturumlarını sonlandırma
- **Özelleştirilmiş Hata Sayfaları**: Kullanıcı dostu 403, 404, 500 hata sayfaları

## 🔧 Gereksinimler

- Python 3.8+
- Django 5.x
- Keycloak 21.x+
- Firefox, Chrome, Edge gibi modern bir web tarayıcı

## 💻 Kurulum

### 1. Python Ortamını Hazırlama

```bash
# Sanal ortam oluştur
python -m venv vdjango

# Sanal ortamı aktifleştir
# Windows için:
vdjango\Scripts\activate

# Linux/Mac için:
source vdjango/bin/activate

# Gerekli paketleri yükle
pip install -r requirements.txt
```

### 2. Keycloak Yapılandırması

1. **Keycloak Sunucusu Kurulumu**:
   - [Keycloak'ı indirin ve kurun](https://www.keycloak.org/getting-started)
   - Yönetici hesabı oluşturun ve yönetici konsoluna giriş yapın

2. **Realm Oluşturma**:
   - Yeni bir realm oluşturun (örn. "sivasbeltr")
   - Realm ayarlarında Token Lifetime değerlerini uygulamanıza göre yapılandırın

3. **İstemci (Client) Ayarları**:
   - Yeni bir istemci oluşturun (örn. "envanter")
   - Access Type: "confidential" olarak ayarlayın
   - Valid Redirect URIs: "http://localhost:8000/*" ekleyin
   - Web Origins: "+" ekleyin (CORS desteği için)
   - İstemci Secrets sekmesinden gizli anahtarı alın

4. **Roller ve Kullanıcılar**:
   - Realm Roles üzerinden roller oluşturun: admin, user, manager
   - Test için kullanıcılar ekleyin ve rolleri atayın

### 3. Django Projesi Yapılandırması

1. **.env Dosyası Oluşturma**:
   Proje kök dizininde `.env` dosyası oluşturun ve şu değişkenleri ekleyin:

   ```
   OIDC_RP_CLIENT_ID=envanter
   OIDC_RP_CLIENT_SECRET=<keycloak_client_secret>
   OIDC_OP_AUTHORIZATION_ENDPOINT=https://<keycloak_url>/realms/<realmname>/protocol/openid-connect/auth
   OIDC_OP_TOKEN_ENDPOINT=https://<keycloak_url>/realms/<realmname>/protocol/openid-connect/token
   OIDC_OP_USER_ENDPOINT=https://<keycloak_url>/realms/<realmname>/protocol/openid-connect/userinfo
   OIDC_OP_JWKS_ENDPOINT=https://<keycloak_url>/realms/<realmname>/protocol/openid-connect/certs
   OIDC_OP_LOGOUT_ENDPOINT=https://<keycloak_url>/realms/<realmname>/protocol/openid-connect/logout
   OIDC_RP_POST_LOGOUT_REDIRECT_URI=http://localhost:8000/
   ```

2. **Veritabanı Migrasyonları**:
   ```bash
   python manage.py migrate
   ```

## 🚀 Çalıştırma

```bash
# Geliştirme sunucusunu başlat
python manage.py runserver

# Tarayıcıda aç
# http://localhost:8000
```

## 🔐 Rol Tabanlı Erişim Kontrolü

### View Seviyesinde Rol Kontrolü

`@roles_required` decorator'ı kullanarak belirli rollere sahip kullanıcılara erişim sağlayabilirsiniz:

```python
from ornekapp.decorators import roles_required

@login_required
@roles_required("admin", "manager")
def my_protected_view(request):
    # Bu view'a sadece admin veya manager rolüne sahip kullanıcılar erişebilir
    return render(request, "my_template.html")
```

### Şablonlarda Rol Kontrolü

Şablonlarda `has_role` etiketi ile rol bazlı içerik gösterebilirsiniz:

```html
{% load role_tags %}

{% has_role 'admin' %}
    <p>Bu içerik sadece admin kullanıcılarına görünür</p>
{% end %}

{% has_role 'admin' 'manager' %}
    <p>Bu içerik hem admin hem de manager rolüne sahip kullanıcılara görünür</p>
{% end %}
```

## 🚨 Güvenlik Notları

- Bu proje varsayılan olarak SSL doğrulamasını devre dışı bırakır ve geliştirme ortamı için tasarlanmıştır
- Üretim ortamında SSL doğrulamasını aktifleştirin ve güvenli bağlantı kullanın
- Keycloak'tan gelen "roles" veya "realm_access.roles" alanı üzerinden roller çözümlenir
- Hassas bilgileri daima `.env` dosyasında saklayın ve versiyon kontrolüne eklemekten kaçının

## 📄 Notlar

### Çıkış İşlemi
Uygulama, hem Django'dan hem de Keycloak'tan güvenli çıkış sağlar. Bu sayede SSO oturumu tamamen sonlandırılır.

### Hata Sayfaları
Erişim izni olmayan kullanıcılara bilgilendirici bir 403 hata sayfası gösterilir.

## 🤝 Katkıda Bulunma

Hata raporları, özellik istekleri ve pull request'ler için GitHub üzerinden iletişime geçebilirsiniz.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.
