import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, kstest

def uniform_test():
    """
    SCENARIO:
    - Produced metal rods are distributed with equal probability between 50 cm and 60 cm.
    - 100 rod measurements were taken.

    TEST:
    - H0: The data follow a Uniform(50,60) distribution.
    - H1: The data do not follow a Uniform(50,60) distribution.
    - The Kolmogorov-Smirnov test is applied.
    """

    # 1) Folder
    folder_name = "uniform"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2) Data
    np.random.seed(44)
    low, high = 50, 60
    sample_size = 100
    data = np.random.uniform(low, high, sample_size)

    # 3) KS test
    ks_stat, p_value = kstest(data, 'uniform', args=(low, high - low))

    # 4) Print results
    print("=== Uniform(50,60) Test ===")
    print(f"KS Statistic = {ks_stat:.4f}")
    print(f"p-value = {p_value:.4f}")

    if p_value < 0.05:
        decision = "H0 is rejected (data may not follow Uniform(50,60))."
    else:
        decision = "H0 cannot be rejected (data are consistent with Uniform(50,60))."
    print("Decision:", decision)

    # 5) Save .txt
    explanation_path = os.path.join(folder_name, "uniform.txt")
    with open(explanation_path, "w", encoding="utf-8") as f:
        f.write("UNIFORM(50,60) GOODNESS-OF-FIT TEST\n")
        f.write("---------------------------------\n")
        f.write("Scenario:\n")
        f.write(" - Metal rods are distributed between 50–60 cm with equal probability.\n")
        f.write(" - 100 measurements.\n\n")

        f.write("Kolmogorov-Smirnov Test:\n")
        f.write(f" - KS statistic: {ks_stat:.4f}\n")
        f.write(f" - p-value: {p_value:.4f}\n\n")

        f.write(f"Decision: {decision}\n")
        f.write("""
Explanation:
The KS test measures the maximum difference between the empirical CDF of the data
and the theoretical Uniform(50,60) CDF. If p-value < 0.05, H0 is rejected.
""")

    # 6) Histogram
    plt.hist(data, bins=10, edgecolor='black')
    plt.title("Uniform(50,60) Histogram")
    plt.xlabel("Rod Length (cm)")
    plt.ylabel("Frequency")
    plt.tight_layout()

    hist_path = os.path.join(folder_name, "uniform.jpg")
    plt.savefig(hist_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    uniform_test()