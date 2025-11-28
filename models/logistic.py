import numpy as np

def logistic_curve(K, r, P0, t_max, n=5000):
    t = np.linspace(0, t_max, n)
    c = (K - P0) / max(P0, 1e-12)
    P = K / (1 + c * np.exp(-r * t))
    return t, P, c