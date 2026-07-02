from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Source, Category, Job


class JobAPITest(APITestCase):
    def setUp(self):
        self.source_a = Source.objects.create(nombre="Computrabajo", url_base="https://a.com")
        self.source_b = Source.objects.create(nombre="ZonaJobs", url_base="https://b.com")
        self.category = Category.objects.create(nombre="Backend")

        Job.objects.create(
            titulo="Desarrollador Django Jr", empresa="Empresa A",
            url_original="https://a.com/1", source=self.source_a, category=self.category,
        )
        Job.objects.create(
            titulo="Analista Funcional", empresa="Empresa B",
            url_original="https://b.com/1", source=self.source_b,
        )

    def test_listado_devuelve_200(self):
        response = self.client.get("/api/jobs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listado_devuelve_dos_jobs(self):
        response = self.client.get("/api/jobs/")
        self.assertEqual(response.data["count"], 2)

    def test_filtro_por_fuente(self):
        response = self.client.get("/api/jobs/", {"fuente": "computrabajo"})
        resultados = response.data["results"]
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["empresa"], "Empresa A")

    def test_busqueda_por_titulo(self):
        response = self.client.get("/api/jobs/", {"q": "django"})
        resultados = response.data["results"]
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["titulo"], "Desarrollador Django Jr")

    def test_source_viene_anidado_en_la_respuesta(self):
        response = self.client.get("/api/jobs/", {"q": "django"})
        job = response.data["results"][0]
        self.assertEqual(job["source"]["nombre"], "Computrabajo")

    def test_detalle_de_job_inexistente_devuelve_404(self):
        response = self.client.get("/api/jobs/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobAPIPermissionsTest(APITestCase):
    def setUp(self):
        self.source = Source.objects.create(nombre="Computrabajo", url_base="https://a.com")
        self.job = Job.objects.create(
            titulo="Desarrollador Django Jr", empresa="Empresa A",
            url_original="https://a.com/1", source=self.source,
        )
        self.user = User.objects.create_user(username="patricio", password="claveSegura123")

    def test_lectura_no_requiere_login(self):
        response = self.client.get("/api/jobs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_usuario_logueado_puede_acceder_igual(self):
        self.client.login(username="patricio", password="claveSegura123")
        response = self.client.get("/api/jobs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)