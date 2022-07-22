from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Ingredient, IngredientInRecipe, Tag, TagsRecipe


def create_tags_ingredients(recipe, tags, ingredients):
    for tag in tags:
        current_tag = get_object_or_404(Tag, id=tag.pk)
        TagsRecipe.objects.get_or_create(recipe=recipe, tag=current_tag)
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient, id=ingredient["id"].id)
        IngredientInRecipe.objects.get_or_create(
            recipe=recipe,
            ingredient=current_ingredient,
            amount=ingredient["amount"],
        )


def create_action_recipe_or_error(
    method,
    user,
    recipe,
    model_action,
    serializer_class,
    error_post_message,
    error_delete_message,
):
    if method == "POST":
        if model_action.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                data=error_post_message,
                status=status.HTTP_400_BAD_REQUEST,
            )
        model_action.objects.get_or_create(user=user, recipe=recipe)
        data = get_object_or_404(model_action, user=user, recipe=recipe)
        serializer = serializer_class(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    instance = get_object_or_404(model_action, user=user, recipe=recipe)
    instance.delete()
    return Response(
        data=error_delete_message,
        status=status.HTTP_204_NO_CONTENT,
    )
