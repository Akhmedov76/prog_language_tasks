from django.contrib import admin

from apps.language.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
