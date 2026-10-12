from collections import deque

def validate_inputs(jug_a, jug_b, target):
    if not all(isinstance(x, int) for x in (jug_a, jug_b, target)):
        raise ValueError("Capacities and target must be integers.")
    if jug_a <= 0 or jug_b <= 0:
        raise ValueError("Jug capacities must be positive.")
    if target < 0 or target > max(jug_a, jug_b):
        raise ValueError("Target must be between 0 and the larger jug capacity.")

def get_next_states(state, jug_a, jug_b):
    a, b = state
    candidates = [
        ((jug_a, b), "Fill Jug A"),
        ((a, jug_b), "Fill Jug B"),
        ((0, b), "Empty Jug A"),
        ((a, 0), "Empty Jug B"),
        ((a - min(a, jug_b - b), b + min(a, jug_b - b)), "Pour A -> B"),
        ((a + min(b, jug_a - a), b - min(b, jug_a - a)), "Pour B -> A"),
    ]
    # Remove no-op transitions while preserving action order.
    result, seen = [], set()
    for next_state, action in candidates:
        if next_state != state and next_state not in seen:
            result.append((next_state, action))
            seen.add(next_state)
    return result

def water_jug_search(jug_a, jug_b, target, strategy="bfs"):
    validate_inputs(jug_a, jug_b, target)
    if target == 0:
        return {"path": [((0, 0), None)], "expanded": 0, "generated": 1, "strategy": strategy}
    if target > jug_a and target > jug_b:
        return None
    if strategy.lower() not in ("bfs", "dfs"):
        raise ValueError("strategy must be 'bfs' or 'dfs'")

    start = (0, 0)
    frontier = deque([start])
    visited = {start}
    parent = {start: None}
    action = {start: None}
    expanded = 0
    generated = 1

    while frontier:
        current = frontier.popleft() if strategy.lower() == "bfs" else frontier.pop()
        if current[0] == target or current[1] == target:
            path = []
            node = current
            while node is not None:
                path.append((node, action[node]))
                node = parent[node]
            path.reverse()
            return {"path": path, "expanded": expanded, "generated": generated, "strategy": strategy.lower()}
        expanded += 1
        next_states = get_next_states(current, jug_a, jug_b)
        if strategy.lower() == "dfs":
            next_states = list(reversed(next_states))
        for next_state, operation in next_states:
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = current
                action[next_state] = operation
                frontier.append(next_state)
                generated += 1
    return None

def water_jug_bfs(jug_a, jug_b, target):
    """Backward-compatible function returning the original list path or None."""
    result = water_jug_search(jug_a, jug_b, target, "bfs")
    return None if result is None else result["path"]

def main():
    try:
        jug_a = int(input("Enter capacity of Jug A: "))
        jug_b = int(input("Enter capacity of Jug B: "))
        target = int(input("Enter target volume: "))
        result = water_jug_search(jug_a, jug_b, target, "bfs")
        if result is None:
            print("\nNo solution exists for these capacities and target.")
            return
        print("\nBFS Solution Found!")
        for i, (state, operation) in enumerate(result["path"]):
            print(f"{'Start' if operation is None else f'{i}. {operation}'}: {state}")
        print(f"\nStates expanded: {result['expanded']}")
        print(f"States generated: {result['generated']}")
    except ValueError as exc:
        print(f"Input error: {exc}")

if __name__ == "__main__":
    main()
