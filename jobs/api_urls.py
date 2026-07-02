from rest_framework.routers import DefaultRouter
from .api_views import JobViewSet, SourceViewSet, CategoryViewSet, TechnologyViewSet
 
router = DefaultRouter()
router.register("jobs", JobViewSet, basename="job")
router.register("sources", SourceViewSet, basename="source")
router.register("categories", CategoryViewSet, basename="category")
router.register("technologies", TechnologyViewSet, basename="technology")
 
urlpatterns = router.urls