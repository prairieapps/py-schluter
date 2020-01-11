import os
import json
import logging
from enum import Enum
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

def to_authentication_json(authentication):
    if authentication is None:
        return json.dumps({})

    return json.dumps({
        "session_id": authentication.session_id,
        "state": authentication.state.value,
        "expires": authentication.expires.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    })

def from_authentication_json(data):
    if data is None:
        return None

    session_id = data["session_id"]
    state = AuthenticationState(data["state"])
    expires = data["expires"]
    return Authentication(state, session_id, expires)

class AuthenticationState(Enum):
    REQUIRES_AUTHENTICATION = "requires_authentication"
    AUTHENTICATED = "authenticated"
    BAD_EMAIL = "bad_email"
    BAD_PASSWORD = "bad_password"

class Authentication:
    def __init__(self, state, session_id = None, expires = None):
        self._state = state
        self._session_id = session_id,
        self._expires = expires

    @property
    def session_id(self):
        return self._session_id

    @property
    def expires(self):
        return self._expires

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

class Authenticator:

    def __init__(self, api, email, password, session_id_cache_file=None):
        self._api = api
        self._email = email
        self._password = password
        self._session_id_cache_file = session_id_cache_file

        if (session_id_cache_file is not None and
                os.path.exists(session_id_cache_file)):
            with open(session_id_cache_file, 'r') as file:
                try:
                    self._authentication = from_authentication_json(
                        json.load(file))
                    token_expired = datetime.strptime(
                        self._authentication.expires,
                        '%Y-%m-%dT%H:%M:%S.%fZ'
                    ) - datetime.utcnow()
                    
                    if token_expired < timedelta(
                            seconds=0):
                        _LOGGER.error("Token has expired.")
                        self._authentication = Authentication(AuthenticationState.REQUIRES_AUTHENTICATION)
                    return
                except json.decoder.JSONDecodeError as error:
                    _LOGGER.error("Unable to read cache file (%s): %s",
                                  session_id_cache_file, error)

        self._authentication = Authentication(AuthenticationState.REQUIRES_AUTHENTICATION)

    def authenticate(self):
        if self._authentication.state == AuthenticationState.AUTHENTICATED:
                return self._authentication
        
        response = self._api.get_session(self._email, self._password)

        data = response.json()
        session_id = data["SessionId"]
        expires = datetime.utcnow() + timedelta(hours=1)

        if data["ErrorCode"] == 2:
            state = AuthenticationState.BAD_PASSWORD
        elif data["ErrorCode"] == 1:
            state = AuthenticationState.BAD_EMAIL
        else:
            state = AuthenticationState.AUTHENTICATED
        
        self._authentication = Authentication(state, session_id, expires)

        if state == AuthenticationState.AUTHENTICATED:
            self._cache_authentication(self._authentication)

        return self._authentication
    
    def _cache_authentication(self, authentication):
        if self._session_id_cache_file is not None:
            with open(self._session_id_cache_file, "w") as file:
                file.write(to_authentication_json(authentication))
