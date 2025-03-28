# SSL sertifika doğrulama sorununu çözmek için
# NOT: Bu yaklaşım SADECE GELİŞTİRME ortamı içindir!
import os

import urllib3


def disable_ssl_warnings():
    """SSL uyarılarını devre dışı bırak"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Sadece DEBUG=True ise uygula
if os.environ.get("DJANGO_DEVELOPMENT") == "true":
    disable_ssl_warnings()
