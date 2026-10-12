# Water Jug Solver → Smart City Water Allocation System (v2.0)

This project preserves the original Water Jug BFS solver and extends it with an educational Smart City water allocation demonstration.

## Features
- Water jug state transitions and BFS/DFS search support.
- CSP-style water allocation using backtracking, optional forward checking, and MRV/value ordering.
- Normal and drought scenarios.
- Rule-based leak/shortage diagnosis with illustrative certainty factors.
- Minimum-supply and allocation audit report.
- Search statistics and propagation comparison.

## Run
Requires Python 3.10+.

```bash
python app.py
```

Run tests:

```bash
pip install -r requirements.txt
python -m pytest -q
```

Run the original water-jug program:

```bash
python -m src.water_jug_solver
```

## Units and assumptions
The allocation demonstration uses integer units; one unit represents 10,000 litres. Scenario values and sensor readings are simulated for teaching. They are not real municipal sensor data or operational recommendations.

The allocator maximizes total served demand, then uses a priority-weighted score as a tie-breaker. Real deployments require approved policies, validated data, safety review and stakeholder oversight. Certainty factors are illustrative confidence values, not calibrated probabilities.

## Repository layout
- `src/water_jug_solver.py`: original state-space problem, enhanced with BFS/DFS statistics and validation.
- `src/csp_allocator.py`: allocation CSP and demo scenarios.
- `src/diagnosis_engine.py`: explainable rule-based diagnosis.
- `src/fairness.py`: minimum-supply checks and audit output.
- `app.py`: terminal demonstration runner.
- `tests/`: automated tests.

## Final demonstration checklist
1. Show BFS state transitions and ordered solution steps.
2. Show normal and drought allocation scenarios.
3. Compare propagation on/off using nodes, backtracks and runtime.
4. Show one diagnosis trace with simulated sensor evidence.
5. Explain fairness assumptions and limitations.
