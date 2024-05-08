import numpy as np
import pandas as pd
from os import PathLike
from glob import glob
from tqdm import tqdm
import itertools

req_names = [
    "WAY-SI",
    "WAY-EDP",
    "WAY-A-II",
    "WAY-CE",
    "WAY-SMA",
    "WAY-FR",
    "WAY-AQR",
    "WAY-ER"
]

req_abbrev_to_full = {
    "WAY-SI": "Social Inquiry",
    "WAY-EDP": "Exploring Difference and Power",
    "WAY-A-II": "Aesthetic and Interpretive Inquiry",
    "WAY-CE": "Creative Expression",
    "WAY-SMA": "Scientific Method and Analysis",
    "WAY-FR": "Formal Reasoning",
    "WAY-AQR": "Applied Quantitative Reasoning",
    "WAY-ER": "Ethical Reasoning"
}

department_code_to_full = {
    "ATHLETIC": "Athletics and Club Sports",
    "KIN": "Kinesiology",
    "OUTDOOR": "Outdoor Education",
    "PHYSWELL": "Physical Wellness",
    "EARTHSYS": "Earth Systems",
    "ENERGY": "Energy Science and Engineering",
    "ENVRES": "Environment and Resources",
    "EPS": "Earth and Planetary Sciences",
    "ESS": "Earth System Science",
    "OCEANS": "Oceans",
    "GEOPHYS": "Geophysics",
    "SUSTAIN": "Sustainability",
    "SUST": "Sustainability Science and Practice",
    "ACCT": "Accounting",
    "ALP": "Action Learning Programs",
    "BUSGEN": "Business General Pathways",
    "MGTECON": "Economic Analysis and Policy",
    "FINANCE": "Finance",
    "GSBGEN": "GSB General and Interdisciplinary",
    "GSBGID": "GSB Interdisciplinary",
    "HRMGT": "Human Resource Management",
    "MKTG": "Marketing",
    "OIT": "Operations Information and Technology",
    "OB": "Organizational Behavior",
    "POLECON": "Political Economics",
    "STRAMGT": "Strategic Management",
    "EDUC": "Education",
    "AA": "Aeronautics and Astronautics",
    "BIOE": "Bioengineering",
    "CHEMENG": "Chemical Engineering",
    "CEE": "Civil and Environmental Engineering",
    "CME": "Computational and Mathematical Engineering",
    "CS": "Computer Science",
    "DESIGN": "Design",
    "DESINST": "Design Institute",
    "EE": "Electrical Engineering",
    "ENGR": "Engineering",
    "MS&E": "Management Science and Engineering",
    "MATSCI": "Materials Science and Engineering",
    "ME": "Mechanical Engineering",
    "SCCM": "Scientific Computing and Computational Math",
    "AFRICAAM": "African and African American Studies",
    "AMELANG": "African and Middle Eastern Languages",
    "AFRICAST": "African Studies",
    "AMSTUD": "American Studies",
    "ANTHRO": "Anthropology",
    "APPPHYS": "Applied Physics",
    "ARABLANG": "Arabic Language",
    "ARCHLGY": "Archaeology",
    "ARTHIST": "Art History",
    "ARTSINST": "Arts Institute",
    "ARTSTUDI": "Art Studio",
    "ASNAMST": "Asian American Studies",
    "ASNLANG": "Asian Languages",
    "BIO": "Biology",
    "BIOHOPK": "Biology/Hopkins Marine",
    "BIOPHYS": "Biophysics",
    "CATLANG": "Catalan Language Courses",
    "CHEM": "Chemistry",
    "CHILATST": "Chicana/o-Latina/o Studies",
    "CHINA": "Chinese",
    "CHINLANG": "Chinese Language",
    "CLASSICS": "Classics",
    "COMM": "Communication",
    "COMPLIT": "Comparative Literature",
    "CSRE": "Comparative Studies in Race and Ethnicity",
    "DANCE": "Dance",
    "DATASCI": "Data Science",
    "DLCL": "Division of Literatures, Cultures, and Languages",
    # "TAPS": "Drama",
    "EALC": "East Asian Languages and Cultures",
    "EASTASN": "East Asian Studies",
    "ECON": "Economics",
    "ENGLISH": "English",
    "EFSLANG": "English for Foreign Students",
    "ETHICSOC": "Ethics in Society",
    "FEMGEN": "Feminist, Gender and Sexuality Studies",
    "FILMPROD": "Film Production",
    "FILMEDIA": "Film and Media Studies",
    "FRENLANG": "French Language",
    "FRENCH": "French Studies",
    "GERLANG": "German Language",
    "GERMAN": "German Studies",
    "GLOBAL": "Global Studies",
    "HISTORY": "History",
    "HPS": "History and Philosophy of Science",
    "HUMBIO": "Human Biology",
    "HUMRTS": "Human Rights",
    "HUMCORE": "Humanities Core",
    "HUMSCI": "Humanities and Sciences",
    "ILAC": "Iberian and Latin American Cultures",
    "IIS": "Institute for International Studies (FSI)",
    "INTLPOL": "International Policy",
    "INTNLREL": "International Relations",
    "ITALLANG": "Italian Language",
    "ITALIAN": "Italian Studies",
    "JAPAN": "Japanese",
    "JAPANLNG": "Japanese Language",
    "JEWISHST": "Jewish Studies",
    "KOREA": "Korean",
    "KORLANG": "Korean Language",
    "LATINAM": "Latin American Studies",
    "LINGUIST": "Linguistics",
    "MLA": "Master of Liberal Arts",
    "MCS": "Mathematical and Computational Science",
    "MATH": "Mathematics",
    "MEDVLST": "Medieval Studies",
    "MTL": "Modern Thought and Literature",
    "MUSIC": "Music",
    "NATIVEAM": "Native American Studies",
    "PHIL": "Philosophy",
    "PHYSICS": "Physics",
    "POLISCI": "Political Science",
    "PORTLANG": "Portuguese Language",
    "PSYCH": "Psychology",
    "PUBLPOL": "Public Policy",
    "RELIGST": "Religious Studies",
    "REES": "Russian, East European, and Eurasian Studies",
    "STS": "Science, Technology, and Society",
    "SLAVLANG": "Slavic Language",
    "SLAVIC": "Slavic Studies",
    "SOC": "Sociology",
    "SPANLANG": "Spanish Language",
    # "ILAC": "Spanish, Portuguese, and Catalan Literature",
    "SPECLANG": "Special Language Program",
    "SIW": "Stanford in Washington",
    "STATS": "Statistics",
    "SYMSYS": "Symbolic Systems",
    "TAPS": "Theater and Performance Studies",
    "TIBETLNG": "Tibetan Language",
    "URBANST": "Urban Studies",
    "LAW": "Law",
    "LAWGEN": "Law, Nonprofessional",
    "ANES": "Anesthesia",
    "BIOC": "Biochemistry",
    "BIODS": "Biomedical Data Science",
    "BIOMEDIN": "Biomedical Informatics",
    "BMP": "Biomedical Physics",
    "BIOS": "Biosciences Interdisciplinary",
    "CBIO": "Cancer Biology",
    "CTS": "Cardiothoracic Surgery",
    "CSB": "Chemical and Systems Biology",
    "CHPR": "Community Health and Prevention Research",
    "COMPMED": "Comparative Medicine",
    "DERM": "Dermatology",
    "DBIO": "Developmental Biology",
    "EMED": "Emergency Medicine",
    "EPI": "Epidemiology",
    "FAMMED": "Family and Community Medicine",
    "GENE": "Genetics",
    "HRP": "Health Research and Policy",
    "IMMUNOL": "Immunology",
    "LEAD": "Leadership Innovations",
    "LIFE": "Lifeworks",
    "MED": "Medicine",
    "INDE": "Medicine Interdisciplinary",
    "MI": "Microbiology and Immunology",
    "MCP": "Molecular and Cellular Physiology",
    "NBIO": "Neurobiology",
    "NENS": "Neurology and Neurological Sciences",
    "NEPR": "Neurosciences Program",
    "NSUR": "Neurosurgery",
    "OBGYN": "Obstetrics and Gynecology",
    "OPHT": "Ophthalmology",
    "ORTHO": "Orthopedic Surgery",
    "OTOHNS": "Otolaryngology",
    "PATH": "Pathology",
    "PEDS": "Pediatrics",
    "PAS": "Physician Assistant Studies",
    "PSYC": "Psychiatry",
    "RADO": "Radiation Oncology",
    "RAD": "Radiology",
    "SOMGEN": "School of Medicine General",
    "STEMREM": "Stem Cell Biology and Regenerative Medicine",
    "SBIO": "Structural Biology",
    "SURG": "Surgery",
    "UROL": "Urology",
    "WELLNESS": "Wellness Education",
    "CTL": "Center for Teaching and Learning",
    "COLLEGE": "Civic, Liberal, and Global Education",
    "ESF": "Education as Self-Fashioning",
    "ITALIC": "Immersion in the Arts",
    "SOAR": "Online Bridge Course",
    "ORALCOMM": "Oral Communications",
    "OSPGEN": "Overseas Studies General",
    "OSPAUSTL": "Overseas Studies in Australia",
    "OSPBARCL": "Overseas Studies in Barcelona (CASB)",
    "OSPBEIJ": "Overseas Studies in Beijing",
    "OSPBER": "Overseas Studies in Berlin",
    "OSPCPTWN": "Overseas Studies in Cape Town",
    "OSPFLOR": "Overseas Studies in Florence",
    "OSPHONGK": "Overseas Studies in Hong Kong",
    "OSPISTAN": "Overseas Studies in Istanbul",
    "OSPKYOTO": "Overseas Studies in Kyoto",
    "OSPKYOCT": "Overseas Studies in Kyoto (KCJS)",
    "OSPMADRD": "Overseas Studies in Madrid",
    "OSPOXFRD": "Overseas Studies in Oxford",
    "OSPPARIS": "Overseas Studies in Paris",
    "OSPSANTG": "Overseas Studies in Santiago",
    "RESPROG": "Residential Programs",
    "ROTCAF": "ROTC Air Force",
    "ROTCARMY": "ROTC Army",
    "ROTCNAVY": "ROTC Navy",
    "SINY": "Stanford in New York",
    "SLE": "Structured Liberal Education",
    "THINK": "Thinking Matters",
    "UAR": "Undergraduate Advising and Research",
    "PWR": "Program in Writing and Rhetoric",
    "VPTL": "Teaching and Learning"
}

