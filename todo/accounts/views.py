from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Accounts
from accounts.serializer import AccountsSignupSerializer, AccountsLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class AccountsManager:
    """
    A class that handles user accounts.

    Methods:
    - account_signup: Handles user signup.
    - account_login: Handles user login.
    - account_logout: Handles user logout.
    - account_update: Handles user account update.
    """

    @api_view(["POST"])
    @permission_classes([AllowAny])
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
    @permission_classes([AllowAny])
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
            user = Accounts.objects.get(email=email)
            if user.check_password(password):
                refresh_token = RefreshToken.for_user(user)

                response["message"] = "Login successful"
                response["data"] = {"user_name": user.user_name, "email": user.email}
                response["refresh_token"] = str(refresh_token)
                response["access_token"] = str(refresh_token.access_token)

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

    @api_view(["POST"])
    def account_update(request):
        """
        Handles user account update.

        Args:
        - request: The HTTP request object.

        Returns:
        - Response: The HTTP response object.
        """

        response = {}
        user = request.user
        serializer = AccountsSignupSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response["message"] = "User updated successfully"
            response["data"] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
