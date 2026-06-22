from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Note


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username sudah digunakan"
            )
        ],
        error_messages={
            "required": "username wajib diisi",
            "blank": "username wajib diisi",
            "min_length": "username harus 3-50 karakter",
            "max_length": "username harus 3-50 karakter",
        },
    )
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        error_messages={
            "required": "password minimal 6 karakter",
            "blank": "password minimal 6 karakter",
            "min_length": "password minimal 6 karakter",
        },
    )

    def create(self, validated_data):
        # create_user memakai mekanisme hashing password bawaan Django
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )


class NoteSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=100,
        error_messages={
            "required": "title wajib diisi",
            "blank": "title wajib diisi",
            "max_length": "title maksimal 100 karakter",
        },
    )
    body = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = Note
        # user_id sengaja tidak diekspos di respons API
        fields = ["id", "title", "body", "created_at"]