department_codes = ["EARTHSYS", "ENERGY", "ENVRES", "EPS", "ESS", "OCEANS", "GEOPHYS", "SUSTAIN", "SUST", "ACCT", "ALP", "BUSGEN", "MGTECON", "FINANCE", "GSBGEN", "GSBGID", "HRMGT", "MKTG", "OIT", "OB", "POLECON", "STRAMGT", "EDUC", "AA", "BIOE", "CHEMENG", "CEE", "CME", "CS", "DESIGN", "DESINST", "EE", "ENGR", "MS&E", "MATSCI", "ME", "SCCM", "AFRICAAM", "AMELANG", "AFRICAST", "AMSTUD", "ANTHRO", "APPPHYS", "ARABLANG", "ARCHLGY", "ARTHIST", "ARTSINST", "ARTSTUDI", "ASNAMST", "ASNLANG", "BIO", "BIOHOPK", "BIOPHYS", "CATLANG", "CHEM", "CHILATST", "CHINA", "CHINLANG", "CLASSICS", "COMM", "COMPLIT", "CSRE", "DANCE", "DATASCI", "DLCL", "TAPS", "EALC", "EASTASN", "ECON", "ENGLISH", "EFSLANG", "ETHICSOC", "FEMGEN", "FILMPROD", "FILMEDIA", "FRENLANG", "FRENCH", "GERLANG", "GERMAN", "GLOBAL", "HISTORY", "HPS", "HUMBIO", "HUMRTS", "HUMCORE", "HUMSCI", "ILAC", "IIS", "INTLPOL", "INTNLREL", "ITALLANG", "ITALIAN", "JAPAN", "JAPANLNG", "JEWISHST", "KOREA", "KORLANG", "LATINAM", "LINGUIST", "MLA", "MCS", "MATH", "MEDVLST", "MTL", "MUSIC", "NATIVEAM", "PHIL", "PHYSICS", "POLISCI", "PORTLANG", "PSYCH", "PUBLPOL", "RELIGST", "REES", "STS", "SLAVLANG", "SLAVIC", "SOC", "SPANLANG", "ILAC", "SPECLANG", "SIW", "STATS", "SYMSYS", "TAPS", "TIBETLNG", "URBANST", "LAW", "LAWGEN", "ANES", "BIOC", "BIODS", "BIOMEDIN", "BMP", "BIOS", "CBIO", "CTS", "CSB", "CHPR", "COMPMED", "DERM", "DBIO", "EMED", "EPI", "FAMMED", "GENE", "HRP", "IMMUNOL", "LEAD", "LIFE", "MED", "INDE", "MI", "MCP", "NBIO", "NENS", "NEPR", "NSUR", "OBGYN", "OPHT", "ORTHO", "OTOHNS", "PATH", "PEDS", "PAS", "PSYC", "RADO", "RAD", "SOMGEN", "STEMREM", "SBIO", "SURG", "UROL", "WELLNESS", "CTL", "COLLEGE", "ESF", "ITALIC", "SOAR", "ORALCOMM", "OSPGEN", "OSPAUSTL", "OSPBARCL", "OSPBEIJ", "OSPBER", "OSPCPTWN", "OSPFLOR", "OSPHONGK", "OSPISTAN", "OSPKYOTO", "OSPKYOCT", "OSPMADRD", "OSPOXFRD", "OSPPARIS", "OSPSANTG", "RESPROG", "ROTCAF", "ROTCARMY", "ROTCNAVY", "SINY", "SLE", "THINK", "UAR", "PWR", "VPTL"]


