import numpy as np
import pandas as pd
from os import PathLike
from glob import glob
from tqdm import tqdm


def glob_json(folder: str | PathLike) -> pd.DataFrame:
    result = []
    for name in glob(f"{folder}/*.json"):
        result.extend(map(lambda r: r[0], pd.read_json(name).values))
    return pd.DataFrame(result)


def ways_value_counts(year: str, department_code: str | None = None, drop_duplicates: bool = False) -> pd.DataFrame:
    df = glob_json(year)

    if department_code is not None:
        df = df[df["subject"] == department_code]
    if drop_duplicates:
        df = df.drop_duplicates(subset=["course_id"])

    gers = df["gers"]
    exploded = gers.explode()
    counts = exploded[exploded.str.startswith("WAY")].value_counts().reset_index()
    counts.columns = ["Requirement", "Count"]
    counts["Year"] = year

    return counts


def time_series(years: list[str], department_code: str) -> pd.DataFrame:
    all_data = [ways_value_counts(year, department_code) for year in years]
    all_data = pd.concat(all_data).reset_index(drop=True)
    all_data["Department"] = department_code  # Include department name in each row
    pivot_df = all_data.pivot_table(index=["Department", "Requirement"], columns="Year", values="Count", fill_value=0)

    return pivot_df


def years_list(start: int, stop: int) -> list[str]:
    return [f"{i}-{i + 1}" for i in range(start, stop)]


def time_major_composition(years: list[str], department_codes: list[str]) -> pd.DataFrame:
    all_data = pd.DataFrame()

    for code in tqdm(department_codes):
        all_data = pd.concat([all_data, time_series(years, code)])

    return all_data

def write_time_major_composition(start: int, stop: int, department_codes: list[str]):
    years = years_list(start, stop)
    time_major_composition_df = time_major_composition(years, department_codes)
    time_major_composition_df.to_csv("time_major_composition.csv")

"""
Note, the min unit count chart is not comprehensive, as it does not feature all undergraduate majors, only ones whose estimates were readily available on department websites
Chords between departments to see how strong cross listing for certain ones that would also be interesting
"""

if __name__ == "__main__":
    department_codes = ['EARTHSYS', 'ENERGY', 'ENVRES', 'EPS', 'ESS', 'OCEANS', 'GEOPHYS', 'SUSTAIN', 'SUST', 'ACCT', 'ALP', 'BUSGEN', 'MGTECON', 'FINANCE', 'GSBGEN', 'GSBGID', 'HRMGT', 'MKTG', 'OIT', 'OB', 'POLECON', 'STRAMGT', 'EDUC', 'AA', 'BIOE', 'CHEMENG', 'CEE', 'CME', 'CS', 'DESIGN', 'DESINST', 'EE', 'ENGR', 'MS&E', 'MATSCI', 'ME', 'SCCM', 'AFRICAAM', 'AMELANG', 'AFRICAST', 'AMSTUD', 'ANTHRO', 'APPPHYS', 'ARABLANG', 'ARCHLGY', 'ARTHIST', 'ARTSINST', 'ARTSTUDI', 'ASNAMST', 'ASNLANG', 'BIO', 'BIOHOPK', 'BIOPHYS', 'CATLANG', 'CHEM', 'CHILATST', 'CHINA', 'CHINLANG', 'CLASSICS', 'COMM', 'COMPLIT', 'CSRE', 'DANCE', 'DATASCI', 'DLCL', 'TAPS', 'EALC', 'EASTASN', 'ECON', 'ENGLISH', 'EFSLANG', 'ETHICSOC', 'FEMGEN', 'FILMPROD', 'FILMEDIA', 'FRENLANG', 'FRENCH', 'GERLANG', 'GERMAN', 'GLOBAL', 'HISTORY', 'HPS', 'HUMBIO', 'HUMRTS', 'HUMCORE', 'HUMSCI', 'ILAC', 'IIS', 'INTLPOL', 'INTNLREL', 'ITALLANG', 'ITALIAN', 'JAPAN', 'JAPANLNG', 'JEWISHST', 'KOREA', 'KORLANG', 'LATINAM', 'LINGUIST', 'MLA', 'MCS', 'MATH', 'MEDVLST', 'MTL', 'MUSIC', 'NATIVEAM', 'PHIL', 'PHYSICS', 'POLISCI', 'PORTLANG', 'PSYCH', 'PUBLPOL', 'RELIGST', 'REES', 'STS', 'SLAVLANG', 'SLAVIC', 'SOC', 'SPANLANG', 'ILAC', 'SPECLANG', 'SIW', 'STATS', 'SYMSYS', 'TAPS', 'TIBETLNG', 'URBANST', 'LAW', 'LAWGEN', 'ANES', 'BIOC', 'BIODS', 'BIOMEDIN', 'BMP', 'BIOS', 'CBIO', 'CTS', 'CSB', 'CHPR', 'COMPMED', 'DERM', 'DBIO', 'EMED', 'EPI', 'FAMMED', 'GENE', 'HRP', 'IMMUNOL', 'LEAD', 'LIFE', 'MED', 'INDE', 'MI', 'MCP', 'NBIO', 'NENS', 'NEPR', 'NSUR', 'OBGYN', 'OPHT', 'ORTHO', 'OTOHNS', 'PATH', 'PEDS', 'PAS', 'PSYC', 'RADO', 'RAD', 'SOMGEN', 'STEMREM', 'SBIO', 'SURG', 'UROL', 'WELLNESS', 'CTL', 'COLLEGE', 'ESF', 'ITALIC', 'SOAR', 'ORALCOMM', 'OSPGEN', 'OSPAUSTL', 'OSPBARCL', 'OSPBEIJ', 'OSPBER', 'OSPCPTWN', 'OSPFLOR', 'OSPHONGK', 'OSPISTAN', 'OSPKYOTO', 'OSPKYOCT', 'OSPMADRD', 'OSPOXFRD', 'OSPPARIS', 'OSPSANTG', 'RESPROG', 'ROTCAF', 'ROTCARMY', 'ROTCNAVY', 'SINY', 'SLE', 'THINK', 'UAR', 'PWR', 'VPTL']
    write_time_major_composition(2014, 2024, department_codes)