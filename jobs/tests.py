from django.test import TestCase
from django.urls import reverse
from .models import Source, Category, Job, ScoringKeyWord
from .scoring import calcular_score


class SourceModelTest(TestCase):
    def test_str_devuelve_nombre(self):
        source = Source.objects.create(nombre="Computrabajo", url_base="https://ar.computrabajo.com")
        self.assertEqual(str(source), "Computrabajo")


class JobModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(nombre="ZonaJobs", url_base="https://zonajobs.com.ar")
        self.category = Category.objects.create(nombre="Backend")
        self.job = Job.objects.create(
            titulo="Desarrollador Django Jr",
            empresa="Empresa Test",
            url_original="https://zonajobs.com.ar/empleo/1",
            source=self.source,
            category=self.category,
        )

    def test_str_devuelve_titulo_y_empresa(self):
        self.assertEqual(str(self.job), "Desarrollador Django Jr — Empresa Test")

    def test_borrar_source_borra_el_job_en_cascada(self):
        self.source.delete()
        self.assertEqual(Job.objects.count(), 0)

    def test_borrar_category_deja_job_sin_categoria(self):
        self.category.delete()
        self.job.refresh_from_db()
        self.assertIsNone(self.job.category)


class ScoringTest(TestCase):
    def test_calcular_score_suma_pesos_de_keywords_encontradas(self):
        ScoringKeyWord.objects.create(termino="django", peso=10)
        ScoringKeyWord.objects.create(termino="python", peso=5)
        ScoringKeyWord.objects.create(termino="java", peso=3)

        score = calcular_score("Desarrollador Python y Django Jr")

        self.assertEqual(score, 15)

    def test_calcular_score_sin_keywords_es_cero(self):
        score = calcular_score("Vendedor de electrodomésticos")
        self.assertEqual(score, 0)


class JobListViewTest(TestCase):
    def setUp(self):
        self.source_a = Source.objects.create(nombre="Computrabajo", url_base="https://a.com")
        self.source_b = Source.objects.create(nombre="ZonaJobs", url_base="https://b.com")

        Job.objects.create(
            titulo="Desarrollador Django", empresa="Empresa A",
            url_original="https://a.com/1", source=self.source_a,
        )
        Job.objects.create(
            titulo="Analista Funcional", empresa="Empresa B",
            url_original="https://b.com/1", source=self.source_b,
        )

    def test_lista_devuelve_200(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)

    def test_lista_muestra_todos_los_jobs_sin_filtro(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(len(response.context["jobs"]), 2)

    def test_filtro_por_fuente(self):
        response = self.client.get(reverse("job_list"), {"fuente": "Computrabajo"})
        jobs = response.context["jobs"]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].empresa, "Empresa A")

    def test_busqueda_por_titulo(self):
        response = self.client.get(reverse("job_list"), {"q": "django"})
        jobs = response.context["jobs"]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].titulo, "Desarrollador Django")


class JobDetailViewTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(nombre="Computrabajo", url_base="https://a.com")
        self.job = Job.objects.create(
            titulo="Desarrollador Django", empresa="Empresa A",
            url_original="https://a.com/1", source=self.source,
        )

    def test_detalle_devuelve_200(self):
        response = self.client.get(reverse("job_detail", args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detalle_inexistente_devuelve_404(self):
        response = self.client.get(reverse("job_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)