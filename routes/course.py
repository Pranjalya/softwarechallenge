"""Routes for the course resource.
"""

from run import app
from flask import request, Response
from http import HTTPStatus
from math import ceil
import json
import data


def validate_data(json_data):
    assert type(json_data["description"]) == str or json_data["description"] is None
    assert (
        type(json_data["discount_price"]) == int
        or type(json_data["discount_price"]) == float
        or json_data["discount_price"] is None
    )
    assert type(json_data["title"]) == str
    assert type(json_data["price"]) == int or type(json_data["price"]) == float
    assert json_data["price"] >= 0
    assert json_data["discount_price"] >= 0
    assert type(json_data["image_path"]) == str or json_data["image_path"] is None
    assert type(json_data["on_discount"]) == bool or json_data["on_discount"] is None


@app.route("/course/<int:id>", methods=["GET"])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan on your data structure.
    """
    if request.method == "GET":
        if data.courses.get(id, None) is None:
            response = json.dumps({"message": "Course {} does not exist".format(id)})
            return Response(
                response=response,
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
        response = json.dumps(data.courses[id])
        return Response(
            response=response, status=HTTPStatus.OK, content_type="application/json"
        )


@app.route("/course", methods=["GET"])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    if request.method == "GET":
        page_size = request.args.get("page-size", 10)
        page_number = request.args.get("page-number", 1)
        title_words = request.args.get("title-words", None).split(",")

        len_db = len(data.courses)
        matching = []
        counter = {}
        metadata = {"page_count": ceil(len_db/page_size), "page_number": page_number, "page_size": page_size, "record_count": len_db}

        if title_words is None:
            matching = data.courses.values()[(page_number-1)*page_size : page_number*page_size]
        else:
            for word in title_words:
                for id in data.title_keywords[word]:
                    counter[id] = counter.get(id, 0) + 1
            sorted_matchings = sorted(counter, key=counter.get, reverse=True)
            matching = [data.courses[id] for id in sorted_matchings]
            matching = matching[(page_number-1)*page_size : page_number*page_size]

        if len(matching) == 0:
            response = json.dumps({"message": "No matching course found"})
            return Response(
                response=response,
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )
        else:
            response = json.dumps({"data": matching, "metadata": metadata})
            return Response(
                response=response,
                status=HTTPStatus.OK,
                content_type="application/json",
            )


@app.route("/course", methods=["POST"])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    if request.method == "POST":
        try:
            json_data = json.loads(request.data)
            validate_data(json_data)
            return_data = data.add_course(json_data)
            response = json.dumps(return_data)
            return Response(
                response=response,
                status=HTTPStatus.CREATED,
                content_type="application/json",
            )
        except Exception as ae:
            response = json.dumps({"message": "Missing or bad data"})
            return Response(
                response=response,
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )


@app.route("/course/<int:id>", methods=["PUT"])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    if request.method == "PUT":
        invalid = False
        status = None

        if data.courses.get(id, None) is None:
            invalid = True
            status = HTTPStatus.NOT_FOUND
            response = json.dumps({"message": "Course {} does not exist".format(id)})

        if id != data.courses.get(id)["id"]:
            invalid = True
            status = HTTPStatus.BAD_REQUEST
            response = json.dumps({"message": "The id does not match the payload"})

        try:
            json_data = json.loads(request.data)
            validate_data(json_data)
        except:
            invalid = True
            status = HTTPStatus.BAD_REQUEST
            response = json.dumps({"message": "Bad or invalid request format"})

        if invalid:
            return Response(
                response=response, status=status, content_type="application/json",
            )

        return_data = data.update_course(id, json_data)
        response = json.dumps(return_data)
        return Response(
            response=response, status=HTTPStatus.OK, content_type="application/json",
        )


@app.route("/course/<int:id>", methods=["DELETE"])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """

    if request.method == "DELETE":
        if data.courses.get(id, None) is None:
            response = json.dumps({"message": "Course {} does not exist".format(id)})
            return Response(
                response=response,
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json",
            )

        data.delete_course(id)
        response = json.dumps({"message": "The specified course was deleted"})
        return Response(
            response=response, status=HTTPStatus.NO_CONTENT, content_type="application/json",
        )
