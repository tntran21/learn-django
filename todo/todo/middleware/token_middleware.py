from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from accounts.models import Accounts
from accounts.utils import AccountUtils
from common.constants.authencation_paths import ProtectedPath
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.utils.deprecation import MiddlewareMixin


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # Code to be executed for each request before
    def __call__(self, request):
        print("Middleware executed: ", request.path)
        if request.path in ProtectedPath:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse(
                    {"errors": "Authorization header is required"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                try:
                    token = auth_header.split(" ")[1]
                    decode_token = AccountUtils.decode_jwt_token(token)
                    if decode_token:
                        account = Accounts.objects.get(email=decode_token["email"])

                        print("---------- token middleware account", account)
                        request.user = account

                except (InvalidToken, TokenError, IndexError):
                    return JsonResponse(
                        {"errors": "Invalid token"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

        response = self.get_response(request)

        return response


class DisableCSRFMiddleware(MiddlewareMixin):
    def progess_request(self, request):
        if request.path.startWith("/api"):
            request.csrf_processing_done = True


@decorator_from_middleware(DisableCSRFMiddleware)
def api_view_csrf_exempt(view_func):
    return view_func
