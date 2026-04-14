from .base import BaseScraper
from playwright.sync_api import sync_playwright
from jobs.models import Job, Source

class PortalEmpleoScraper(BaseScraper):
    URL = "https://portalempleo.gob.ar/OfertasLaborales?provincia=ENTRE+RIOS&municipio=PARANA&page-number={}"

    def scrape(self):
        source, _ = Source.objects.get_or_create(
            nombre ="Portal Empleo",
            defaults={"url_base": "https://portalempleo.gob.ar/"})
        
        ofertas = self._fetch_ofertas()

        for oferta in ofertas:
            if oferta["titulo"] and oferta["url"]:
                try:
                    Job.objects.get_or_create(
                        url_original=oferta["url"],
                        defaults={
                            "titulo": oferta["titulo"],
                            "empresa": oferta["empresa"],
                            "ubicacion": "Paraná, Entre Ríos",
                            "source": source,
                        }
                    )
                    print(f"Guardado: {oferta['titulo']} - {oferta['empresa']}")
                except Exception as e:
                    print(f"Error al guardar {oferta['titulo']}: {e}")
    
    def _fetch_ofertas(self):
        resultados = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            pagina = 1

            while True:
                url = self.URL.format(pagina)
                page.goto(url, timeout=90000,   wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                botones = page.query_selector_all("a.comp-button-ciudadanos")

                if not botones:
                    break

                titulos = page.query_selector_all("h5.text-turqueza")
                empresas = page.query_selector_all("i.fa-building")

                for i, boton in enumerate(botones):
                    titulo = titulos[i].inner_text().strip() if i < len(titulos) else ""
                    empresa_icon = empresas[i] if i < len(empresas) else None   
                    empresa = ""
                    if empresa_icon:
                        parent = empresa_icon.evaluate("el => el.parentElement.innerText")
                        empresa = parent.strip()
                    
                    href = boton.get_attribute("href")
                    url = "https://portalempleo.gob.ar" + href if href else ""

                    resultados.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "url": url
                    })
                
                pagina += 1
            browser.close()
        return resultados
