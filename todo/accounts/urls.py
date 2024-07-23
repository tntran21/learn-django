from django.urls import path
from accounts.views import AccountsManager


urlpatterns = [
    path("signup/", AccountsManager.account_signup, name="signup"),
    path("login/", AccountsManager.account_login, name="login"),
    path("update/", AccountsManager.account_update, name="update-account"),
]
