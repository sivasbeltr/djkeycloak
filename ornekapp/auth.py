import requests
from django.contrib.auth.models import Group, Permission
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KeycloakRoleMixin:
    """Keycloak rollerini yönetmek için mixin"""

    def get_roles_from_claims(self, claims):
        """Token içerisindeki rollerini çıkarır"""
        # Direkt 'roles' alanından rolleri al
        roles = claims.get("roles", [])
        # Eğer boşsa, eski yapıyı da kontrol et (geriye dönük uyumluluk için)
        if not roles:
            realm_access = claims.get("realm_access", {})
            roles = realm_access.get("roles", [])
        return roles

    def update_user_roles(self, user, roles):
        """Kullanıcının rollerini günceller"""
        # Önce mevcut tüm gruplardan kullanıcıyı çıkaralım
        user.groups.clear()

        # Gelen rollere göre gruplara ekleyelim
        for role_name in roles:
            group, _ = Group.objects.get_or_create(name=role_name)
            user.groups.add(group)

        user.save()
        return user


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend, KeycloakRoleMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # SSL hatası için requests session konfigürasyonu
        self.disable_ssl_verification()

    def disable_ssl_verification(self):
        """SSL doğrulamasını devre dışı bırak (geliştirme ortamı için)"""
        session = requests.Session()
        session.verify = False
        # SSL uyarılarını gizle
        requests.packages.urllib3.disable_warnings()
        return session

    def create_user(self, claims):
        user = super().create_user(claims)
        user.username = claims.get("preferred_username", user.email)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        # Rolleri ata
        roles = self.get_roles_from_claims(claims)
        self.update_user_roles(user, roles)

        return user

    def update_user(self, user, claims):
        user = super().update_user(user, claims)

        # Kullanıcı bilgilerini güncelle
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()

        # Rolleri güncelle
        roles = self.get_roles_from_claims(claims)
        self.update_user_roles(user, roles)

        return user
