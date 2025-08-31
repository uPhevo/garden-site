from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField  # для редактируемого текста с загрузкой картинок

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
