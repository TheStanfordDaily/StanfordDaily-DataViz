from typing import Any
from os import PathLike
import pandas as pd
from tqdm import tqdm
from explorecourses import CourseConnection, School, Department, filters

ways_nice_names = {
    filters.WAY_AII: "Aesthetic and Interpretive Inquiry",
    filters.WAY_CE: "Creative Expression",
    filters.WAY_EDP: "Exploring Difference and Power",
    filters.WAY_ER: "Ethical Reasoning",
    filters.WAY_FR: "Formal Reasoning",
    filters.WAY_AQR: "Applied Quantitative Reasoning",
    filters.WAY_SMA: "Scientific Method and Analysis",
    filters.WAY_SI: "Social Inquiry"
}
connect = CourseConnection()

year = "2023-2024"
# for school in connect.get_schools(year):
#     for dept in school.departments:
#         for req_filter in [filters.WAY_AII, filters.WAY_CE, filters.WAY_ED, filters.WAY_ER, filters.WAY_FR, filters.WAY_AQR, filters.WAY_SMA, filters.WAY_SI]:
#             courses = connect.get_courses_by_query(dept.code, req_filter, year=year)
#             print(f"{dept.name} has {len(courses)} {req_filter}")
            # for course in courses:
            #     print(course)

# column chart of all depts across a given ways requirement
# stacked column chart of all depts across a given ways requirement
# pie chart of each dept with its composition of requirements

def create_dataframe(connect: CourseConnection, school: School, ways: list[str], year: Any):
    data = dict()

    for dept in tqdm(school.departments, desc=school.name):
        # Initialize an empty list to hold the number of courses for each WAYS requirement.
        num_courses = []

        for way in ways:
            courses = connect.get_courses_by_query(dept, way, year=year)
            # Append the number of courses to the list.
            num_courses.append(len(courses))

        # Add the list of number of courses to the dictionary with the department as the key
        data[dept] = num_courses

    return pd.DataFrame(data, index=ways)


# for school in connect.get_schools(year):
#     # departments = [dept.code for dept in school.departments]
#     ways = [filters.WAY_AII, filters.WAY_CE, filters.WAY_EDP, filters.WAY_ER, filters.WAY_FR, filters.WAY_AQR, filters.WAY_SMA, filters.WAY_SI]
#     df = create_dataframe(school, ways, connect, year)
#     df.to_csv(f"{school.name}.csv")


def export_all_schools_to_csv(connect: CourseConnection, year: Any, ways: list[str], filename: str | PathLike[str]):
    dfs = []

    for school in connect.get_schools(year):
        df = create_dataframe(connect, school, ways, year)
        dfs.append(df)

    # Concatenate all the DataFrames and write to CSV.
    result = pd.concat(dfs, axis=1).transpose()
    result.to_csv(filename)


# ways = [filters.WAY_AII, filters.WAY_CE, filters.WAY_EDP, filters.WAY_ER, filters.WAY_FR, filters.WAY_AQR, filters.WAY_SMA, filters.WAY_SI]
# export_all_schools_to_csv(connect, year, ways, "all_schools.csv")

# then a pack chart for each WAYS requirement where a bubble is a department sized on how many it has
# could also have a time series of increase and decreases of requirements listed in various depts/schools over the years

def create_dataframe_pack(connect: CourseConnection, school: School, ways: list[str], year: Any):
    data = {"School": [],  "Department": [], "Number of Courses": [], "Requirement": [], "Department Code": []}

    for dept in tqdm(school.departments, desc=school.name):
        for way in ways:
            courses = connect.get_courses_by_query(dept, way, year=year)
            data["Requirement"].append(ways_nice_names[way])
            data["Department"].append(dept.name)
            data["Number of Courses"].append(len(courses))
            data["School"].append(school)
            data["Department Code"].append(dept.code)

    return pd.DataFrame(data)

def export_all_pack_to_csv(connect: CourseConnection, year: Any, ways: list[str], filename: str | PathLike[str]):
    dfs = []

    for school in connect.get_schools(year):
        df = create_dataframe_pack(connect, school, ways, year)
        dfs.append(df)

    # Concatenate all the DataFrames and write to CSV.
    result = pd.concat(dfs, ignore_index=True)
    result.to_csv(filename, index=False)

ways = [filters.WAY_AII, filters.WAY_CE, filters.WAY_EDP, filters.WAY_ER, filters.WAY_FR, filters.WAY_AQR, filters.WAY_SMA, filters.WAY_SI]
export_all_pack_to_csv(connect, year, ways, "all_pack.csv")
