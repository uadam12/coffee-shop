from flask import jsonify, request


def data(**kwargs):
    kwargs['success'] = True
    return jsonify(kwargs)


def get_data():
    if request.is_json:
        return request.json
    return request.form
