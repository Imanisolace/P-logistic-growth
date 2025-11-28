import matplotlib.pyplot as plt
import numpy as np

def plot_logistic(t, P, K, r, c):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(t, P, color="blue", label="Population")
    ax.axhline(K, linestyle="--", color="red", label="Carrying Capacity")

    if c > 0 and r > 0:
        t_inflect = (1 / r) * np.log(c)
        if np.isfinite(t_inflect) and t_inflect > 0:
            ax.plot(t_inflect, K / 2, "ro", label="Inflection Point")

    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("Logistic Growth Model")
    ax.grid(alpha=0.3)
    ax.legend()

    return fig
