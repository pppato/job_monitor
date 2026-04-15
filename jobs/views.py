from django.views.generic import ListView, DetailView
from .models import Job
# Create your views here.
class JobListView(ListView):
    model = Job
    template_name = "job_list.html"
    context_object_name = "jobs"
    queryset = Job.objects.all().order_by("score")

class JobDetailView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"