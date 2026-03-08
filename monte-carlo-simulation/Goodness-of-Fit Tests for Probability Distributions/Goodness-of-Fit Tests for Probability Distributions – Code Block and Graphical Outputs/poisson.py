import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare, poisson

def poisson_test():
    """
    SCENARIO:
    - A call center receives an average of 4 complaints per hour (λ=4).
    - Data are recorded over 100 hours.

    TEST:
    - H0: The data follow a Poisson(4) distribution.
    - H1: The data do not follow a Poisson(4) distribution.
    """

    # 1) Folder
    folder_name = "poisson"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2) Data
    np.random.seed(43)
    lam = 4
    sample_size = 100
    data = np.random.poisson(lam, sample_size)

    # 3) Observed and expected frequencies
    obs_counts = np.bincount(data)
    exp_counts = [sample_size * poisson.pmf(k, lam) for k in range(len(obs_counts))]

    # 4) Normalization (to ensure totals match)
    sum_obs = np.sum(obs_counts)
    sum_exp = np.sum(exp_counts)
    if abs(sum_obs - sum_exp) > 1e-8:
        ratio = sum_obs / sum_exp
        exp_counts = [e * ratio for e in exp_counts]

    # 5) Chi-Square Test
    chi_sq_stat, p_value = chisquare(obs_counts, f_exp=exp_counts)

    # 6) Console output
    print("=== Poisson(λ=4) Test ===")
    print(f"Chi-Square statistic = {chi_sq_stat:.4f}")
    print(f"p-value = {p_value:.4f}")

    if p_value < 0.05:
        decision = "H0 is rejected (data may not follow Poisson(4))."
    else:
        decision = "H0 cannot be rejected (data are consistent with Poisson(4))."
    print("Decision:", decision)

    # 7) Save .txt
    explanation_path = os.path.join(folder_name, "poisson.txt")
    with open(explanation_path, "w", encoding="utf-8") as f:
        f.write("POISSON(λ=4) GOODNESS-OF-FIT TEST\n")
        f.write("---------------------------------\n")
        f.write("Scenario:\n")
        f.write(" - A call center receives an average of 4 complaints per hour (λ=4).\n")
        f.write(" - Data collected over 100 hours.\n\n")

        f.write("Chi-Square Goodness-of-Fit Test:\n")
        f.write(f" - Chi-Square statistic: {chi_sq_stat:.4f}\n")
        f.write(f" - p-value: {p_value:.4f}\n\n")

        f.write(f"Decision: {decision}\n")
        f.write("""
Explanation:
The Poisson distribution has infinite support. Unexpectedly high values
may rarely occur. Due to the sensitivity of SciPy's chisquare function,
observed and expected totals were slightly normalized.
If p-value < 0.05, H0 is rejected.
""")

    # 8) Histogram
    plt.hist(data, bins=range(np.max(data)+2), edgecolor='black')
    plt.title("Poisson(λ=4) Histogram")
    plt.xlabel("Number of Complaints per Hour")
    plt.ylabel("Frequency")
    plt.tight_layout()

    hist_path = os.path.join(folder_name, "poisson.jpg")
    plt.savefig(hist_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    poisson_test()