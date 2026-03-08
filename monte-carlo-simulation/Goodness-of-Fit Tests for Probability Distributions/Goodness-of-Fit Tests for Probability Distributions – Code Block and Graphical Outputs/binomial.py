import os
import numpy as np
import matplotlib.pyplot as plt
from math import comb
from scipy.stats import chi2

def binomial_test():
    """
    SCENARIO:
    - 15 emails are sent per day.
    - The probability that an email is clicked (p) = 0.25
    - This data is collected over 100 days.

    TEST:
    - H0: The data follow a Binom(15, 0.25) distribution.
    - H1: The data do not follow a Binom(15, 0.25) distribution.
    - A Chi-Square goodness-of-fit test is applied.
    """

    # 1) Create folder
    folder_name = "binom"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2) Data generation
    np.random.seed(42)
    n = 15
    p = 0.25
    sample_size = 100
    data = np.random.binomial(n, p, sample_size)

    # 3) Observed and expected frequencies
    obs_freq = [np.sum(data == k) for k in range(n+1)]
    exp_freq = []
    for k in range(n+1):
        pmf_val = comb(n, k)*(p**k)*((1-p)**(n-k))
        exp_freq.append(sample_size * pmf_val)

    # 4) Chi-Square statistic
    chi_sq_stat = 0.0
    for obs, exp in zip(obs_freq, exp_freq):
        if exp > 0:
            chi_sq_stat += (obs - exp)**2 / exp

    # 5) Degrees of freedom and p-value
    dof = (n + 1 - 1) - 1
    p_value = 1 - chi2.cdf(chi_sq_stat, dof)

    print("=== Binom(15, 0.25) Test ===")
    print(f"Chi-Square statistic = {chi_sq_stat:.4f}")
    print(f"Degrees of freedom = {dof}")
    print(f"p-value = {p_value:.4f}")

    if p_value < 0.05:
        decision = "H0 is rejected (data may not follow Binom(15,0.25))."
    else:
        decision = "H0 cannot be rejected (data are consistent with Binom(15,0.25))."
    print("Decision:", decision)

    # 7) Explanation text (.txt)
    explanation_path = os.path.join(folder_name, "binom.txt")
    with open(explanation_path, "w", encoding="utf-8") as f:
        f.write("BINOM(15, 0.25) GOODNESS-OF-FIT TEST\n")
        f.write("---------------------------------\n")
        f.write("Scenario:\n")
        f.write(" - 15 emails are sent per day.\n")
        f.write(" - Click probability: p=0.25\n")
        f.write(" - Data collected over 100 days.\n\n")

        f.write("Chi-Square Goodness-of-Fit Test:\n")
        f.write(f" - Chi-Square statistic: {chi_sq_stat:.4f}\n")
        f.write(f" - Degrees of freedom: {dof}\n")
        f.write(f" - p-value: {p_value:.4f}\n\n")

        f.write(f"Decision: {decision}\n")
        f.write("""
Explanation:
If the p-value >= 0.05, the hypothesis that the data come from this binomial
distribution cannot be statistically rejected. If the p-value < 0.05, H0 is rejected.
""")

    # 8) Save histogram
    plt.hist(data, bins=range(n+2), edgecolor='black')
    plt.title("Binom(15, 0.25) Histogram")
    plt.xlabel("Number of Clicked Emails (daily)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    hist_path = os.path.join(folder_name, "binom.jpg")
    plt.savefig(hist_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    binomial_test()