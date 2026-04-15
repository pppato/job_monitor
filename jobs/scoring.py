from jobs.models import ScoringKeyWord


def calcular_score(titulo, descripcion=""):
    texto = (titulo + " " + descripcion).lower()
    keywords = ScoringKeyWord.objects.all()
    score = 0
    for kw in keywords:
        if kw.termino.lower() in texto:
            score += kw.peso
    return score