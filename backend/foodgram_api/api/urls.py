from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import urls as urls_users

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()

router.register("tags", TagViewSet)
router.register("recipes", RecipeViewSet, basename="resipes")
router.register("ingredients", IngredientViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(urls_users)),
]
