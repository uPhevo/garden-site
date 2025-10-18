from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Policy(models.Model):
    title = models.CharField(max_length=200, default="Политика конфиденциальности", verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Основной текст")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"
        ordering = ['-updated_at']

    def __str__(self):
        # Просто показываем дату последнего обновления, без несуществующего поля
        return f"Политика от {self.updated_at.strftime('%d.%m.%Y %H:%M')}"


class Contacts(models.Model):
    title = models.CharField(max_length=200, default="Связь с нами", verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Связь с нами")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Связь с нами"
        verbose_name_plural = "Связь с нами"

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=200, default="О нас", verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Текст о нас")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.title


class WorkCondition(models.Model):
    title = models.CharField(max_length=200, default="Условия работы", verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Текст условий работы")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Условия работы"
        verbose_name_plural = "Условия работы"

    def __str__(self):
        return self.title


class Contact(models.Model):
    title = models.CharField(max_length=200, default="Контакты", verbose_name="Заголовок")
    content = RichTextUploadingField(verbose_name="Текст контактов")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Flower(models.Model):
    name = models.CharField("Название", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="flowers", verbose_name="Категория")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Фото", upload_to="flowers/")
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Карточка товара"
        verbose_name_plural = "Карточки товаров"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # предполагаем, что у тебя есть view для детальной страницы цветка с именем 'flower_detail'
        return reverse('flower_detail', args=[self.pk])


# -------------------------
# Новая модель Review
# -------------------------
class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 6)]

    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Email", blank=True, null=True)
    rating = models.IntegerField("Оценка", choices=RATING_CHOICES, default=5)
    text = models.TextField("Текст отзыва", max_length=2000)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    is_published = models.BooleanField("Опубликовать", default=True, help_text="Если включено — отзыв виден на сайте")
    admin_notes = models.TextField("Заметки администратора", blank=True, null=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating} / {self.created_at.strftime('%d.%m.%Y')}"
