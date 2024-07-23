from rest_framework import serializers
from .models import Accounts
from rest_framework.exceptions import ValidationError
from djangorestframework_camel_case.util import camelize, underscoreize


class AccountsSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = (
            "id",
            "user_name",
            "email",
            "password",
            "created_at",
            "updated_at",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Accounts(
            user_name=validated_data["user_name"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        # Convert to camelCase for the response
        ret = super().to_representation(instance)
        return camelize(ret)

    def to_internal_value(self, data):
        # Convert to snake_case for saving to the database
        data = underscoreize(data)
        return super().to_internal_value(data)


class AccountsLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = Accounts.objects.get(email=data["email"])
        except Accounts.DoesNotExist:
            raise ValidationError(serializers.ValidationError("User does not exist"))
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Password is incorrect")
        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        return user
