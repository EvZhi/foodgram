from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as UVS
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from paginations import CustomPagination
from subscriptions.models import Subscription

from .serializers import (AvatarSetRetypeDeleteSerializer,
                          CustomUserCreateSerializer, CustomUserSerializer,
                          SubscriptionSerializer)

User = get_user_model()


class UserViewSet(UVS):
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'me_avatar':
            return AvatarSetRetypeDeleteSerializer
        if self.action == "create":
            return CustomUserCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(
        detail=False,
        methods=['put', 'delete'],
        url_path='me/avatar',
        url_name='me_avatar',
        permission_classes=[IsAuthenticated],
    )
    def me_avatar(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        instance = self.request.user
        if request.method == 'PUT':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            if instance.avatar:
                instance.avatar.delete(save=True)
                return Response(
                    {'Аватар успешно удален'},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'Аватар не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.filter(subscriptions__user=user)
        recipes_limit = request.query_params.get('recipes_limit')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                many=True,
                context={'request': request, 'recipes_limit': recipes_limit},
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(
            queryset,
            many=True,
            context={'request': request, 'recipes_limit': recipes_limit}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, *args, **kwargs):
        subscriber = request.user
        author = self.get_object()
        if subscriber == author:
            return Response(
                "Вы не можете подписаться на себя.",
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            _, created = Subscription.objects.get_or_create(
                user=subscriber, subscription=author
            )
            if created:
                recipes_limit = request.query_params.get('recipes_limit')
                serializer = SubscriptionSerializer(
                    author,
                    context={
                        'request': request, 'recipes_limit': recipes_limit
                    }
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'Вы уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                user=subscriber,
                subscription=author
            )
            if subscription.exists():
                subscription.delete()
                return Response(
                    {'Вы успешно отписались от этого автора'},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'Вы не были подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
