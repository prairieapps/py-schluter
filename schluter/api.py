import logging
import json
from requests import request, Session

from schluter.thermostat import Thermostat

API_BASE_URL = "https://ditra-heat-e-wifi.schluter.com"
API_AUTH_URL = API_BASE_URL + "/api/authenticate/user"
API_GET_THERMOSTATS_URL = API_BASE_URL + "/api/thermostats"
API_APPLICATION_ID = 7

_LOGGER = logging.getLogger(__name__)

class Api:
    def __init__(self, timeout=10, command_timeout=60, http_session: Session = None):
        self._timeout = timeout
        self._command_timeout = command_timeout
        self._http_session = http_session

    def get_session(self, email, password):
        response = self._call_api(
            "post", 
            API_AUTH_URL, 
            json = { 
                'Email': email, 
                'Password': password, 
                'Application': API_APPLICATION_ID
            })

        return response
    
    def get_thermostats(self, sessionId):
        thermostats = self._call_api("get", API_GET_THERMOSTATS_URL, sessionId).json()
        groups = thermostats["Groups"]

        thermostat_list = []
        for group in groups:
            for thermostat in group["Thermostats"]:
                thermostat_list.append(Thermostat(thermostat))

        return thermostat_list

    def _call_api(self, method, url, sessionId = None, **kwargs):
        payload = kwargs.get("params") or kwargs.get("json")

        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout
        
        _LOGGER.debug("Calling %s with payload=%s", url, payload)

        response = self._http_session.request(method, url, params = { 'sessionId': sessionId }, **kwargs) if\
            self._http_session is not None else\
            request(method, url, params = { 'sessionId': sessionId }, **kwargs)

        _LOGGER.debug("API Response received: %s - %s", response.status_code, response.content)

        response.raise_for_status()
        return response