from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name="Название тега",
        help_text="Список рецептов отмеченных тегом",
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name="Цвет тега",
        help_text="Цвет тега в HEX",
    )
    slug = models.SlugField(
        unique=True,
        validators=[
            RegexValidator(
                regex="^[-a-zA-Z0-9_]+$", message="Only ^[-a-zA-Z0-9_]+$"
            )
        ],
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        constraints = [models.UniqueConstraint(fields=["slug"], name="unique_slug")]

    def __str__(self) -> str:
        return str(self.name)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название ингридиента",
        help_text="Ингредиент для рецепта",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
        help_text="Единицы измерения ингредиента",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self) -> str:
        return str(self.name)


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    text = models.TextField("Текст рецепта", help_text="Текст нового рецепта")
    tags = models.ManyToManyField(
        Tag,
        through="TagsRecipe",
        related_name="recipes",
        help_text="Выберите тэг",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        related_name="recipes",
        verbose_name="Ингредиенты",
        help_text="Список ингредиентов",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="recipes/",
        blank=True,
        null=True,
        help_text="Загрузите картинку",
    )
    cooking_time = models.SmallIntegerField(
        verbose_name="Время приготовления",
        validators=[
            MinValueValidator(1, message="Время приготовления не менее 1 минуты"),
            MaxValueValidator(1440, message="Время приготовления не более 1440 минут"),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата публицации",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return str(self.name)


class TagsRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Тег рецпта"
        verbose_name_plural = "Теги рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "recipe"], name="unique_slug_recipe"
            )
        ]


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="Количество ингредиента не менее 1 единицы"),
            MaxValueValidator(
                10000, message="Кухня не резиновая, не более 10000 единиц"
            ),
        ],
        verbose_name="Количество",
        help_text="Количество ингредиента",
    )

    class Meta:
        verbose_name = "Ингредиент в рецепта"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="unique_recipe_ingredient"
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
    )

    class Meta:
        verbose_name = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_recipe_user"
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shopping_cart"
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe"
            )
        ]
