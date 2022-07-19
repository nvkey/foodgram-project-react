# Generated by Django 4.0.6 on 2022-07-17 21:08

import json

from django.db import migrations

"""
Миграции тестовых данных из json
Формат импорта:
[путь, приложение, модель]

"""

data_list = [
    ["data/users.json", "users", "CustomUser"],
    ["data/follows.json", "users", "Follow"],
    ["data/ingredients.json", "recipes", "Ingredient"],
    ["data/tags.json", "recipes", "Tag"],
    ["data/recipes.json", "recipes", "Recipe"],
    ["data/recipe_tags.json", "recipes", "TagsRecipe"],
    ["data/ingredients_in_recipe.json", "recipes", "IngredientInRecipe"],
]


def add_data(apps, schema_editor):
    for data_flow in data_list:
        path = data_flow[0]
        with open(path, encoding="utf-8") as file:
            initial_data = json.load(file)
        model = apps.get_model(data_flow[1], data_flow[2])
        for data in initial_data:
            new_data = model(**data)
            new_data.save()


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [migrations.RunPython(add_data)]
