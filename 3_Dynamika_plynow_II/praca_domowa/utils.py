from flask import Response, request

from errors import InvalidUsage


def check_auth(username, password):
    """This function is called to check if a username password combination is
    valid."""
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def get_train_from_json():
    train_data = request.get_json()
    if not train_data:
        raise InvalidUsage('Please provide json data')
    return train_data
