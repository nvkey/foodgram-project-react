from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow

from .filters import IngredientFilter, RecipeFilter
from .paginations import CustomPageNumberPaginator
from .permissions import (AuthorOrStaffAccessPermissionOrReadOnly,
                          StaffAccessPermissionOrReadOnly)
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)


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
        queryset = Recipe.objects.all()
        user = get_object_or_404(CustomUser, username=self.request.user)
        favorite = self.request.query_params.get("is_favorited")
        cart = self.request.query_params.get("is_in_shopping_cart")
        if favorite is not None:
            queryset_recipe_ids = user.favorite_recipes.all().values("recipe_id")
            queryset = Recipe.objects.filter(pk__in=queryset_recipe_ids)
        if cart is not None:
            queryset_recipe_ids = user.shopping_cart.all().values("recipe_id")
            queryset = Recipe.objects.filter(pk__in=queryset_recipe_ids)
        return queryset

    def get_serializer_class(self):
        if self.action == "favorite" or self.action == "shopping_cart":
            return FavoriteSerializer
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

        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    data=f"Рецепт {recipe.name} уже есть в избранном",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.get_or_create(user=user, recipe=recipe)
            data = get_object_or_404(Favorite, user=user, recipe=recipe)
            serializer = self.get_serializer(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            instance = get_object_or_404(Favorite, user=user, recipe=recipe)
            instance.delete()
            return Response(
                "Репцепт успешно удален из избранного",
                status=status.HTTP_204_NO_CONTENT,
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

        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    data=f"Рецепт {recipe.name} уже есть в списке покупок",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.get_or_create(user=user, recipe=recipe)
            data = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
            serializer = self.get_serializer(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            instance = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
            instance.delete()
            return Response(
                "Репцепт успешно удален из списка покупок",
                status=status.HTTP_204_NO_CONTENT,
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

        ingredients_recipes = IngredientInRecipe.objects.filter(recipe__in=recipes)
        ingredients = {}
        for obj in ingredients_recipes:
            key = obj.ingredient.id
            name = obj.ingredient.name
            measure = obj.ingredient.measurement_unit
            amount = obj.amount
            if key in ingredients:
                ingredients.get(key)[1] += amount
            else:
                ingredients.update({key: [f"{name} ", amount, f" {measure}"]})
        ingredients_list = []
        for item in ingredients.values():
            ingredients_list.append("".join(map(str, item)))

        data = (
            "Список покупок:\n"
            "Список рецептов:\n"
            + "\n".join(recipes_list)
            + "\n\n"
            + "Список всех ингредлиентов:\n"
            + "\n".join(ingredients_list)
            + "\n\n"
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
