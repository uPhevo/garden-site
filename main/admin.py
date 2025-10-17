# flowers/admin.py
from django.contrib import admin
from django.utils.html import strip_tags
from flowers.models import Category, Flower, WorkCondition, About, Contacts, Policy

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_content',  'updated_at')
    search_fields = ('content',)
    readonly_fields = ('updated_at',)

    def short_content(self, obj):
        text = strip_tags(obj.content or '')
        if len(text) > 120:
            return text[:117].rstrip() + '...'
        return text
    short_content.short_description = 'Текст (кратко)'


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(WorkCondition)
class WorkConditionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category", "in_stock")
