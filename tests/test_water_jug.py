from src.water_jug_solver import water_jug_bfs


def test_4_3_target_2():
    solution = water_jug_bfs(4, 3, 2)

    assert solution is not None

    final_state = solution[-1][0]

    assert final_state[0] == 2 or final_state[1] == 2


def test_3_5_target_4():
    solution = water_jug_bfs(3, 5, 4)

    assert solution is not None

    final_state = solution[-1][0]

    assert final_state[0] == 4 or final_state[1] == 4


def test_impossible_target():
    solution = water_jug_bfs(2, 4, 3)

    assert solution is None