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
            if '_subscribed_users' not in self.context:
                self.context['_subscribed_users'] = set(
                    Subscription.objects.filter(user=request.user)
                    .values_list('subscription_id', flat=True)
                )
            subscribed_users = self.context['_subscribed_users']
            return obj.id in subscribed_users
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

    def get_recipes_queryset(self, obj):
        return obj.recipes.prefetch_related('ingredients')

    def get_recipes(self, obj):
        queryset = self.get_recipes_queryset(obj)
        limit = self.context.get('recipes_limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        from recipes.api.v1.serializers import RecipeMiniSerializer
        return RecipeMiniSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return self.get_recipes_queryset(obj).count()


class AvatarSetRetypeDeleteSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    def validate(self, attrs):
        if 'avatar' not in attrs or not attrs['avatar']:
            raise serializers.ValidationError(
                {"avatar": "Поле 'avatar' не может быть пустым."}
            )
        return attrs

    class Meta:
        model = User
        fields = ('avatar',)
