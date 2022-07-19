from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name="author__id", lookup_expr="exact")
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug", to_field_name="slug", queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags"]


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ["name"]
