from src.csp_allocator import demo_scenarios, solve_allocation
from src.diagnosis_engine import diagnose
from src.fairness import fairness_report

def show_allocation(label, capacity, zones):
    print(f"\n=== {label.upper()} SCENARIO ===")
    result = solve_allocation(capacity, zones, propagation=True, heuristic=True)
    print(f"Available water: {capacity} units (1 unit = 10,000 litres)")
    if not result.feasible:
        print(result.message)
        return
    print("Allocation:")
    for zone in zones:
        value = result.allocation[zone.name]
        print(f"  {zone.name}: {value} units = {value * 10000:,} litres")
    print(f"Total allocated: {sum(result.allocation.values())} / {capacity} units")
    print(f"Search nodes: {result.nodes}; backtracks: {result.backtracks}; time: {result.elapsed_ms:.3f} ms")
    report = fairness_report(zones, result.allocation)
    print(f"All minimum supplies met: {report['all_minimums_met']}")
    for row in report["zones"]:
        print(f"  Audit: {row['zone']} | minimum met={row['minimum_met']} | reason={row['reason']}")

def compare_propagation(capacity, zones):
    print("\n=== PROPAGATION COMPARISON ===")
    for enabled in (False, True):
        result = solve_allocation(capacity, zones, propagation=enabled, heuristic=True)
        print(f"Propagation {'ON' if enabled else 'OFF'}: feasible={result.feasible}, "
              f"nodes={result.nodes}, backtracks={result.backtracks}, time={result.elapsed_ms:.3f} ms")

def main():
    scenarios = demo_scenarios()
    for name, (capacity, zones) in scenarios.items():
        show_allocation(name, capacity, zones)
    capacity, zones = scenarios["drought"]
    compare_propagation(capacity, zones)

    print("\n=== DIAGNOSIS TRACE ===")
    print("Evidence: pressure=low, flow=high (simulated sensor readings)")
    for item in diagnose("low", "high"):
        print(f"Rule: {item['rule']}")
        print(f"Conclusion: {item['conclusion']}")
        print(f"Certainty factor: {item['certainty_factor']:.2f}")
        print(f"Explanation: {item['explanation']}")

if __name__ == "__main__":
    main()
