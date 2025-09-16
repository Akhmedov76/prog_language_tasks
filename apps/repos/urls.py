from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepositoryReportView

router = DefaultRouter()
router.register(r"repos", RepositoryReportView, basename="repos")

urlpatterns = [
    path("", include(router.urls)),
]
