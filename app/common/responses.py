from http import HTTPStatus
from flask import Response, json as flask_json

from app.common.encoders import ExtendedJSONEncoder
# Alias HTTP response codes
Status = HTTPStatus


class IkiruJsonResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, payload=None, message=None, status_code=HTTPStatus.OK, headers=None):
        """ Sens an application/json response with the following format:
        {
            status: {
                code: <response status code>,
                message: <custom message or default phrase for the return code>
            }
            data: <payload>
        }
        response_status may be either int or HTTPStatus enum value.
        """
        if isinstance(status_code, int):
            st_res = [st for st in HTTPStatus if status_code == st.value]
            if len(st_res) != 1:
                raise ValueError('Invalid response code')
            status_code = st_res[0]

        # Sadly there is no JSON response standardization
        # Using a home-baked static response format
        response = {
            'status': {
                'code': status_code.value,
                'message': message or status_code.phrase
            },
        }

        if payload is not None:
            response['data'] = payload

        response_json = flask_json.dumps(response, cls=ExtendedJSONEncoder)
        super(IkiruJsonResponse, self).__init__(response_json, status_code.value, headers=headers)
