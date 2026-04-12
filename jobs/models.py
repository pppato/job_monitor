from django.db import models

class Source(models.Model):
    nombre = models.CharField(max_length=100)
    url_base = models.URLField()

    def __str__(self):
        return self.nombre


class Category(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Technology(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Job(models.Model):
    titulo = models.CharField(max_length=500)
    empresa = models.CharField(max_length=500)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=500, blank=True)
    url_original = models.URLField(max_length=500)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_scraping = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.titulo} — {self.empresa}"


class JobTechnology(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'technology')

    def __str__(self):
        return f"{self.job} — {self.technology}"
