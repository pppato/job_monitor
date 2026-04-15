from django.views.generic import ListView, DetailView
from .models import Job, Source
# Create your views here.
class JobListView(ListView):
    model = Job
    template_name = "job_list.html"
    context_object_name = "jobs"
    queryset = Job.objects.all().order_by("score")
    paginate_by = 20

    def get_queryset(self):
        queryset = Job.objects.all().order_by("score")
        fuente = self.request.GET.get("fuente")
        busqueda = self.request.GET.get("q")

        if fuente:
            queryset = queryset.filter(source__nombre=fuente)
        if busqueda:
            queryset = queryset.filter(titulo__icontains=busqueda)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fuentes"] = Source.objects.all()
        context["fuente_actual"] = self.request.GET.get("fuente", "")
        context["busqueda_actual"] = self.request.GET.get("q", "")
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"