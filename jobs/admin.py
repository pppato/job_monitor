from django.contrib import admin
from .models import Source, Category, Technology, Job, ScoringKeyWord, JobTechnology


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("nombre", "url_base")
    search_fields = ("nombre",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class JobTechnologyInline(admin.TabularInline):
    model = JobTechnology
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "source", "category", "score", "fecha_scraping")
    list_filter = ("source", "category")
    search_fields = ("titulo", "empresa")
    ordering = ("-score",)
    date_hierarchy = "fecha_scraping"
    inlines = [JobTechnologyInline]


@admin.register(ScoringKeyWord)
class ScoringKeyWordAdmin(admin.ModelAdmin):
    list_display = ("termino", "peso")
    search_fields = ("termino",)
    ordering = ("-peso",)