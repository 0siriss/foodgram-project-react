from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from backend.api.user_view import UserViewSetForRequests

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('users', UserViewSetForRequests)

urlpatterns = [
    path('', include(router_v1.urls)),
]