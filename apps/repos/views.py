from django.db.models import Sum, F, Window
from django.db.models.functions import ExtractYear, RowNumber
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.repos.models import Repository, RepositoryLanguage
from apps.repos.serializers import RepositorySerializer


class RepositoryReportView(viewsets.GenericViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    @action(detail=False, methods=["GET"], url_path="Get_languages")
    def all_language(self, request):
        data = (
            RepositoryLanguage.objects
            .annotate(year=ExtractYear("repository__created_at"))
            .values("year", "language__name")
            .annotate(total_size=Sum("size"))
            .annotate(
                row_number=
                Window(expression=RowNumber(),
                       partition_by=[F("year")],
                       order_by=F("total_size").desc()
                       )
            )
            .filter(row_number__lte=5)
            .order_by("year", "-total_size")
        )

        return Response(data)
