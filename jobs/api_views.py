from rest_framework import viewsets
from .models import Job, Source, Category, Technology
from .serializers import (
    JobSerializer,
    SourceSerializer,
    CategorySerializer,
    TechnologySerializer,
)


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all().order_by("-score")
        fuente = self.request.query_params.get("fuente")
        busqueda = self.request.query_params.get("q")

        if fuente:
            queryset = queryset.filter(source__nombre=fuente)
        if busqueda:
            queryset = queryset.filter(titulo__icontains=busqueda)
        return queryset


class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer