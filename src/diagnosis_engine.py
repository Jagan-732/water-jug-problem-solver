"""Rule-based water network diagnosis with illustrative certainty factors."""

RULES = [
    {
        "name": "Possible leak",
        "conditions": {"pressure": "low", "flow": "high"},
        "conclusion": "Leak suspected",
        "certainty_factor": 0.80,
        "explanation": "Low pressure together with unusually high flow can indicate water escaping from the network."
    },
    {
        "name": "Possible supply shortage",
        "conditions": {"pressure": "low", "flow": "low"},
        "conclusion": "Supply shortage suspected",
        "certainty_factor": 0.75,
        "explanation": "Low pressure and low flow may indicate insufficient upstream supply or a restriction."
    },
    {
        "name": "Possible blockage",
        "conditions": {"pressure": "high", "flow": "low"},
        "conclusion": "Pipeline blockage suspected",
        "certainty_factor": 0.70,
        "explanation": "High upstream pressure with low downstream flow may indicate a restriction."
    },
]

def diagnose(pressure, flow):
    pressure, flow = pressure.lower().strip(), flow.lower().strip()
    if pressure not in {"low", "normal", "high"}:
        raise ValueError("Pressure must be low, normal, or high.")
    if flow not in {"low", "normal", "high"}:
        raise ValueError("Flow must be low, normal, or high.")
    evidence = {"pressure": pressure, "flow": flow}
    matches = []
    for rule in RULES:
        if all(evidence.get(k) == v for k, v in rule["conditions"].items()):
            matches.append({
                "rule": rule["name"],
                "conclusion": rule["conclusion"],
                "certainty_factor": rule["certainty_factor"],
                "explanation": rule["explanation"],
                "evidence": evidence.copy(),
            })
    if not matches:
        matches.append({
            "rule": "No specific rule matched",
            "conclusion": "No clear fault inferred",
            "certainty_factor": 0.40,
            "explanation": "The selected evidence does not match a defined fault pattern. More sensor readings are needed.",
            "evidence": evidence.copy(),
        })
    return matches