def glob_json(folder: str | PathLike) -> pd.DataFrame:
    result = []
    for name in glob(f"{folder}/*.json"):
        result.extend(map(lambda r: r[0], pd.read_json(name).values))
    return pd.DataFrame(result)


def ways_value_counts(year: str, department_code: str | None = None, drop_duplicates: bool = True) -> pd.DataFrame:
    df = glob_json(year)

    if department_code is not None:
        df = df[df["subject"] == department_code]
    if drop_duplicates:
        df = df.drop_duplicates(subset=["course_id"])
    # df = df[df["active"]]
    # print(df["sections"].values[0][0]["term"])
    df = df[df['sections'].apply(lambda sections: any('2023-2024' in section['term'] for section in sections))]
    print(df[df["title"].str.contains("History Goes Pop")])
    print(df)
    # Filter the DataFrame to only include rows where at least one objective has a code of "WAY-CE"
    # df = df[df["objectives"].apply(lambda objectives: any("WAY" in obj["code"] for obj in objectives))]
    # print(df)

    gers = df["gers"]
    exploded = gers.explode()
    counts = exploded[exploded.str.contains("WAY")].value_counts().reset_index()
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
Ratio number of units for major against number of ways requirements that major satisfies
"""

def scatter_plot(start: int, stop: int) -> pd.DataFrame:
    data = []

    for year in years_list(start, stop):
        df = glob_json(year)
        # df = df.dropna(subset=["gers"]).drop_duplicates(subset=["course_id"])
        has_section = df["sections"].apply(lambda r: len(r) > 0)
        req = df["gers"].apply(lambda r: any(g.startswith("WAY-") for g in r))
        df = df[has_section & req]
        print(len(df.index))
        row = dict(df["gers"].explode().value_counts())
        row = {key: value for key, value in row.items() if "WAY-" in key}
        row["Year"] = year
        data.append(row)

    return pd.DataFrame(data)


def bar_race(start: int, stop: int) -> pd.DataFrame:
    data = dict()

    for year in tqdm(years_list(start, stop)):
        df = glob_json(f"/Users/matthewturk/Desktop/ways-data/{year}")
        has_sections = df["sections"].apply(lambda x: len(x) > 0)
        column = []

        for name in req_names:
            # print(df["gers"].value_counts())
            req = df["gers"].apply(lambda r: name in r)
            # print(req_name, len(df[has_sections & req].index))
            column.append(len(df[has_sections & req].index))

        data[year] = column

    return pd.DataFrame(data, index=req_names)


def ways_distribution(year: str) -> pd.DataFrame:
    data = []
    df = glob_json(year)
    has_ways = df["gers"].apply(lambda r: any(g.startswith("WAY-") for g in r))

    for code in tqdm(department_codes):
        subject = df["subject"] == code
        has_schedule = df["sections"].apply(lambda r: len(r) > 0)
        ddf = df[has_schedule & subject & has_ways]
        exploded = ddf["gers"].explode()

        value_counts = exploded.value_counts()
        row = dict(value_counts)
        row = {req_abbrev_to_full[key]: value for key, value in row.items() if key.startswith("WAY-")}

        for name in req_abbrev_to_full.values():
            if name not in row:
                row[name] = None

        row["Department"] = department_code_to_full[code]
        data.append(row)

    return pd.DataFrame(data)

def ways_layers(start: int, stop: int) -> pd.DataFrame:
    data = []
    df = glob_json("2023-2024")

    for year in years_list(start, stop):
        for code in tqdm(department_codes):
            for name in req_names:
                req = df["gers"].apply(lambda r: name in r)
                subject = df["subject"] == code
                has_schedule = df["sections"].apply(lambda r: len(r) > 0)
                fdf = df[has_schedule & subject & req] # .drop_duplicates(subset=["course_id"])
                row = {
                    "Requirement": req_abbrev_to_full[name],
                    "Department": department_code_to_full[code],
                    "Department Code": code,
                    "Number of Courses": len(fdf.index),
                    "Year": year
                }

                if all(d != row for d in data):
                    data.append(row)

    return pd.DataFrame(data)


def print_statistical_summary():
    df = glob_json("2023-2024")
    within_doerr = df["academic_group"] == "SUSTN"
    within_hs = df["academic_group"] == "H&S"
    within_soe = df["academic_group"] == "ENGR"
    req = df["gers"].apply(lambda r: any(x.startswith("WAY-") for x in r))
    ug = df["academic_career"] == "UG"
    has_sections = df["sections"].apply(lambda r: len(r) > 0)
    # dept = df["subject"] == "GEOPHYS"
    base_filters = has_sections & req
    doerr_counts = df[within_doerr & base_filters].groupby("subject").size()
    hs_counts = df[within_hs & base_filters].groupby("subject").size()
    soe_counts = df[within_soe & base_filters].groupby("subject").size()

    print("Doerr School of Sustainability")
    print(f"Mean: {doerr_counts.mean()}")
    print(f"Median: {doerr_counts.median()}")
    print(f"Standard Deviation: {doerr_counts.std()}")
    print("School of Humanities and Sciences")
    print(f"Mean: {hs_counts.mean()}")
    print(f"Median: {hs_counts.median()}")
    print(f"Standard Deviation: {hs_counts.std()}")
    print("School of Engineering")
    print(f"Mean: {soe_counts.mean()}")
    print(f"Median: {soe_counts.median()}")
    print(f"Standard Deviation: {soe_counts.std()}")


if __name__ == "__main__":
    # write_time_major_composition(2014, 2024, department_codes)
    # print(time_series(["2023-2024"], "HISTORY"))
    # print(ways_value_counts("2023-2024", "HISTORY", drop_duplicates=True))
    # subject = df["subject"] == "HISTORY"
    # req = df["gers"].apply(lambda x: "WAY-CE" in x) # df["gers"].astype(str).str.contains("WAY-CE")
    # df = df.drop_duplicates(subset=["course_id"])
    # req = df["gers"].apply(lambda r: any(g.startswith("WAY-") for g in r)) # df["gers"].astype(str).str.contains("WAY")

    # df = df[has_sections & req]
    # df = df[subject & req]
    # df = df["sections"]
    # 1,876 courses in 2023-24 school year satisfy ways.
    # if you account for cross listings, that number is then 1,266.
    # row = dict(df["gers"].explode().value_counts())
    # row = {key: value for key, value in row.items() if "WAY-" in key}
    # print(row)
    # for row in df["sections"]:
    #     if len(row) > 0:
    #         print(row)
    scatter_plot(2014, 2024).to_csv("growth_of_ways.csv", index=False)
    # bar_race(2014, 2024).to_csv("bar_race.csv")
    # ways_layers(2023, 2024).to_csv("ways_layers.csv", index=False)
    # df = glob_json("2018-2019")
    # req = df["gers"].apply(lambda r: any(g.startswith("WAY-") for g in r))
    # print(df[req].drop_duplicates(subset=["course_id"]))
    # exploded = ways_distribution("2023-2024")["gers"].explode()
    # ways_distribution("2023-2024").to_csv("ways_distribution.csv", index=False)

    # data = []
    # for year in years_list(2014, 2024):
    #     row = {"Year": year}
    #     for name in tqdm(req_names):
    #         df = glob_json(year)
    #         req = df["gers"].apply(lambda r: name in r)
    #         has_sections = df["sections"].apply(lambda r: len(r) > 0)
    #         df = df[has_sections & req]
    #         df = df.drop_duplicates(subset=["course_id"])
    #         row[req_abbrev_to_full[name]] = len(df.index)
    #     data.append(row)
    # pd.DataFrame(data).to_csv("growth_of_ways.csv")