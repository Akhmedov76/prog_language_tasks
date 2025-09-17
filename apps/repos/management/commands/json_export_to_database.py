import json

from django.core.management.base import BaseCommand

from apps.language.models import Language
from apps.repos.models import Repository, RepositoryLanguage, TopicsStars
from apps.topics.models import Topic

BATCH_SIZE = 5000


class Command(BaseCommand):
    help = "JSON import qilish"

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="JSON fayl manzili")

    def handle(self, *args, **opts):
        path = opts["json_path"]

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            repos = []

            for repo_data in data:
                owner, _ = Repository.objects.get_or_create(username=repo_data.get("owner"))
                primary_lang, _ = Language.objects.get_or_create(
                    name=repo_data.get("primaryLanguage")
                )
                repo = Repository(
                    owner=owner,
                    name=repo_data.get("name"),
                    stars=repo_data.get("stars"),
                    forks=repo_data.get("forks"),
                    watchers=repo_data.get("watchers"),
                    isFork=repo_data.get("isFork"),
                    isArchived=repo_data.get("isArchived"),
                    languagesCount=repo_data.get("languagesCount"),
                    topicCount=repo_data.get("topicCount"),
                    diskUsageKb=repo_data.get("diskUsageKb"),
                    pullRequests=repo_data.get("pullRequests"),
                    issues=repo_data.get("issues"),
                    description=repo_data.get("description"),
                    primaryLanguage=primary_lang,
                    createdAt=repo_data.get("createdAt"),
                    pushedAt=repo_data.get("pushedAt"),
                    defaultBranchCommitCount=repo_data.get("defaultBranchCommitCount"),
                    license=repo_data.get("license"),
                    assignableUserCount=repo_data.get("assignableUserCount"),
                    codeOfConduct=repo_data.get("codeOfConduct"),
                    forkingAllowed=repo_data.get("forkingAllowed"),
                    nameWithOwner=repo_data.get("nameWithOwner"),
                    parent=repo_data.get("parent"),
                )
                repo.save()

                for lang in repo_data.get("languages", []):
                    lang_obj, _ = Language.objects.get_or_create(
                        name=lang.get("name")
                    )
                    RepositoryLanguage.objects.create(
                        repo=repo,
                        language=lang_obj,
                        size=lang.get("size"),
                    )

                for topic in repo_data.get("topics", []):
                    topic_obj, _ = Topic.objects.get_or_create(name=topic.get("topic"))
                    TopicsStars.objects.create(
                        repo=repo,
                        topic=topic_obj,
                        stars=topic.get("stars"),
                    )

                repos.append(repo)

                if len(repos) >= BATCH_SIZE:
                    self.stdout.write(f"{len(repos)} repo import qilindi.")
                    repos.clear()

        self.stdout.write(self.style.SUCCESS("Import tugadi"))

# import json
#
# from django.core.management.base import BaseCommand
# from django.db import transaction
#
# from apps.language.models import Language
# from apps.repos.models import Repository, RepositoryLanguage, TopicsStars
# from apps.topics.models import Topic
#
#
# class Command(BaseCommand):
#     help = "Import repositories from JSON file"
#
#     def add_arguments(self, parser):
#         parser.add_argument("json_file", type=str, help="Path to JSON file")
#
#     def handle(self, *args, **options):
#         json_file = options["json_file"]
#
#         with open(json_file, "r", encoding="utf-8") as f:
#             data = json.load(f)
#
#         with transaction.atomic():
#             languages = {l.name: l for l in Language.objects.all()}
#             topics = {t.name: t for t in Topic.objects.all()}
#
#             repos = []
#             repo_languages = []
#             repo_topics = []
#             for repo_data in data:
#                 print("Processing repo {}".format(repo_data["name"]))
#                 repo = Repository(
#                     owner=repo_data["owner"],
#                     name=repo_data["name"],
#                     stars=repo_data["stars"],
#                     forks=repo_data["forks"],
#                     watchers=repo_data["watchers"],
#                     is_fork=repo_data["isFork"],
#                     is_archived=repo_data["isArchived"],
#                     language_count=repo_data["languageCount"],
#                     topic_count=repo_data["topicCount"],
#                     disk_usage_kb=repo_data["diskUsageKb"],
#                     pull_requests=repo_data["pullRequests"],
#                     created_at=repo_data.get("createdAt"),
#                     pushed_at=repo_data.get("pushedAt"),
#                     issues=repo_data["issues"],
#                     description=repo_data.get("description"),
#                     primary_language=repo_data.get("primaryLanguage"),
#                     default_branch_commit_count=repo_data.get("defaultBranchCommitCount", 0),
#                     license=repo_data.get("license"),
#                     assignable_user_count=repo_data.get("assignableUserCount", 0),
#                     code_of_conduct=repo_data.get("codeOfConduct"),
#                     forking_allowed=repo_data["forkingAllowed"],
#                     name_with_owner=repo_data["nameWithOwner"],
#                     parent=repo_data.get("parent"),
#                 )
#                 repos.append(repo)
#
#             Repository.objects.bulk_create(repos, ignore_conflicts=True)
#             created_repos = Repository.objects.filter(
#                 name_with_owner__in=[r.name_with_owner for r in repos]
#             )
#             repo_map = {r.name_with_owner: r for r in created_repos}
#
#             repo_obj = repo_map[repo_data["nameWithOwner"]]
#
#             print("language qoshilmoqda")
#
#             for lang_data in repo_data.get("languages", []):
#                 lang_name = lang_data["name"]
#                 if lang_name in languages:
#                     lang_obj = languages[lang_name]
#                 else:
#                     lang_obj = Language.objects.create(name=lang_name)
#                     languages[lang_name] = lang_obj
#                 repo_languages.append(RepositoryLanguage(
#                     repository=repo_obj,
#                     language=lang_obj,
#                     size=lang_data.get("size", 0)
#                 ))
#
#             print("topic qoshilmoqda")
#
#             for topic_data in repo_data.get("topics", []):
#                 topic_name = topic_data["name"]
#                 if topic_name in topics:
#                     topic_obj = topics[topic_name]
#                 else:
#                     topic_obj = Topic.objects.create(name=topic_name)
#                     topics[topic_name] = topic_obj
#                 repo_topics.append(TopicsStars(
#                     repository=repo_obj,
#                     topic=topic_obj,
#                     stars=topic_data.get("stars", 0)
#                 ))
#
#         Repository.objects.bulk_create(repos, ignore_conflicts=True)
#         RepositoryLanguage.objects.bulk_create(repo_languages, ignore_conflicts=True)
#         TopicsStars.objects.bulk_create(repo_topics, ignore_conflicts=True)
#
#         self.stdout.write(self.style.SUCCESS("Import tugadil"))
