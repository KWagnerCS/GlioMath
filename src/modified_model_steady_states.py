import sympy as sp
import numpy as np
from tqdm import tqdm  # For progress bar

# Define symbolic variables with assumptions
T, sigma_brain, C_t, T_beta, sigma_serum = sp.symbols('T sigma_brain C_t T_beta sigma_serum', real=True, positive=True)

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

    # Added parameters
    "a_2": 0, # Ranges from 0-0.5 # antigenicity of glioma (tumor)
    "k_5": 2000, # inhibitory parameter
    "mu_1": 0.0074, # natural death of CD8+ T cells
    "alpha_4": 0.1694, # death rate of CD8+ T Cells
    "k_3": 334452, # half saturation constant
    "s_1": 63305, # constant source of TGF-β (modified from 63305)
    "b_1": 0.0000057, # release rate per glioma cell
    "mu_2": 6.93, # natural death of TGF-β (modified from 6.93)
}

# Define F_steady as a constant (F(t) = sigma_min in steady-state)
F_steady = params["sigma_min"]

# Define steady-state equations
dT = params["alpha_T"] * sigma_brain * T * (1 - T / params["K_T"]) - params["d_T"] * T - params["d_TI"] * T * (C_t - T_beta)
dsigma_brain = params["alpha_sigma"] * (sigma_serum - sigma_brain) - params["d_Tsigma"] * T * sigma_brain - (params["d_sigma_1"] + params["alpha_s"] * (params["nu"] + C_t + T_beta)) * sigma_brain
dC_t = ((params["a_2"] * T) / (params["k_5"] + T_beta)) - (params["mu_1"] * C_t) - params["alpha_4"] * (T / (T + params["k_3"])) * C_t
dT_beta = params["s_1"] + params["b_1"] * T - params["mu_2"] * T_beta
dsigma_serum = params["alpha_sigma"] * (sigma_brain - sigma_serum) + F_steady - params["d_sigma_2"] * sigma_serum

# List of numerical ranges to explore steady states
ranges = [
    (0, 10),  # T range
    (0, 10),  # sigma_brain range
    (0, 10),  # C_t range
    (0, 10),  # T_beta range
    (0, 10),  # sigma_serum range
]

# Define grid for initial guesses
num_points = 4  # increase for more precision
grids = [np.linspace(start, end, num_points) for start, end in ranges]

# Solve with nsolve
steady_states = []
total_combinations = num_points ** len(ranges)

print("Solving steady states ...")
with tqdm(total=total_combinations, desc="Progress") as pbar:
    for T_val in grids[0]:
        for sigma_brain_val in grids[1]:
            for C_t_val in grids[2]:
                for T_beta_val in grids[3]:
                    for sigma_serum_val in grids[4]:
                        try:
                            guess = (T_val, sigma_brain_val, C_t_val, T_beta_val, sigma_serum_val)
                            sol = sp.nsolve(
                                [dT, dsigma_brain, dC_t, dT_beta, dsigma_serum], 
                                (T, sigma_brain, C_t, T_beta, sigma_serum), 
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
        for var, value in zip([T, sigma_brain, C_t, T_beta, sigma_serum], ss):
            print(f"  {var} = {value.evalf()}")
        print("\n")
else:
    print("No steady states found.")
