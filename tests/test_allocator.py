from src.csp_allocator import Zone, solve_allocation, demo_scenarios

def test_normal_allocation_feasible():
    capacity, zones = demo_scenarios()["normal"]
    result = solve_allocation(capacity, zones, propagation=True)
    assert result.feasible
    assert sum(result.allocation.values()) <= capacity
    for zone in zones:
        assert result.allocation[zone.name] >= zone.minimum
        assert result.allocation[zone.name] <= min(zone.demand, zone.pipeline_limit)

def test_drought_allocation_feasible():
    capacity, zones = demo_scenarios()["drought"]
    result = solve_allocation(capacity, zones, propagation=True)
    assert result.feasible
    assert sum(result.allocation.values()) <= capacity

def test_infeasible_minimums():
    zones = [Zone("A", 3, 5, 5), Zone("B", 4, 5, 5)]
    result = solve_allocation(5, zones)
    assert not result.feasible
