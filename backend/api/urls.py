from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .user_view import UserViewSetForRequests
from .views import RecipeViewSet, IngredientViewSet, TagViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('users', UserViewSetForRequests)

urlpatterns = [
    path('', include(router_v1.urls)),
]
