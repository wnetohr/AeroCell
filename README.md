# Aerocell: Aerosol Propagation Simulator

## Access the application

Use the deployed site to try the app directly in your browser:
https://aerocell-wnetohr.streamlit.app/

## Overview

Aerocell is a simulator designed to model the propagation of aerosols in enclosed environments using cellular automata concepts. It provides realistic simulations of how respiratory diseases spread in confined spaces, helping researchers and professionals understand transmission dynamics and evaluate mitigation strategies.

## Project Description

This project simulates aerosol transmission in closed environments by leveraging cellular automata theory. It models the spatial and temporal dynamics of disease transmission in indoor settings, enabling analysis of factors that influence respiratory disease spread.

## Key Features

- **Cellular Automata-based simulation** - Models aerosol propagation using discrete grid-based rules
- **Enclosed environment modeling** - Simulates realistic indoor scenarios
- **Disease transmission analysis** - Tracks how respiratory diseases spread through aerosol particles
- **Customizable parameters** - Adjust environment conditions and transmission factors

## Getting Started

Follow the steps below to set up the environment and run AeroCell on your local machine.

#### **Prerequisites**
* Python 3.8 or higher installed.
* `pip` package manager.

#### **Step-by-Step**

1.  **Clone the repository or download the files:**
    Ensure that `main.py`, `engine.py`, and `requirements.txt` are in the same directory.

2.  **Install dependencies:**
    Open the terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    In the terminal, use the Streamlit command:
    ```bash
    streamlit run main.py
    ```

4.  **Access in Browser:**
    The application will automatically open in your default browser at `http://localhost:8501`.

## 🧠 How Does the Diffusion Logic Work?

The propagation of particles in **AeroCell** does not use complex loops for each cell, but rather a mathematical model of **Cellular Automata** based on fluid physics. The central idea is that air tends toward equilibrium: areas with high concentration "donate" particles to neighboring areas with lower concentration.

### The Transition Rule

At each simulation step (frame), the new value of a cell is calculated by the following formula:

$$\phi_{new} = (\phi_{current} \cdot (1 - \alpha)) + (\bar{\phi}_{neighbors} \cdot \alpha)$$

Where:
* **$\phi_{current}$**: The amount of aerosol that the cell contains at the moment.
* **$\alpha$ (Diffusion Rate)**: A coefficient between 0 and 1 that defines the speed of spreading.
* **$\bar{\phi}_{neighbors}$**: The average concentration of neighboring cells (Von Neumann Neighborhood).

### In practice, this means that:

1.  **Inertia:** If we set diffusion to $0.2$, the cell preserves $80\%$ ($1 - 0.2$) of its current content. This represents the resistance of the air mass to instantaneous movement.
2.  **Interaction:** The cell absorbs $20\%$ of the average concentration around it. If the neighbors are saturated, the cell tends to equalize its concentration with them.
3.  **Visual Realism:** This calculation results in smooth radial dissipation, simulating the real behavior of gases and vapors in enclosed environments.

### Optimization with NumPy

To ensure the simulation runs in real-time on **Streamlit**, AeroCell uses **matrix vectorization**. Instead of iterating over each cell individually (which would be computationally expensive in Python), we shift the entire data matrix in four directions using the `np.roll()` function. 

This allows the processor to execute mathematical operations in blocks, ensuring high performance even on high-resolution grids.

## 📉 Decay Mechanism

In a realistic simulation, aerosol particles do not remain suspended forever. **AeroCell** implements a decay factor to simulate physical phenomena such as sedimentation (particles falling to the ground) and natural dissipation of viral load in the environment.

### The Decay Equation

After calculating the diffusion, we apply a linear reduction in the concentration of each cell through the following formula:

$$\phi_{final} = \phi_{new} \cdot (1 - \delta)$$

Where:
* **$\phi_{final}$**: The final concentration value after all frame losses.
* **$\phi_{new}$**: The value resulting from the diffusion calculation.
* **$\delta$ (Decay Rate)**: A coefficient (usually very small, ex: 0.005) that defines the percentage of loss per cycle.

### Why is Decay Important?

1.  **Sedimentation:** Aerosol particles are influenced by gravity and eventually deposit on surfaces.
2.  **Viral Inactivation:** In the context of pathogens like SARS-CoV-2 or Influenza, the virus loses its infectious capacity over time due to environmental factors (humidity, temperature, UV radiation).
3.  **Simulation Stability:** Mathematically, decay prevents particle concentration from accumulating infinitely in the system, ensuring that the environment eventually returns to "clean air" if the emission source is interrupted.

### Vectorized Implementation

In the code, this operation is performed in a single line for the entire grid:

```python
self.grid *= (1 - self.decay)
```

## 🧱 Obstacle and Collision System

To simulate real-world environments (rooms, offices, or workspaces), **AeroCell** uses a boolean mask system to define physical barriers. Obstacles are treated as regions of "zero capacity," where aerosol concentration is null and particle passage is blocked.

### Matrix Mask Logic

Unlike traditional collision systems based on vectors, AeroCell uses matrix algebra to apply physical constraints in real-time:

$$\phi_{final} = \phi_{calculated} \odot (1 - M_{obstacles})$$

Where:
* **$M_{obstacles}$**: A binary matrix of the same dimension as the grid, where $1$ represents an obstacle and $0$ represents free space.
* **$\odot$**: Represents the Hadamard product (element-wise multiplication).

### Why use masks?

1. **Performance:** Allows the simulator to calculate collisions for millions of cells simultaneously, without the need to check each particle individually.
2. **Scenario Complexity:** With this approach, it's possible to draw any environment layout (walls, tables, dividers) simply by changing the values in the obstacle matrix.
3. **Realism:** Barriers force the aerosol "cloud" to navigate around objects, faithfully simulating how air behaves in corners and narrow corridors.




