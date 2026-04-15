from .base import BaseScraper
from playwright.sync_api import sync_playwright
from jobs.models import Job, Source
from jobs.scoring import calcular_score

class ComputrabajoScraper(BaseScraper):
    URL = "https://ar.computrabajo.com/empleos-en-entre-rios-en-parana"
    def scrape(self):
        source, _ = Source.objects.get_or_create(
            nombre="Computrabajo",
            defaults={"url_base": "https://ar.computrabajo.com"}
        )

        ofertas = self.fetch_ofertas()

        for oferta in ofertas:
            if oferta["titulo"] and oferta["url"]:
                try:
                    Job.objects.get_or_create(
                        url_original=oferta["url"],
                        defaults={
                            "titulo": oferta["titulo"],
                            "empresa": oferta["empresa"],
                            "descripcion": oferta["descripcion"],
                            "ubicacion": oferta["ubicacion"],
                            "source": source,
                            "score": calcular_score(oferta["titulo"])
                        }
                    )
                    print(f"Guardado: {oferta['titulo']} - {oferta['empresa']}")
                except Exception as e:
                    print(f"Error al guardar {oferta['titulo']}: {e}")

    def fetch_ofertas(self):
        resultados = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.URL, timeout = 60000)
            page.wait_for_selector(".box_offer")

            ofertas = page.query_selector_all(".box_offer")

            for oferta in ofertas:
                titulo_el = oferta.query_selector("h2.fs18")
                empresa_el = oferta.query_selector(".fc_base.t_ellipsis")
                url_el = oferta.query_selector("h2.fs18 a")

                titulo = titulo_el.inner_text() if titulo_el else ""
                empresa = empresa_el.inner_text() if empresa_el else ""
                href = url_el.get_attribute("href") if url_el else ""
                url = "https://ar.computrabajo.com" + href if href else ""

                resultados.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": "Paraná, Entre Ríos",
                    "url": url,
                    "descripcion": "",
                })
            browser.close()
        return resultados

