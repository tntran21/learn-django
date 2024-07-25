from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Accounts
from accounts.serializer import AccountsSignupSerializer
from accounts.utils import AccountUtils
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from todo.middleware.token_middleware import api_view_csrf_exempt
from rest_framework.views import APIView


# Create your views here.
class AccountsManager(APIView):
    """
    A class that handles user accounts.

    Methods:
    - account_signup: Handles user signup.
    - account_login: Handles user login.
    - account_logout: Handles user logout.
    - account_update: Handles user account update.
    """

    @api_view(["POST"])
    def account_signup(request):
        """
        Handles user signup.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """

        serializer = AccountsSignupSerializer(data=request.data)
        req_email = request.data["email"]
        response = {}

        # check if email already exists
        email_exists = Accounts.objects.filter(email=req_email).exists()
        if email_exists:
            response["errors"] = "Email already exists"
            response["data"] = None
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response["message"] = "User created successfully"
            response["data"] = serializer.data

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["POST"])
    def account_login(request):
        """
        Handles user login.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """

        email = request.data["email"]
        password = request.data["password"]
        response = {}

        try:
            account = Accounts.objects.get(email=email)
            if account.check_password(password):
                token_payload = {"email": account.email}
                token = AccountUtils.generate_jwt_token(token_payload)

                response["message"] = "Login successful"
                response["data"] = {
                    "user_name": account.user_name,
                    "email": account.email,
                }
                response["token"] = str(token)

                return Response(response, status=status.HTTP_200_OK)
            else:
                response["errors"] = "Invalid credentials"
                response["data"] = None
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Accounts.DoesNotExist:
            response["errors"] = "User does not exist"
            response["data"] = None
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    def account_logout(request):
        """
        Handles user logout.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """

        response = {}
        response["message"] = "Logout successful"
        return Response(response, status=status.HTTP_200_OK)

    @csrf_exempt
    @api_view(["POST"])
    def account_update(request, *args, **kwargs):
        """
        Handles user account update.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """

        response = {}
        user = {
            "email": request.data["email"],
            "user_name": request.data["user_name"],
            "password": request.data["password"],
        }
        serializer = AccountsSignupSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response["message"] = "User updated successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
