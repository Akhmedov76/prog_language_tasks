from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ExportMixin

from apps.repos.models import Repository, RepositoryLanguage, TopicsStars
from apps.utils.excel import CenterAlignedXLSX

admin.site.unregister(Group)


@admin.register(Repository)
class RepositoryAdmin(ExportMixin, admin.ModelAdmin):
    xlsx_format = CenterAlignedXLSX()

    list_display = (
        "id",
        "owner",
        "name",
        "stars",
        "forks",
        "watchers",
        "primary_language",
        "created_at",
        "pushed_at",
        "is_fork",
        "is_archived",
    )
    list_filter = ("is_fork", "is_archived", "primary_language", "created_at", "pushed_at")
    search_fields = ("owner", "name", "primary_language")
    ordering = ("-stars",)


@admin.register(RepositoryLanguage)
class RepositoryLanguageAdmin(ExportMixin, admin.ModelAdmin):
    xlsx_format = CenterAlignedXLSX()
    list_display = (
        "id", "repository", "language", "size"
    )
    search_fields = ("repository__owner", "repository__name", "language__name")
    ordering = ("-size",)


@admin.register(TopicsStars)
class TopicsStarsAdmin(ExportMixin, admin.ModelAdmin):
    xlsx_format = CenterAlignedXLSX()
    list_display = (
        "id",
        "repository",
        "topic",
        "stars",
    )
    search_fields = ("repository__owner", "topic__name")
    ordering = ("-stars",)
