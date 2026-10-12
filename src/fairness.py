"""Basic transparency and minimum-supply checks for the demo allocator."""

def fairness_report(zones, allocation):
    rows = []
    for zone in zones:
        amount = allocation.get(zone.name, 0)
        rows.append({
            "zone": zone.name,
            "allocated_units": amount,
            "minimum_units": zone.minimum,
            "demand_units": zone.demand,
            "priority": zone.priority,
            "minimum_met": amount >= zone.minimum,
            "demand_met": amount >= zone.demand,
            "reason": (
                "Hospital priority" if zone.is_hospital else
                "Higher service priority" if zone.priority >= 3 else
                "Standard priority"
            ),
        })
    return {
        "all_minimums_met": all(row["minimum_met"] for row in rows),
        "zones": rows,
        "note": "Priority is a transparent policy choice. Review it with stakeholders; it is not a substitute for real municipal policy."
    }
