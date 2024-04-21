import os

import numpy as np
import pandas as pd
from os import PathLike
from glob import glob
from functools import reduce


def glob_json(folder: str | PathLike[str]) -> pd.DataFrame:
    result = []
    for name in glob(f"{folder}/*.json"):
        result.extend(map(lambda r: r[0], pd.read_json(name).values))
    return pd.DataFrame(result)




# def ways_value_counts(year: str) -> pd.DataFrame:
#     df = glob_json(year).drop_duplicates(subset=["course_id"])
#     gers = df["gers"]
#     # print(gers.value_counts())
#     exploded = gers.explode()
#     return exploded[exploded.str.startswith("WAY")].value_counts()
def ways_value_counts(year: str, department_code: str | None = None) -> pd.DataFrame:
    df = glob_json(year)
    if department_code is not None:
        df = df[df["subject"] == department_code]
    df = df.drop_duplicates(subset=["course_id"])
    gers = df["gers"]
    exploded = gers.explode()
    counts = exploded[exploded.str.startswith("WAY")].value_counts().reset_index()
    counts.columns = ['Requirement', 'Count']
    counts['Year'] = year  # Add a column for the year

    return counts

def time_series(years: list[str], department_code: str | None = None) -> pd.DataFrame:
    all_data = pd.DataFrame()

    for year in years:
        year_data = ways_value_counts(year, department_code)
        all_data = pd.concat([all_data, year_data])

    all_data.reset_index(drop=True, inplace=True)
    pivot_df = all_data.pivot(index="Year", columns="Requirement", values="Count")

    if department_code is not None:
        pivot_df["Department"] = [department_code for _ in range(len(pivot_df))]

    return pivot_df

def years_list(start: int, stop: int) -> list[str]:
    return [f"{i}-{i + 1}" for i in range(start, stop)]

def write_time_series(start: int, stop: int):
    years = years_list(start, stop)
    time_series_df = time_series(years)
    time_series_df.to_csv("time_series.csv")

def time_major_composition(years: list[str], department_codes: list[str]) -> pd.DataFrame:
    all_data = pd.DataFrame()

    for code in department_codes:
        all_data = pd.concat([all_data, time_series(years, code)])

    reduce(lambda a, b: pd.concat([a, time_series(years, b)]), pd.DataFrame())

    return all_data.transpose()


def write_time_major_composition(start: int, stop: int):
    years = years_list(start, stop)

    time_major_composition_df = time_major_composition(years, ["CS", "MATH", "MUSIC"])
    time_major_composition_df.to_csv("time_major_composition.csv")


if __name__ == "__main__":
    # print(ways_value_counts("2023-2024", "CS"))
    write_time_major_composition(2014, 2024)
