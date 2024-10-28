from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet as UVS
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from subscriptions.models import Subscription
from .serializers import UserSerializer, AvatarSetRetypeDeleteSerializer

User = get_user_model()


class UserViewSet(UVS):
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'me_avatar':
            return AvatarSetRetypeDeleteSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar', url_name='me_avatar')
    def me_avatar(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "PUT":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            instance = self.get_object()
            if instance.avatar:
                instance.avatar.delete(save=True)
                return Response({'Аватар успешно удален'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'Аватар не найден'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.filter(subscriptions__user=user)

        serializer = UserSerializer(queryset, many=True, context={"request": request,})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, *args, **kwargs):
        subscriber = request.user
        author = self.get_object()
        if request.method == "POST":
            _, created = Subscription.objects.get_or_create(user=subscriber, subscription=author)
            if created:
                serializer = UserSerializer(author, context={"request": request,})
                return Response(serializer.data, status=status.HTTP_201_CREATED )
            return Response({'Вы уже подписаны на этого автора'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            subscription = Subscription.objects.filter(user=subscriber, subscription=author)
            if subscription.exists():
                subscription.delete()
                return Response({'Вы успешно отписались от этого автора'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'Вы не были подписаны на этого автора'}, status=status.HTTP_400_BAD_REQUEST)

