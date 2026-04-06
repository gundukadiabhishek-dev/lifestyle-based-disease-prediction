def estimate_timeframe(prob):

    if prob < 0.3:
        return "5–10 years (low risk if lifestyle maintained)"

    elif prob < 0.6:
        return "2–5 years (moderate risk, improvement recommended)"

    elif prob < 0.8:
        return "6 months – 2 years (high risk developing)"

    else:
        return "Immediate to 6 months (critical risk)"