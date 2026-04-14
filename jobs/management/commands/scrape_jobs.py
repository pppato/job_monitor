from django.core.management.base import BaseCommand
from jobs.scrapers.computrabajo import ComputrabajoScraper
from jobs.scrapers.zonajobs import ZonaJobsScrapper
from jobs.scrapers.portal_empleo import PortalEmpleoScraper

class Command(BaseCommand):
    help = 'Scrapea ofertas laborales de todas las fuentes'

    def handle(self, *args, **options):
        scrapers = [
           #ComputrabajoScraper(),
           #ZonaJobsScrapper(),
            PortalEmpleoScraper()
        ]
        print(f"Scrapers a ejecutar: {scrapers}")
        for scraper in scrapers:
            self.stdout.write(f'Ejecutando {scraper.__class__.__name__}...')
            scraper.scrape()
            self.stdout.write(self.style.SUCCESS(f'{scraper.__class__.__name__} finalizado.'))