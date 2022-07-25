import reportlab
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
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


def ingredients_list_to_pdf(ingredients_list):
    reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + "/reportlab/fonts/")
    pdfmetrics.registerFont(TTFont("htc-hand", "htc-hand.ttf", "UTF-8"))
    filename = "shopping_list.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    page = canvas.Canvas(response, pagesize=A4)
    # A4 = 210 mm x 297 mm
    # рамка
    page.setStrokeColorRGB(0, 0, 0)
    page.rect(20 * mm, 35 * mm, 170 * mm, 240 * mm, fill=0)
    # cписок
    height = 262
    page.setFillColorRGB(0, 0, 0)
    page.setFont("htc-hand", size=32)
    page.drawCentredString(105 * mm, height * mm, "Список ингредиентов")
    page.setFont("htc-hand", size=16)
    height -= 10
    for string in ingredients_list:
        page.drawString(100, height * mm, string)
        height -= 8
        if height < 50:
            page.drawString(100, height * mm, "Все ингердиенты не поместились...")
            break
    # подвал
    page.drawString(20 * mm, 25 * mm, "Документ подготовлен и разработан nvkey")
    # картинка github
    image_path = str(settings.BASE_DIR) + "/reportlab/images/"
    github_black = image_path + "github_black.png"
    page.drawImage(
        github_black,
        20 * mm,
        12 * mm,
        height=10 * mm,
        width=10 * mm,
        mask=(0, 0, 0, 0.3),
    )
    # ссылка на репозиторий
    page.setFillColorRGB(0, 0, 204)
    page.drawString(30 * mm, 16 * mm, "https://github.com/nvkey")
    page.showPage()
    page.save()
    return response
