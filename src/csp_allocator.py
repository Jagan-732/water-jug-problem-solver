"""Small, explainable CSP allocator for a teaching/demo scenario.

All quantities are integer allocation units. In the demo, one unit = 10,000 litres.
The solver finds a feasible allocation that maximizes total allocation, then uses
zone priority as a tie-breaker. It does not claim to be a production water model.
"""
from dataclasses import dataclass
from time import perf_counter

@dataclass(frozen=True)
class Zone:
    name: str
    minimum: int
    demand: int
    pipeline_limit: int
    priority: int = 1
    is_hospital: bool = False

@dataclass
class SolveResult:
    allocation: dict
    feasible: bool
    nodes: int
    backtracks: int
    elapsed_ms: float
    propagation: bool
    objective: tuple | None
    message: str

def _validate(capacity, zones):
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("Reservoir capacity must be a non-negative integer.")
    if not zones:
        raise ValueError("Provide at least one zone.")
    names = [z.name for z in zones]
    if len(set(names)) != len(names):
        raise ValueError("Zone names must be unique.")
    for z in zones:
        if z.minimum < 0 or z.demand < z.minimum or z.pipeline_limit < 0:
            raise ValueError(f"Invalid demand/minimum/pipeline limit for {z.name}.")
        if z.priority < 1:
            raise ValueError(f"Priority for {z.name} must be at least 1.")

def solve_allocation(capacity, zones, propagation=True, heuristic=True):
    """Backtracking CSP with optional forward checking and MRV/LCV ordering."""
    _validate(capacity, zones)
    started = perf_counter()
    if sum(z.minimum for z in zones) > capacity:
        return SolveResult({}, False, 0, 0, (perf_counter()-started)*1000,
                           propagation, None,
                           "Infeasible: total minimum supply exceeds available reservoir water.")

    names = [z.name for z in zones]
    zone_by_name = {z.name: z for z in zones}
    domains = {
        z.name: list(range(z.minimum, min(z.demand, z.pipeline_limit) + 1))
        for z in zones
    }
    if any(not values for values in domains.values()):
        return SolveResult({}, False, 0, 0, (perf_counter()-started)*1000,
                           propagation, None, "Infeasible: a zone's minimum exceeds its limit.")

    nodes = 0
    backtracks = 0
    best_alloc = None
    best_objective = (-1, -1)

    def objective(assign):
        total = sum(assign.values())
        weighted_priority = sum(assign[n] * zone_by_name[n].priority for n in names)
        hospital_supply = sum(assign[n] for n in names if zone_by_name[n].is_hospital)
        # Total served first; priority-weighted service and hospital supply break ties.
        return (total, weighted_priority + hospital_supply * 100)

    def recurse(assign, current_domains):
        nonlocal nodes, backtracks, best_alloc, best_objective
        nodes += 1
        remaining = [n for n in names if n not in assign]
        used = sum(assign.values())
        if used > capacity:
            backtracks += 1
            return

        if not remaining:
            score = objective(assign)
            if score > best_objective:
                best_objective = score
                best_alloc = dict(assign)
            return

        # Optimistic bound: current assignment + maximum remaining domain values.
        upper_total = used + sum(max(current_domains[n]) for n in remaining)
        if best_alloc is not None and upper_total < best_objective[0]:
            return

        if heuristic:
            # MRV, then highest priority; LCV is approximated by descending values
            # because larger allocations serve more demand under this model.
            var = min(remaining, key=lambda n: (len(current_domains[n]),
                                                -zone_by_name[n].priority,
                                                n))
        else:
            var = remaining[0]

        values = sorted(current_domains[var], reverse=True) if heuristic else list(current_domains[var])
        for value in values:
            if used + value > capacity:
                continue
            new_assign = dict(assign)
            new_assign[var] = value
            new_domains = {n: list(v) for n, v in current_domains.items()}
            if propagation:
                remaining_capacity = capacity - sum(new_assign.values())
                for other in remaining:
                    if other == var:
                        continue
                    new_domains[other] = [
                        v for v in new_domains[other]
                        if v <= remaining_capacity
                    ]
                if any(not new_domains[n] for n in remaining if n != var):
                    backtracks += 1
                    continue
            recurse(new_assign, new_domains)
        # Count a failed branch if no value could be extended.
        if best_alloc is None:
            backtracks += 1

    recurse({}, domains)
    elapsed = (perf_counter() - started) * 1000
    if best_alloc is None:
        return SolveResult({}, False, nodes, backtracks, elapsed, propagation,
                           None, "No feasible allocation found.")
    return SolveResult(best_alloc, True, nodes, backtracks, elapsed, propagation,
                       best_objective, "Feasible allocation found.")

def demo_scenarios():
    zones = [
        Zone("Hospital Zone", minimum=3, demand=6, pipeline_limit=5, priority=5, is_hospital=True),
        Zone("Residential Zone", minimum=2, demand=7, pipeline_limit=6, priority=3),
        Zone("Commercial Zone", minimum=1, demand=5, pipeline_limit=4, priority=1),
    ]
    return {
        "normal": (13, zones),
        "drought": (8, zones),
    }
