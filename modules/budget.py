def compare_budget(category_spend, budget):
    result = {}
    for cat, limit in budget.items():
        spent = category_spend.get(cat, 0)
        result[cat] = {
            "spent": spent,
            "remaining": limit - spent
        }
    return result