from django.contrib import admin

from apps.topics.models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("-name",)
