from flask import request, abort
from jose import jwt
from jose.exceptions import JWTError
from urllib.request import urlopen
from urllib.error import URLError
from werkzeug.exceptions import HTTPException
from functools import wraps
import json
from dotenv import load_dotenv
from os import getenv

load_dotenv()


AUTH0_DOMAIN = getenv('AUTH0_DOMAIN', 'uadam12.us.auth0.com')
ALGORITHMS = getenv('ALGORITHMS', ['RS256'])
API_AUDIENCE = getenv('API_AUDIENCE', 'coffee')


class AuthError(HTTPException):
    def __init__(self, code, description):
        self.code = code
        self.description = description


# Auth Header

# source : https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def get_token_auth_header():
    # Obtains the Access Token from the Authorization Header
    auth = request.headers.get('Authorization', None)

    # Check if the auth header is available
    if auth is None:
        raise AuthError(401, 'Authorization header Not Found')

    # Split authorization into parts
    auth_parts = auth.split(' ')
    
    # Check if the Token is available
    if len(auth_parts) == 1:
        raise AuthError(401, 'Token not found.')

    # Check if authorization is bearer token
    if len(auth_parts) > 2:
        raise AuthError(401, 'Authorization must be "bearer token".')

    # Check token type
    token_type = auth_parts[0].lower()
    if token_type != 'bearer':
        raise AuthError(
            401,
            'Invalid Token Type. Token type must be Bearer.'
        )

    token = auth_parts[1]
    return token


def check_permissions(permission, payload):
    user_permissions = payload.get('permissions', None)

    # Check if permissions array in the JWT
    if user_permissions is None:
        abort(400, "You are not permitted to access this resources.")

    # Check if the user have permissions to access this rescuers
    if permission not in user_permissions:
        raise AuthError(403, 'You are not permitted to access the requested resources.')


def verify_decode_jwt(token):
    try:
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        if 'kid' not in unverified_header:
            raise AuthError(401, 'Invalid Token. Authorization malformed.')

        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

    except jwt.ExpiredSignatureError:
        raise AuthError(401, 'Token has expired.')

    except jwt.JWTClaimsError:
        raise AuthError(401, 'Invalid claims. Please, check the audience and issuer.')

    except JWTError:
        raise AuthError(400, 'Invalid token provided')

    except URLError:
        raise AuthError(417, 'It looks like you are offline.')
    raise AuthError(403, 'Invalid Header. Unable to find the appropriate key.')


def requires_auth(permission=''):
    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return func(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
