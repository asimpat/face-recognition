from rest_framework import serializers
from .models import User, Face
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "password",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FaceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Face
        fields = (
            "id",
            "user",
            "image",
            "enrolled_at",
        )
        read_only_fields = ("id", "enrolled_at")


class UserDetailSerializer(serializers.ModelSerializer):
    face = FaceSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "face",
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {"detail": "Invalid email or password."})
        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "User account is inactive."})

        attrs["user"] = user
        return attrs