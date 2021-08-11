from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',)


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'confirmation_code', 'email',)


class UsersSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=get_user_model().objects.all())
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=get_user_model().objects.all())
        ]
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'bio', 'first_name',
                  'last_name', 'email', 'role',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
