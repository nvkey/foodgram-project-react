from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import (Ingredient, IngredientInRecipe, Recipe, Tag,
                            TagsRecipe)
from users.models import Follow


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    list_editable = (
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class TagAdminInLine(admin.TabularInline):
    model = TagsRecipe
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    list_editable = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class IngredientAdminInLine(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "text",
        "get_image",
        "image",
        "cooking_time",
        "pub_date",
    )
    list_editable = (
        "author",
        "text",
        "image",
        "cooking_time",
    )
    inlines = [TagAdminInLine, IngredientAdminInLine]
    search_fields = ("author",)
    empty_value_display = "-пусто-"

    def get_image(self, obj):
        if bool(obj.image) is False:
            return
        return mark_safe(f'<img src="{obj.image.url}" height="100>')

    get_image.short_description = "Изображение"


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "amount",
    )
    list_editable = (
        "recipe",
        "ingredient",
        "amount",
    )
    search_fields = (
        "recipe",
        "ingredient",
    )
    empty_value_display = "-пусто-"


class TagsRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "tag",
        "recipe",
    )
    list_editable = (
        "tag",
        "recipe",
    )
    search_fields = (
        "tag",
        "recipe",
    )
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "following",
    )
    list_editable = (
        "user",
        "following",
    )
    search_fields = (
        "user",
        "following",
    )
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(TagsRecipe, TagsRecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
