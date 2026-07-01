# Job Monitor

Agregador de ofertas laborales para Paraná, Entre Ríos. Centraliza en un solo lugar las publicaciones de varios portales de empleo, evitando tener que revisar cada sitio por separado.

## ¿Qué hace?

El sistema recorre periódicamente distintos portales de empleo, extrae las ofertas nuevas y las guarda en una base de datos propia. Desde una interfaz web simple se pueden listar, buscar y filtrar todas las ofertas encontradas, cada una con un **score** calculado según palabras clave relevantes (por ejemplo, tecnologías buscadas).

**Fuentes actualmente soportadas:**
- Computrabajo
- ZonaJobs
- Portal Empleo (portalempleo.gob.ar)

## Stack

- **Backend:** Django
- **Base de datos:** PostgreSQL
- **Scraping:** Playwright
- **Frontend:** Templates de Django + Bootstrap 5
- **Deploy (planeado):** Railway

## Arquitectura

El scraping está resuelto con el **patrón Strategy**: cada fuente implementa una clase propia (`ComputrabajoScraper`, `ZonaJobsScrapper`, `PortalEmpleoScraper`) que hereda de `BaseScraper` y define su propio método `scrape()`. Esto permite agregar una fuente nueva sin tocar el código de las demás — solo hay que escribir la clase nueva y sumarla al comando de gestión.

```
jobs/
├── models.py              # Source, Category, Technology, Job, JobTechnology, ScoringKeyWord
├── scoring.py              # Cálculo de score por palabras clave
├── scrapers/
│   ├── base.py             # BaseScraper (clase abstracta)
│   ├── computrabajo.py
│   ├── zonajobs.py
│   └── portal_empleo.py
├── management/commands/
│   └── scrape_jobs.py       # Orquesta todos los scrapers
├── views.py                 # Listado (con filtro y búsqueda) y detalle de ofertas
├── admin.py                 # Panel de administración
└── tests.py
```

### Modelo de datos

- `Source`: portal de origen de la oferta (Computrabajo, ZonaJobs, etc.)
- `Category`: categoría opcional de la oferta
- `Technology`: tecnologías relacionadas a una oferta
- `Job`: la oferta laboral en sí, vinculada a `Source` y `Category`
- `JobTechnology`: tabla intermedia para la relación muchos a muchos entre `Job` y `Technology`
- `ScoringKeyWord`: palabras clave con un peso asociado, usadas para calcular el `score` de cada oferta

## Instalación local

**Requisitos:** Python 3.13, PostgreSQL corriendo localmente.

```bash
# Clonar el repo
git clone https://github.com/pppato/job_monitor.git
cd job_monitor

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
playwright install chromium

# Configurar base de datos
# Crear una base PostgreSQL llamada "job_monitor_db" (usuario/password según tu instalación local)

# Migraciones
python manage.py migrate

# Crear superusuario para acceder al admin
python manage.py createsuperuser

# Levantar el servidor
python manage.py runserver
```

La app queda disponible en `http://127.0.0.1:8000/` y el panel de administración en `http://127.0.0.1:8000/admin/`.

## Uso

**Ejecutar el scraping de todas las fuentes:**
```bash
python manage.py scrape_jobs
```

**Cargar palabras clave de scoring:**
Desde el admin (`/admin/`), agregar registros de `ScoringKeyWord` con un término y un peso. El score de cada oferta se recalcula sumando los pesos de las palabras clave que aparecen en su título/descripción.

**Correr los tests:**
```bash
python manage.py test jobs
```

## Roadmap

- [x] **Etapa 1** — Django clásico, scraping con Playwright, listado y filtro de ofertas, admin, tests
- [ ] **Etapa 2** — Exponer la API con Django REST Framework
- [ ] **Etapa 3** — Frontend en React
- [ ] Deploy en Railway

## Autor

Patricio De María — [github.com/pppato](https://github.com/pppato)
