"""Routines associated with the application data.
"""

import json

courses = {}

FILE_PATH = "json/course.json"


def load_data() -> dict:
    """Load the data from the json file.
    """
    with open(FILE_PATH, "r") as f:
        courses_list = json.load(f)
    for course in courses_list:
        courses[course["id"]] = course
    return courses
