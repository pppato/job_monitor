from .base import BaseScraper
from playwright.sync_api import sync_playwright
from jobs.models import Job, Source
from jobs.scoring import calcular_score

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
                            "source": source,
                            "score": calcular_score(oferta["titulo"])
                        }
                    )
                    print(f"Oferta '{oferta['titulo']} - {oferta['empresa']}' guardada.")
                except Exception as e:
                    print(f"Error al guardar la oferta '{oferta['titulo']} - {oferta['empresa']}': {e}")
                
    def _fetch_ofertas(self):
        resultados = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 768},
                locale="es-AR",
            )
            page = context.new_page()
            page.goto(self.URL, timeout = 60000, wait_until="domcontentloaded")
            try:
                page.wait_for_selector("a[href*='/empleos/']", timeout=60000)
            except Exception:
                page.screenshot(path="debug_zonajobs.png", full_page=True)
                with open("debug_zonajobs.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
                print("No se encontró el selector. Revisá debug_zonajobs.png y debug_zonajobs.html")
                browser.close()
                return resultados

            tarjetas = page.query_selector_all("a[href*='/empleos/']")

            for tarjeta in tarjetas:
                titulo_el = tarjeta.query_selector("h2")
                h3_elements = tarjeta.query_selector_all("h3")
                href = tarjeta.get_attribute("href")

                titulo = titulo_el.inner_text().strip() if titulo_el else ""
                empresa = h3_elements[1].inner_text().strip() if len(h3_elements) > 1 else ""
                url = href if href.startswith("http") else "https://www.zonajobs.com.ar" + href

                resultados.append({
                    "titulo": titulo,
                    "empresa": empresa,
                    "ubicacion": "Paraná, Entre Ríos",
                    "url": url
                })

            browser.close()
        return resultados