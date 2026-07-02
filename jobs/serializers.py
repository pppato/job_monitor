from rest_framework import serializers
from .models import Job, Source, Category, Technology
 
 
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "nombre", "url_base"]
 
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "nombre"]
 
 
class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "nombre"]
 
 
class JobSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
 
    class Meta:
        model = Job
        fields = [
            "id",
            "titulo",
            "empresa",
            "descripcion",
            "ubicacion",
            "url_original",
            "fecha_publicacion",
            "fecha_scraping",
            "source",
            "category",
            "score",
        ]