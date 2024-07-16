# Trade Credit Market Payment System Balancer

This project implements a system to balance payments in the trade credit market, which is recreating the paper- [*Mathematical Foundations for Balancing the Payment System*](https://www.mdpi.com/1911-8074/14/9/452). 
in the Trade Credit Market It provides a framework for simulating different scenarios and optimizing debt networks among companies.

## Project Structure

- `company.py`: Defines the `Company` and `DebtNetwork` classes for managing (Add, delete, check and change.) companies and their debt relationships.
- `optimizer.py`: Implements for optimizing debt cycles in the network.
- `calculations.py`: Provides various methods for calculating financial metrics and parameters based on the debt network.
- `scenario.py`: Defines different scenarios for initializing the debt network with sample data.
- `visualize.py`: Contains functions for visualizing the debt network.
- `main.py`: The main script to run different scenarios, perform calculations, optimize the network, and visualize the results.


`bash

python main.py


## Project Explain
- `company.py`:  In this part, [`uuid`](https://docs.python.org/3/library/uuid.html) (`uuid4`) is used to ensure the universally unique identifiers of the company.

