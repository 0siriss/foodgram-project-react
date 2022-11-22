from django.db.models import Sum
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RecipeForUserSerializer, UserSerializer
from ..users.models import User
from .filters import IngredientFilter, RecipeFilter
from backend.recipes.models import Ingredient, Recipe, Tag
from .permissions import AuthPostAuthorChangesOrReadOnly
from .serializers import (
    IngredientRecipe, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer,
    TagSerializer, UserAuthSerializer
)
from .services import add_or_del_obj, create_shopping_list


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('^name',)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthPostAuthorChangesOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        return add_or_del_obj(
            pk, request, request.user.favorites,
            RecipeForUserSerializer
        )

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk):
        return add_or_del_obj(
            pk, request, request.user.shopping_cart,
            RecipeForUserSerializer
        )

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        filename = f'{user.username}_shopping_list.txt'
        recipes_in_cart = user.shopping_cart.all()
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=recipes_in_cart
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))
        text_list = create_shopping_list(ingredients)
        response = HttpResponse(text_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{filename}"'
        )
        return response


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
