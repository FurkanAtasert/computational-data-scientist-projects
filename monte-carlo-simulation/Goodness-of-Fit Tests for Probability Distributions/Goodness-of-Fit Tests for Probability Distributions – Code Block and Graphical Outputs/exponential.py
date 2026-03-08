import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, kstest

def exponential_test():
    """
    SCENARIO:
    - The average time between two failures in a machine is 4 hours => λ=0.25.
    - 80 failure intervals are observed.

    TEST:
    - H0: The data follow an Exponential(λ=0.25) distribution.
    - H1: The data do not follow this exponential distribution.
    - With the Kolmogorov-Smirnov test, if p-value < 0.05 => H0 is rejected.
    """

    # 1) Folder
    folder_name = "exponential"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2) Data
    np.random.seed(46)
    lam = 0.25
    sample_size = 80
    data = np.random.exponential(scale=1/lam, size=sample_size)

    # 3) KS test
    ks_stat, p_value = kstest(data, 'expon', args=(0, 1/lam))

    # 4) Console output
    print("=== Exponential(λ=0.25) Test ===")
    print(f"KS Statistic = {ks_stat:.4f}")
    print(f"p-value = {p_value:.4f}")

    if p_value < 0.05:
        decision = "H0 is rejected (data may not follow Exponential(0.25))."
    else:
        decision = "H0 cannot be rejected (data are consistent with Exponential(0.25))."
    print("Decision:", decision)

    # 5) Save .txt
    explanation_path = os.path.join(folder_name, "exponential.txt")
    with open(explanation_path, "w", encoding="utf-8") as f:
        f.write("EXPONENTIAL(λ=0.25) GOODNESS-OF-FIT TEST\n")
        f.write("---------------------------------\n")
        f.write("Scenario:\n")
        f.write(" - The average time between two failures is 4 hours.\n")
        f.write(" - 80 failure intervals observed.\n\n")

        f.write("Kolmogorov-Smirnov Test:\n")
        f.write(f" - KS statistic: {ks_stat:.4f}\n")
        f.write(f" - p-value: {p_value:.4f}\n\n")

        f.write(f"Decision: {decision}\n")
        f.write("""
Explanation:
The exponential distribution is commonly used for waiting times or
failure intervals. If p-value >= 0.05, no statistical evidence is found
against this distribution.
""")

    # 6) Histogram
    plt.hist(data, bins=10, edgecolor='black')
    plt.title("Exponential(λ=0.25) Histogram")
    plt.xlabel("Failure Interval (hours)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    hist_path = os.path.join(folder_name, "exponential.jpg")
    plt.savefig(hist_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    exponential_test()