def predict_traffic(density):

    if density > 70:
        return "High Traffic Expected"
    elif density > 40:
        return "Moderate Traffic"
    else:
        return "Low Traffic"