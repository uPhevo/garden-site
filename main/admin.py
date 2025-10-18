# flowers/admin.py
from django.contrib import admin
from django.utils.html import strip_tags
from flowers.models import Category, Flower, WorkCondition, About, Contacts, Policy, Review

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


# -------------------------
# Review admin
# -------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'short_text', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('name', 'text', 'email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['make_published', 'make_unpublished']

    def short_text(self, obj):
        txt = obj.text or ''
        return (txt[:80] + '...') if len(txt) > 80 else txt
    short_text.short_description = 'Отзыв'

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} отзыв(ов) опубликовано.")
    make_published.short_description = "Опубликовать выбранные отзывы"

    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} отзыв(ов) снято с публикации.")
    make_unpublished.short_description = "Снять публикацию с выбранных отзывов"
