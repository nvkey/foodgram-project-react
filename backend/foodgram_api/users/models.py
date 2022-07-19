from django.contrib.auth.models import AbstractUser
from django.db import models
import users.constants as cnst


class CustomUser(AbstractUser):
    USER_ROLE = (
        (cnst.ROLE_USER, "Пользователь"),
        (cnst.ROLE_ADMIN, "Администратор"),
    )
    role = models.CharField(max_length=20, choices=USER_ROLE, default=cnst.ROLE_USER)
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name="Логин пользователя",
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="Почта пользователя",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия пользователя",
    )
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль пользователя",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_admin(self):
        return self.role == cnst.ROLE_ADMIN

    def is_user(self):
        return self.role == cnst.ROLE_USER

    def __str__(self):
        return str(self.username)


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Подписчик",
        help_text="Подписчик на автора рецепта",
        on_delete=models.CASCADE,
        related_name="follower",
    )
    following = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        help_text="Автор рецептов",
        on_delete=models.CASCADE,
        related_name="following",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_user_following"
            )
        ]
