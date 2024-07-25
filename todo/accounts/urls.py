from django.urls import path
from accounts.views import AccountsManager
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


def apply_permissions(view_func, permission_classes_list):
    decorator = permission_classes(permission_classes_list)
    return decorator(view_func)


urlpatterns = [
    path("signup/", AccountsManager.account_signup, name="account_signup"),
    path(
        "login/",
        AccountsManager.account_login,
        name="account_login",
    ),
    path(
        "update/",
        csrf_exempt(AccountsManager.account_update),
        name="account_update",
    ),
]
