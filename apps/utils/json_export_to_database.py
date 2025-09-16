import json

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.language.models import Language
from apps.repos.models import Repository, RepositoryLanguage, TopicsStars
from apps.topics.models import Topic


class Command(BaseCommand):
    help = "Import repositories from JSON file"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to JSON file")

    def handle(self, *args, **options):
        json_file = options["json_file"]
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.stdout.write(self.style.WARNING("Import boshlandi..."))

        with transaction.atomic():
            all_languages = {lang["name"] for d in data for lang in d["languages"]}
            all_topics = {t["name"] for d in data for t in d.get("topics", [])}

            Language.objects.bulk_create(
                [Language(name=name) for name in all_languages], ignore_conflicts=True
            )
            Topic.objects.bulk_create(
                [Topic(name=name) for name in all_topics], ignore_conflicts=True
            )

            langs_db = {l.name: l for l in Language.objects.filter(name__in=all_languages)}
            topics_db = {t.name: t for t in Topic.objects.filter(name__in=all_topics)}

            repos = []
            repo_languages = []
            repo_topics = []

            for d in data:
                repo = Repository(
                    owner=d["owner"],
                    name=d["name"],
                    stars=d["stars"],
                    forks=d["forks"],
                    watchers=d["watchers"],
                    is_fork=d["isFork"],
                    is_archived=d["isArchived"],
                    language_count=d["languageCount"],
                    topic_count=d["topicCount"],
                    disk_usage_kb=d["diskUsageKb"],
                    pull_requests=d["pullRequests"],
                    issues=d["issues"],
                    description=d.get("description"),
                    primary_language=d.get("primaryLanguage"),
                    created_at=d.get("createdAt"),
                    pushed_at=d.get("pushedAt"),
                    default_branch_commit_count=d.get("defaultBranchCommitCount", 0),
                    license=d.get("license"),
                    assignable_user_count=d.get("assignableUserCount", 0),
                    code_of_conduct=d.get("codeOfConduct"),
                    forking_allowed=d["forkingAllowed"],
                    name_with_owner=d["nameWithOwner"],
                    parent=d.get("parent"),
                )
                repos.append(repo)

                for lang in d["languages"]:
                    lang_obj = langs_db.get(lang["name"])
                    if lang_obj:
                        repo_languages.append(
                            RepositoryLanguage(repository=repo, language=lang_obj, size=lang["size"])
                        )

                for t in d.get("topics", []):
                    topic_obj = topics_db.get(t["name"])
                    if topic_obj:
                        repo_topics.append(
                            TopicsStars(repository=repo, topic=topic_obj, stars=t["stars"])
                        )

            Repository.objects.bulk_create(repos, ignore_conflicts=True)
            RepositoryLanguage.objects.bulk_create(repo_languages, ignore_conflicts=True)
            TopicsStars.objects.bulk_create(repo_topics, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("Import tugadi"))
