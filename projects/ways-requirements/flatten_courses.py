import pandas as pd
from tqdm import tqdm
from explorecourses import CourseConnection, School, Department, filters, Attribute, Course
import ast
from enum import Enum

def convert_string_to_list(string):
    try:
        return ast.literal_eval(string)
    except SyntaxError:
        return []  # returns an empty list if there is an error


def flatten_courses(courses):
    course_list = []
    for course in courses:
        # Convert multiple-value fields into a single string or simple list
        gers = ", ".join(course.gers) if course.gers else ""
        objectives = ", ".join(str(obj) for obj in course.objectives) if course.objectives else ""
        sections = ", ".join(str(section) for section in course.sections) if course.sections else ""
        tags = ", ".join(str(tag) for tag in course.tags) if course.tags else ""
        attributes = ", ".join(str(attr) for attr in course.attributes) if course.attributes else ""

        # Flatten the course into a dictionary suitable for DataFrame.
        # Note that description is not included, so as to keep file size down.
        course_dict = {
            'year': course.year,
            'subject': course.subject,
            'code': course.code,
            'title': course.title,
            # 'description': course.description,
            'gers': gers,
            'repeatable': course.repeatable,
            'grading_basis': course.grading_basis,
            'units_min': course.units_min,
            'units_max': course.units_max,
            'objectives': objectives,
            'final_exam': course.final_exam,
            'sections': sections,
            'tags': tags,
            'attributes': attributes,
            'course_id': course.course_id,
            'active': course.active,
            'offer_num': course.offer_num,
            'academic_group': course.academic_group,
            'academic_org': course.academic_org,
            'academic_career': course.academic_career,
            'max_units_repeat': course.max_units_repeat,
            'max_times_repeat': course.max_times_repeat
        }
        course_list.append(course_dict)

    return pd.DataFrame(course_list)

# Usage example:
# courses = [Course(elem1), Course(elem2), ...]
# df = flatten_courses(courses)
# df.to_csv('courses.csv', index=False)

def get_year(year: str, connect: CourseConnection = CourseConnection()) -> pd.DataFrame:
    course_list = []
    for school in connect.get_schools(year):
        for dept in tqdm(school.departments, desc=f"{school.name} ({year})"):
            courses = connect.get_courses_by_department(dept.code, year=year)
            for course in courses:
                course_list.append(course)

    return flatten_courses(course_list)

# df = flatten_courses(course_list)
# df.to_csv("2017-2018.csv", index=False)

df = pd.read_csv("2017-2018.csv").dropna(subset=["gers"]) # .drop_duplicates(subset=["course_id"])
# df['gers'] = df['gers'].apply(convert_string_to_list)
# print(df["gers"].explode().value_counts())

def count_ways(df: pd.DataFrame, way: str) -> int:
    return len(df[df["gers"].str.contains(way)].index)

print(count_ways(df[df["subject"] == "HISTORY"], "WAY-SI"))