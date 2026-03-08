import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, kstest
import statsmodels.api as sm

def normal_test():
    """
    SCENARIO:
    - Mathematics scores of students in a class follow ~ Normal(μ=70, σ=10).
    - Scores of 150 students were collected.

    TEST:
    - H0: The data follow a Normal(70,10) distribution.
    - H1: The data do not follow a Normal(70,10) distribution.
    - The Kolmogorov-Smirnov test is applied.
    """

    # 1) Folder
    folder_name = "normal"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2) Data
    np.random.seed(45)
    mu, sigma = 70, 10
    sample_size = 150
    data = np.random.normal(mu, sigma, sample_size)

    # 3) KS test
    ks_stat, p_value = kstest(data, 'norm', args=(mu, sigma))

    # 4) Console output
    print("=== Normal(70,10) Test ===")
    print(f"KS Statistic = {ks_stat:.4f}")
    print(f"p-value = {p_value:.4f}")

    if p_value < 0.05:
        decision = "H0 is rejected (data may not follow Normal(70,10))."
    else:
        decision = "H0 cannot be rejected (data are consistent with Normal(70,10))."
    print("Decision:", decision)

    # 5) Save .txt
    explanation_path = os.path.join(folder_name, "normal.txt")
    with open(explanation_path, "w", encoding="utf-8") as f:
        f.write("NORMAL(70,10) GOODNESS-OF-FIT TEST\n")
        f.write("---------------------------------\n")
        f.write("Scenario:\n")
        f.write(" - Student exam scores: mean 70, standard deviation 10.\n")
        f.write(" - Scores of 150 students.\n\n")

        f.write("Kolmogorov-Smirnov Test:\n")
        f.write(f" - KS statistic: {ks_stat:.4f}\n")
        f.write(f" - p-value: {p_value:.4f}\n\n")

        f.write(f"Decision: {decision}\n")
        f.write("""
Explanation:
If p-value < 0.05, it indicates a statistically significant deviation from
the normal distribution. The Q-Q plot should also be examined.
""")

    # 6) Histogram
    plt.hist(data, bins=10, edgecolor='black')
    plt.title("Normal(70,10) Histogram")
    plt.xlabel("Exam Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    hist_path = os.path.join(folder_name, "normal.jpg")
    plt.savefig(hist_path, dpi=300)
    plt.show()

    # 7) Q-Q plot (optional save)
    fig = sm.qqplot(data, line='s')
    plt.title("Normal(70,10) - Q-Q Plot")
    qq_path = os.path.join(folder_name, "normal_qq.jpg")
    plt.savefig(qq_path, dpi=300)
    plt.show()

if __name__ == "__main__":
    normal_test()