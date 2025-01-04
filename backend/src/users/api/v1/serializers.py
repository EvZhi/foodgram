from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email",
                  "password")
        extra_kwargs = {"password": {"write_only": True}}


class BaseUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return (
                Subscription.objects
                .filter(user=request.user, subscription=obj)
                .exists()
            )
        return False


class CustomUserSerializer(BaseUserSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'avatar',
        )


class SubscriptionSerializer(BaseUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, obj):
        queryset = obj.recipes.all()
        limit = self.context.get('recipes_limit')
        if limit:
            queryset = queryset[: int(limit)]
        from recipes.api.v1.serializers import RecipeMiniSerializer
        return RecipeMiniSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class AvatarSetRetypeDeleteSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    def validate(self, attrs):
        request = self.context.get('request')
        if request and 'avatar' not in attrs or attrs.get('avatar') is None:
            raise serializers.ValidationError("Отсутствует поле 'avatar'")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar', None)
        if avatar:
            if instance.avatar:
                instance.avatar.delete()
            instance.avatar = avatar
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('avatar',)
