from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .user_serializer import UserSerializer
from .user_serializer import UserAuthSerializer
from .services import add_or_del_obj
from rest_framework import status
from rest_framework.decorators import action

from users.models import User


class UserViewSetForRequests(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        follower = self.get_object()
        if request.user == follower:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return add_or_del_obj(
            id, request, request.user.followers, UserAuthSerializer
        )

    @action(
        methods=['get'],
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def subscriptions(self, request):
        user = request.user
        followers = user.followers.all()
        pages = self.paginate_queryset(followers)
        serializer = UserSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
