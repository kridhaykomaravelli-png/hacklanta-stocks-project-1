def score_stock(info, hist):
    score = 0
    reasons = []

    current_price = hist["Close"].iloc[-1]
    avg_price = hist["Close"].mean()

    pe_ratio = info.get("trailingPE")
    revenue_growth = info.get("revenueGrowth")
    debt_to_equity = info.get("debtToEquity")

    
    if current_price > avg_price:
        score += 1
        reasons.append("Price is above its average for the selected period.")
    else:
        reasons.append("Price is below its average for the selected period.")

    if pe_ratio is not None:
        if pe_ratio < 25:
            score += 1
            reasons.append("P/E ratio looks reasonable.")
        else:
            reasons.append("P/E ratio is high.")
    else:
        reasons.append("P/E ratio is unavailable.")

    if revenue_growth is not None:
        if revenue_growth > 0.10:
            score += 1
            reasons.append("Revenue growth is strong.")
        else:
            reasons.append("Revenue growth is weak.")
    else:
        reasons.append("Revenue growth is unavailable.")

    if debt_to_equity is not None:
        if debt_to_equity < 100:
            score += 1
            reasons.append("Debt level is moderate.")
        else:
            reasons.append("Debt level is high.")
    else:
        reasons.append("Debt data is unavailable.")

    if score >= 3:
        label = "Good candidate"
    elif score == 2:
        label = "Watch carefully"
    else:
        label = "Risky"

    return {
        "score": score,
        "label": label,
        "reasons": reasons
    }


def score_index_fund(info, hist):
    score = 0
    reasons = []

    current_price = hist["Close"].iloc[-1]
    avg_price = hist["Close"].mean()

    ma_50 = hist["Close"].tail(50).mean() if len(hist) >= 50 else hist["Close"].mean()

    if current_price > avg_price:
        score += 1
        reasons.append("Price is above its average for the selected period.")
    else:
        reasons.append("Price is below its average for the selected period.")

    if current_price > ma_50:
        score += 1
        reasons.append("Price is above its 50-day average.")
    else:
        reasons.append("Price is below its 50-day average.")

    volume = info.get("volume")
    if volume is not None:
        if volume > 1000000:
            score += 1
            reasons.append("Trading volume is healthy.")
        else:
            reasons.append("Trading volume is lower than ideal.")
    else:
        reasons.append("Trading volume is unavailable.")

    expense_ratio = (
        info.get("annualReportExpenseRatio")
        or info.get("netExpenseRatio")
        or info.get("expenseRatio")
    )

    if expense_ratio is not None:
        if expense_ratio < 0.005:
            score += 1
            reasons.append("Expense ratio is low.")
        else:
            reasons.append("Expense ratio is a bit high.")
    else:
        reasons.append("Expense ratio is unavailable.")

    if score >= 3:
        label = "Good candidate"
    elif score == 2:
        label = "Watch carefully"
    else:
        label = "Risky"

    return {
        "score": score,
        "label": label,
        "reasons": reasons
    }
