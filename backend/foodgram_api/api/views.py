from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from users.models import CustomUser, Follow
from .filters import IngredientFilter, RecipeFilter
from .paginations import CustomPageNumberPaginator
from .permissions import (AuthorOrStaffAccessPermissionOrReadOnly,
                          StaffAccessPermissionOrReadOnly)
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)
from .services import create_action_recipe_or_error


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [StaffAccessPermissionOrReadOnly]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrStaffAccessPermissionOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.request.user)
        favorite = self.request.query_params.get("is_favorited")
        cart = self.request.query_params.get("is_in_shopping_cart")
        if favorite is not None:
            queryset_recipe_ids = user.favorite_recipes.all().values("recipe_id")
            return Recipe.objects.filter(pk__in=queryset_recipe_ids)
        if cart is not None:
            queryset_recipe_ids = user.shopping_cart.all().values("recipe_id")
            return Recipe.objects.filter(pk__in=queryset_recipe_ids)
        return Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "POST", "PATCH"]:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        user = get_object_or_404(CustomUser, username=self.request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        method = request.method
        model_action = Favorite
        serializer_class = FavoriteSerializer
        error_post_message = f"Рецепт {recipe.name} уже есть в избранном"
        error_delete_message = "Репцепт успешно удален из избранного"
        return create_action_recipe_or_error(
            method,
            user,
            recipe,
            model_action,
            serializer_class,
            error_post_message,
            error_delete_message,
        )

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        user = get_object_or_404(CustomUser, username=self.request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        method = request.method
        model_action = ShoppingCart
        serializer_class = FavoriteSerializer
        error_post_message = f"Рецепт {recipe.name} уже есть в списке покупок"
        error_delete_message = "Репцепт успешно удален из списка покупок"
        return create_action_recipe_or_error(
            method,
            user,
            recipe,
            model_action,
            serializer_class,
            error_post_message,
            error_delete_message,
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        queryset_recipes = user.shopping_cart.all()
        recipes = Recipe.objects.filter(pk__in=queryset_recipes.values("recipe_id"))

        recipes_list = recipes.values_list("name", flat=True)

        with connection.cursor() as cursor:
            query = """
                    with raw_data as (SELECT
                    b.ingredient_id,
                    b.amount,
                    c.name as ingredient_name,
                    c.measurement_unit
                    FROM
                    recipes_shoppingcart AS a
                    JOIN
                    recipes_ingredientinrecipe AS b
                    on a.recipe_id=b.recipe_id
                    JOIN
                    recipes_ingredient as c
                    on b.ingredient_id=c.id
                    WHERE
                    user_id=%s)
                    select
                    ingredient_name,
                    SUM (amount),
                    measurement_unit
                    from raw_data
                    group by
                    ingredient_name, measurement_unit
                    """
            cursor.execute(query, [user.id])
            cursor_list = [i for i in cursor]
            ingredients_list = []
            for ingredient in cursor_list:
                line = [i for i in ingredient]
                ingredients_list.append(" ".join(map(str, line)))

            data = (
                "Список рецептов:\n"
                + "\n".join(recipes_list)
                + "\n\n"
                + "Список покупки ингредиентов:\n"
                + "\n".join(ingredients_list)
            )
        filename = "shopping_list.txt"
        response = HttpResponse(data, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename={0}".format(filename)
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [StaffAccessPermissionOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class FollowListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Запро подписок пользователя"""
        user = self.request.user
        return Follow.objects.filter(user=user).select_related("following")
