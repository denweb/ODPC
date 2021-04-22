def calc_score(metriken):
    """
    Hilfsfunktion zum berechnen der erreichten Punktzahl in einer Dimension
    :param metriken: Ein Dictionary mit den einzelnen Metriken und deren bestimmter Werte.
    :return: Die erreichte Gesamtpunktzahl aus allen Metriken in einer Dimension als Float.
    """
    score = sum(list(metriken.values()))

    return score
