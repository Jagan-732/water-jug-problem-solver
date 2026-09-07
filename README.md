# Water Jug Problem Solver

## Problem Statement

The Water Jug Problem is a state-space search problem.

Given two water jugs with fixed capacities, the objective is to measure a target amount of water using the following operations:

- Fill a jug completely.
- Empty a jug completely.
- Pour water from one jug into the other until either the source jug is empty or the destination jug is full.

The program finds a sequence of operations that reaches the target volume.

## Approach

This project uses Breadth-First Search (BFS).

Each state is represented as:

```text
(a, b)