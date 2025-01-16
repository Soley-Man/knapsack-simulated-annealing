# knapsack-simulated-annealing
This project is an introductory exercise to simulated annealing. To learn the basic structure of this type of algorithms I coded a SA algorithm from scratch to solve the 0/1 knapsack problem.

## The Knapsack Problem
Every item in the problem has a value, weight, and volume. An item's value can range from 1$ to 5$, its weight from 1kg to 7kg, and its volume from 1L to 6L, all with incremental steps of 1 unit. The knapsack can only carry 16kg and has a capacity of 13L.

The items data is stored in knapsack_items.csv. The items used in this project are a duplicate of those in my other repository 'knapsack-ga', where I built a genetic algorithm to solve the knapsack problem. Like this we can compare performance across the two types of algorithm.