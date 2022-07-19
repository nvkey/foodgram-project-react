from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import FollowSerializer

from .models import CustomUser, Follow


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=FollowSerializer,
    )
    def subscribe(self, request, id):
        user = get_object_or_404(CustomUser, username=self.request.user)
        following = get_object_or_404(CustomUser, pk=id)

        if request.method == "POST":
            if Follow.objects.filter(user=user, following=following).exists():
                return Response(
                    data=f"Вы уже подписаны на пользователя {following.username}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user == following:
                return Response(
                    data="Не возможно подписаться на себя",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.create(user=user, following=following)
            data = get_object_or_404(Follow, user=user, following=following)
            serializer = self.get_serializer(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        instance = get_object_or_404(Follow, user=user, following=following)
        instance.delete()
        return Response("Успешная отписка", status=status.HTTP_204_NO_CONTENT)
