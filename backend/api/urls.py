from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .user_view import UserViewSetForRequests
from .views import RecipeViewSet, IngredientViewSet, TagViewSet

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingidients')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('users', UserViewSetForRequests, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
]
