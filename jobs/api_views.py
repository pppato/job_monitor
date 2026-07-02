import django_filters
from rest_framework import viewsets
from .models import Job, Source, Category, Technology
from .serializers import (
    JobSerializer,
    SourceSerializer,
    CategorySerializer,
    TechnologySerializer,
)


class JobFilter(django_filters.FilterSet):
    fuente = django_filters.CharFilter(field_name="source__nombre", lookup_expr="iexact")

    class Meta:
        model = Job
        fields = ["fuente", "category"]


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all().order_by("-score")
    serializer_class = JobSerializer
    filterset_class = JobFilter
    search_fields = ["titulo"]


class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer