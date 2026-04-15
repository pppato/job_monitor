from jobs.models import ScoringKeyWord

positivas = ["vendedor", "ventas", "comercial", "comisiones", "asesor comercial", "ejecutivo de ventas", "promotor", "captacion", "cartera de clientes"]
negativas = ["desarrollador", "programador", "administrativo", "contador", "enfermero", "docente", "profesor", "ingeniero", "diseñador"]

for termino in positivas:
    ScoringKeyWord.objects.get_or_create(termino=termino, defaults={"peso": 10})

for termino in negativas:
    ScoringKeyWord.objects.get_or_create(termino=termino, defaults={"peso": -10})

print("Listo")