from __future__ import annotations

import numpy as np
import pandas as pd
from pandas_datareader import wb

pd.options.display.width = 0

TARGET_COUNTRY = "Australia"
ANALYSIS_YEAR = 2010

INDICATORS = {
    "exports": "NE.EXP.GNFS.CD",
    "imports": "NE.IMP.GNFS.CD",
    "agriculture_value_added": "NV.AGR.TOTL.CD",
    "gdp": "NY.GDP.MKTP.CD",
    "external_balance": "NE.RSB.GNFS.CD",
}


def download_world_bank_data(indicators: list[str], year: int) -> pd.DataFrame:
    return wb.download(country="all", indicator=indicators, start=year, end=year).reset_index()


def filter_non_aggregate_countries(df: pd.DataFrame) -> pd.DataFrame:
    countries = wb.get_countries()
    non_aggregates = countries[countries["region"] != "Aggregates"].name
    return df[df["country"].isin(non_aggregates)].dropna()


def build_country_vectors(df: pd.DataFrame, indicators: list[str]) -> dict[str, np.ndarray]:
    vectors: dict[str, np.ndarray] = {}

    for _, row in df.iterrows():
        vectors[row["country"]] = row[indicators].values.astype(float)

    return vectors


def compute_distances(vectors: dict[str, np.ndarray], target_country: str) -> pd.DataFrame:
    if target_country not in vectors:
        raise ValueError(f"Target country not found in vectors: {target_country}")

    target_vector = vectors[target_country]
    euclidean_distances: dict[str, float] = {}
    cosine_distances: dict[str, float] = {}

    for country, vector in vectors.items():
        euclidean_distance = np.linalg.norm(target_vector - vector)
        cosine_similarity = (target_vector @ vector) / (
            np.linalg.norm(target_vector) * np.linalg.norm(vector)
        )

        euclidean_distances[country] = euclidean_distance
        cosine_distances[country] = 1 - cosine_similarity

    return pd.DataFrame(
        {
            "euclidean_distance": euclidean_distances,
            "cosine_distance": cosine_distances,
        }
    )


def display_results(df_distances: pd.DataFrame, df_filtered: pd.DataFrame, target_country: str, year: int) -> None:
    print(f"Target country: {target_country}")
    print(f"Analysis year: {year}")
    print(f"Number of countries analyzed: {len(df_distances)}")
    print()

    print("Closest countries by Euclidean distance:")
    print(df_distances.sort_values(by="euclidean_distance").head())
    print()

    print("Closest countries by cosine distance:")
    print(df_distances.sort_values(by="cosine_distance").head())
    print()

    print("Selected country details:")
    print(df_filtered[df_filtered["country"].isin(["Mexico", "Colombia", target_country])])


def main() -> None:
    indicator_codes = list(INDICATORS.values())

    df_raw = download_world_bank_data(indicator_codes, ANALYSIS_YEAR)
    df_filtered = filter_non_aggregate_countries(df_raw)
    country_vectors = build_country_vectors(df_filtered, indicator_codes)
    df_distances = compute_distances(country_vectors, TARGET_COUNTRY)

    display_results(df_distances, df_filtered, TARGET_COUNTRY, ANALYSIS_YEAR)


if __name__ == "__main__":
    main()