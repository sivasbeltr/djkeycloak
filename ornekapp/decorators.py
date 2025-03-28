from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def roles_required(*roles):
    """
    İstenen rollere sahip olan kullanıcıların erişimine izin veren decorator.

    Kullanım:
    @roles_required('admin', 'manager')
    def my_view(request):
        ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            # Kullanıcının rollerini kontrol et
            user_groups = set(request.user.groups.values_list("name", flat=True))
            required_roles = set(roles)

            # Eğer kullanıcı gerekli rollerden en az birine sahipse izin ver
            if user_groups.intersection(required_roles):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("Bu sayfaya erişmek için gerekli yetkiniz yok.")

        return wrapped_view

    return decorator
