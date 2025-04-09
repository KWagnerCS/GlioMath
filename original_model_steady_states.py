import sympy as sp
import numpy as np
from tqdm import tqdm  # For progress bar

# Define symbolic variables with assumptions
T, sigma_brain, I, sigma_serum = sp.symbols('T sigma_brain I sigma_serum', real=True, positive=True)

# Define parameters
params = {
    "alpha_T": 1.575, # Growth rate of glioma
    "K_T": 2, # Carrying capacity of glioma
    "d_TI": 0.072, # Decay rate of glioma due to immune response
    "alpha_TI": 0.0003, # Recruitment rate of immune systems cells due to glioma
    "d_T": 0.0001, # Natural decay rate of glioma
    "d_I": 0.01, # Natural decay rate of immune system cells
    "alpha_s": 0.7, # Immune system cell recruitment rate
    "nu": 0.7, # Baseline immune system cell production rate
    "d_Tsigma": 1, # Glucose consumption rate by glioma
    "alpha_sigma": 20, # Transfer rate of glucose from serum to brain
    "sigma_min": 0.0008, # Minimum glucose intake rate to serum
    "sigma_0": 0.0016, # Maximum variation in glucose intake rate
    "d_sigma_1": 0.01, # Glucose consumption in brain by healthy cells (1)
    "d_sigma_2": 0.01, # Glucose consumption in brain by healthy cells (2)
    "d_TT": 0.72, # Rate of glioma cells killing immune cells
}

# Define F_steady as a constant (F(t) = sigma_min in steady-state)
F_steady = params["sigma_min"]

# Define steady-state equations
dT = params["alpha_T"] * sigma_brain * T * (1 - T / params["K_T"]) - params["d_T"] * T - params["d_TI"] * T * I
dsigma_brain = params["alpha_sigma"] * (sigma_serum - sigma_brain) - params["d_Tsigma"] * T * sigma_brain - (params["d_sigma_1"] + params["alpha_s"] * (params["nu"] + I)) * sigma_brain
dI = params["alpha_s"] * (params["nu"] + I) * sigma_brain + params["alpha_TI"] * T * I - params["d_I"] * I - params["d_TT"] * T * I
dsigma_serum = params["alpha_sigma"] * (sigma_brain - sigma_serum) + F_steady - params["d_sigma_2"] * sigma_serum

# List of numerical ranges to explore steady states
ranges = [
    (0, 2),  # T range
    (0, 1),  # sigma_brain range
    (0, 1),  # I range
    (0, 1),  # sigma_serum range
]

# Define grid for initial guesses
num_points = 8  # increase for more precision
grids = [np.linspace(start, end, num_points) for start, end in ranges]

# Solve with nsolve
steady_states = []
total_combinations = num_points ** len(ranges)

print("Solving steady states ...")
with tqdm(total=total_combinations, desc="Progress") as pbar:
    for T_val in grids[0]:
        for sigma_brain_val in grids[1]:
            for I_val in grids[2]:
                for sigma_serum_val in grids[3]:
                    try:
                        guess = (T_val, sigma_brain_val, I_val, sigma_serum_val)
                        sol = sp.nsolve(
                            [dT, dsigma_brain, dI, dsigma_serum], 
                            (T, sigma_brain, I, sigma_serum), 
                            guess
                        )
                        if not any(sp.simplify(sol - ss).norm() < 1e-4 for ss in steady_states):
                            steady_states.append(sol)
                    except Exception:
                        pass  # Ignore cases where nsolve fails
                    pbar.update(1)

# Print steady states
print("\nSteady States:")
if steady_states:
    for i, ss in enumerate(steady_states):
        print(f"Steady State {i + 1}:")
        for var, value in zip([T, sigma_brain, I, sigma_serum], ss):
            print(f"  {var} = {value.evalf()}")
        print("\n")
else:
    print("No steady states found.")
