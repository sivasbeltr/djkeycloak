import urllib.parse

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .decorators import roles_required


def index(request):
    """Ana sayfa görünümü"""
    return render(request, "ornekapp/index.html")


def login(request):
    """Giriş sayfası görünümü"""
    return render(request, "ornekapp/login.html")


@login_required
def profile(request):
    """Kullanıcı profili görünümü"""
    user = request.user
    roles = user.groups.values_list("name", flat=True)

    context = {
        "user": user,
        "roles": roles,
    }
    return render(request, "ornekapp/profile.html", context)


def logout_view(request):
    """Hem Django hem de Keycloak'tan çıkış yap"""
    # İlk olarak ID token'ı kaydedin (redirect'ten önce)
    id_token = request.session.get("oidc_id_token", "")

    # Django'dan çıkış yap
    logout(request)

    # Keycloak'tan da çıkış yap
    if (
        hasattr(settings, "OIDC_OP_LOGOUT_ENDPOINT")
        and settings.OIDC_OP_LOGOUT_ENDPOINT
    ):
        # Yönlendirme URL'ini oluştur
        redirect_url = (
            settings.OIDC_RP_POST_LOGOUT_REDIRECT_URI or request.build_absolute_uri("/")
        )

        # Logout isteği için parametreleri hazırla
        params = {
            "id_token_hint": id_token,
            "post_logout_redirect_uri": redirect_url,
        }

        # İstemci ID'si (opsiyonel ama Keycloak'ta yararlı olabilir)
        if hasattr(settings, "OIDC_RP_CLIENT_ID") and settings.OIDC_RP_CLIENT_ID:
            params["client_id"] = settings.OIDC_RP_CLIENT_ID

        # Parametreleri URL'e ekle
        query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v})
        logout_url = f"{settings.OIDC_OP_LOGOUT_ENDPOINT}?{query_string}"

        print(f"Redirecting to Keycloak logout URL: {logout_url}")
        return redirect(logout_url)

    # Keycloak logout endpoint'i yoksa normal redirect kullan
    return redirect("index")


@login_required
@roles_required("Mudur")
def admin_dashboard(request):
    """Sadece admin rolüne sahip kullanıcılar erişebilir"""
    return render(request, "ornekapp/admin_dashboard.html")


@login_required
@roles_required("Saha")
def user_dashboard(request):
    """Sadece user rolüne sahip kullanıcılar erişebilir"""
    return render(request, "ornekapp/user_dashboard.html")


@login_required
@roles_required("Admin", "Mudur")
def management_dashboard(request):
    """Admin veya manager rolüne sahip kullanıcılar erişebilir"""
    return render(request, "ornekapp/management_dashboard.html")


# Hata sayfaları için view'lar
def handler403(request, exception=None):
    """403 (İzin Reddedildi) hata sayfası"""
    return render(request, "403.html", status=403)


def handler404(request, exception=None):
    """404 (Sayfa Bulunamadı) hata sayfası"""
    return render(request, "404.html", status=404)


def handler500(request):
    """500 (Sunucu Hatası) hata sayfası"""
    return render(request, "500.html", status=500)
