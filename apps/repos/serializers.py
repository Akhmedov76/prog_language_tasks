from rest_framework import serializers

from apps.language.serializers import LanguageSerializer
from apps.repos.models import Repository
from apps.topics.serializers import TopicSerializer


class RepositorySerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = [
            "id", "owner", "name", "stars", "forks", "watchers",
            "is_fork", "is_archived", "language_count", "topic_count",
            "disk_usage_kb", "pull_requests", "issues", "description",
            "primary_language", "created_at", "pushed_at",
            "default_branch_commit_count", "license",
            "assignable_user_count", "code_of_conduct",
            "forking_allowed", "name_with_owner", "parent",
            "languages", "topics"
        ]
