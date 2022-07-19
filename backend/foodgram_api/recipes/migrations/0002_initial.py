# Generated by Django 4.0.6 on 2022-07-17 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                help_text="Список ингредиентов",
                related_name="recipes",
                through="recipes.IngredientInRecipe",
                to="recipes.ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                help_text="Выберите тэг",
                related_name="recipes",
                through="recipes.TagsRecipe",
                to="recipes.tag",
            ),
        ),
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="recipes.ingredient",
            ),
        ),
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="recipes.recipe",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_recipes",
                to="recipes.recipe",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_recipes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredientinrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredient"), name="unique_recipe_ingredient"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_recipe_user"
            ),
        ),
    ]
