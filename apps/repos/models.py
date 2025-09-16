from django.db import models

from apps.language.models import Language
from apps.topics.models import Topic


class Repository(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stars = models.IntegerField()
    forks = models.IntegerField()
    watchers = models.IntegerField()
    is_fork = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    languages = models.ManyToManyField(
        Language,
        through="RepositoryLanguage",
        related_name="repositories"
    )
    language_count = models.IntegerField()
    topics = models.ManyToManyField(Topic, through="TopicsStars", related_name="repositories")
    topic_count = models.IntegerField()
    disk_usage_kb = models.BigIntegerField()
    pull_requests = models.IntegerField()
    issues = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    primary_language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    default_branch_commit_count = models.FloatField(null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)
    assignable_user_count = models.IntegerField()
    code_of_conduct = models.CharField(max_length=255, null=True, blank=True)
    forking_allowed = models.BooleanField()
    name_with_owner = models.CharField(max_length=255, unique=True)
    parent = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"


class RepositoryLanguage(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    size = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ("repository", "language")

    def __str__(self):
        return f"{self.repository.name} - {self.language.name} ({self.size})"


class TopicsStars(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    stars = models.BigIntegerField()

    class Meta:
        unique_together = ('repo', 'topic')

    def __str__(self):
        return f"{self.repository.name} - {self.topic.name} ({self.stars} stars)"
