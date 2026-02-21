def evaluate_vendor(vendor_data, requirement):

    score = 0
    total = 0
    results = {}

    for field in requirement["fields"]:
        name = field["name"]
        if name not in vendor_data:
            continue

        total += 1

        required_value = requirement.get(name)
        vendor_value = vendor_data.get(name)

        if isinstance(required_value, (int, float)):
            passed = vendor_value >= required_value
        else:
            passed = vendor_value == required_value
        results[name] = passed
        if passed:
            score += 1

    compliance = score / total if total else 0

    return {
        "score": score,
        "total": total,
        "compliance": compliance,
        "details": results
    }
