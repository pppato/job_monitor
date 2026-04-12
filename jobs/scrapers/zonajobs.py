from .base import BaseScraper
from playwright.sync_api import sync_playwright
from jobs.models import Job, Source

class ZonaJobsScrapper(BaseScraper):

    URL = "https://www.zonajobs.com.ar/en-entre-rios/parana/empleos.html"

    def scrape(self):
        source, _ = Source.objects.get_or_create(nombre="ZonaJobs", defaults = {"url_base": "https://www.zonajobs.com.ar/"})

        ofertas = self._fetch_ofertas()

        for oferta in ofertas:
            if oferta["titulo"] and oferta["url"]:
                try:
                    Job.objects.get_or_create(
                        url_original=oferta["url"],
                        defaults={
                            "titulo": oferta["titulo"],
                            "empresa": oferta["empresa"],
                            "ubicacion": oferta["ubicacion"],
                            "source": source
                        }
                    )
                    print(f"Oferta '{oferta['titulo']} - {oferta['empresa']}' guardada.")
                except Exception as e:
                    print(f"Error al guardar la oferta '{oferta['titulo']} - {oferta['empresa']}': {e}")
                
    def _fetch_ofertas(self):
        resultados = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.URL, timeout = 60000, wait_until="domcontentloaded")
            page.wait_for_selector("a[href*='/empleos/']", timeout = 60000)

            tarjetas = page.query_selector_all("a[href*='/empleos/']")

            for tarjeta in tarjetas:
                titulo_el = tarjeta.query_selector("h2")
                empresa_el = tarjeta.query_selector("span h3")
                ubicacion_el = tarjeta.query_selector("i[aria-label='Ubicación'] + span h3")
                href = tarjeta.get_attribute("href")

                titulo = titulo_el.inner_text().strip() if titulo_el else ""
                empresa = empresa_el.inner_text().strip() if empresa_el else ""
                ubicacion = ubicacion_el.inner_text().strip() if ubicacion_el else ""
                url = "https://www.zonajobs.com.ar" + href if href else ""

                resultados.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": ubicacion,
                    "url": url
                })

            browser.close()
        return resultados

