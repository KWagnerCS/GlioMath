import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

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
    "a_2": 0.5, # Ranges from 0-0.5 # antigenicity of glioma (tumor)
    "k_5": 2000, # inhibitory parameter
    "mu_1": 0.0074, # natural death of CD8+ T cells
    "alpha_4": 0.1694, # death rate of CD8+ T Cells
    "k_3": 334452, # half saturation constant
    "s_1": 63305, # constant source of TGF-β
    "b_1": 0.0000057, # release rate per glioma cell
    "mu_2": 6.93, # natural death of TGF-β
}
