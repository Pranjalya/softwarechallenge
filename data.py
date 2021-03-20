"""Routines associated with the application data.
"""

import json
from collections import defaultdict, OrderedDict
from datetime import datetime


courses = OrderedDict()
title_keywords = defaultdict(set)

last_id = 0

FILE_PATH = "json/course.json"
punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""


def load_title_keywords(title, id):
    """Load the title keywords in a hashmap.
    """
    for e in title:
        if e in punc:
            title = title.replace(e, "")
    for word in title.split():
        title_keywords[word.lower()].add(id)


def load_data():
    """Load the data from the json file.
    """
    global last_id
    with open(FILE_PATH, "r") as f:
        courses_list = json.load(f)
    for course in courses_list:
        courses[course["id"]] = course
        load_title_keywords(course["title"], course["id"])
        last_id = course["id"]


def add_course(json_data):
    print("Adding course")
    global last_id
    json_data["date_created"] = str(datetime.now())
    json_data["date_updated"] = str(datetime.now())
    json_data["id"] = last_id + 1
    courses[last_id + 1] = json_data
    print("JSON", json_data)
    last_id += 1
    return {"data": json_data}


def update_course(id, json_data):
    print("Updating course with id {}".format(id))
    for k in json_data.keys():
        courses[id][k] = json_data[k]
    courses[id]["date_updated"] = str(datetime.now())
    return {"data": courses[id]}


def delete_course(id):
    print("Deleting course with id {}".format(id))
    del courses[id]
