from django.db import models

from apps.repos.models import Repository


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
