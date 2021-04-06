import os
import json

from requests import Request, Session


def load_json():
    """ loads and returns json file """

    project_path = os.path.abspath(os.path.dirname(__file__))
    json_file_path = os.path.join(project_path, 'config.json')

    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    return data
