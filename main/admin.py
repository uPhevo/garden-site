from django.contrib import admin
from flowers.models import Category, Flower
from flowers.models import WorkCondition, About, Contacts

@admin.register(Contacts)
class WorkConditionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")

@admin.register(About)
class WorkConditionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")

@admin.register(WorkCondition)
class WorkConditionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category", "in_stock")
