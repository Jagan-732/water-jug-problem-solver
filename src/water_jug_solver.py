from collections import deque


def get_next_states(state, jug_a, jug_b):
    a, b = state
    states = []

    states.append(((jug_a, b), "Fill Jug A"))
    states.append(((a, jug_b), "Fill Jug B"))
    states.append(((0, b), "Empty Jug A"))
    states.append(((a, 0), "Empty Jug B"))

    # Pour A -> B
    amount = min(a, jug_b - b)
    states.append(((a - amount, b + amount), "Pour A -> B"))

    # Pour B -> A
    amount = min(b, jug_a - a)
    states.append(((a + amount, b - amount), "Pour B -> A"))

    return states


def water_jug_bfs(jug_a, jug_b, target):
    start = (0, 0)

    queue = deque([start])
    visited = {start}

    parent = {start: None}
    action = {start: None}

    while queue:
        current = queue.popleft()

        if current[0] == target or current[1] == target:
            path = []

            while current is not None:
                path.append((current, action[current]))
                current = parent[current]

            path.reverse()
            return path

        for next_state, operation in get_next_states(
            current, jug_a, jug_b
        ):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = current
                action[next_state] = operation
                queue.append(next_state)

    return None


def main():
    # User input
    jug_a = int(input("Enter capacity of Jug A: "))
    jug_b = int(input("Enter capacity of Jug B: "))
    target = int(input("Enter target volume: "))

    # Solve using BFS
    solution = water_jug_bfs(jug_a, jug_b, target)

    # Display result
    if solution:
        print("\nSolution Found!\n")

        for i, (state, operation) in enumerate(solution):
            if operation:
                print(f"{i}. {operation}")
                print(f"   State: {state}")
            else:
                print(f"Start State: {state}")
    else:
        print("\nNo solution exists.")


if __name__ == "__main__":
    main()