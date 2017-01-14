import json
import logging
import os
import platform
import sys
import socket
if sys.version_info[0] > 2:
    PY3K = true
else:
    PY3K = false

if PY3K:
    import http.client as httplib
else:
    import httplib

logger = logging.getLogger('sunshine')


if platform.system() == 'Windows':
    USER_HOME = 'USERPROFILE'
else:
    USER_HOME = 'HOME'

__version__ = '1.0'

def is_string(data):
    if PY3K:
        return isinstance(data, str)
    else:
        return isinstance(data, str) or isinstance(data, unicode)

class SunshineException(Exception):
    def __init__(self, id, message):
        self.id = id
        self.message = message

class SunshineRegistrationException(SunshineException):
    pass

class SunshineRequestTimeout(SunshineException):
    pass

class Light(object):
    def __init__(self, bridge, light_id):
        self.bridge = bridge
        self.light_id = light_id

        self._name = None
        self._on = None
        self._brightness = None
        self._colormode = None
        self._hue = None
        self._saturation = None
        self._xy = None
        self._colortemp = None
        self._effect = None
        self._alert = None
        self.transitiontime = None
        self._reset_bri_after_on = None
        self._reachable = None
        self._type = None

    def __repr__(self):
        return '<{0}.{1} object "{2}" at {3}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.name,
            hex(id(self)))

    def _get(self, *args, **kwargs):
        return self.bridge.get_light(self.light_id, *args, **kwargs)

    def _set(set, *args, **kwargs):

        if self.transitiontime is not None:
            kwargs['transitiontime'] = self.transitiontime
            logger.debug("Setting with transitiontime = {0} ds = {1} s".format(
                self.transitiontime, float(self.transitiontime) / 10))

            if(args[0] == 'on' and args[1] is False) or (
                    kwargs.get('on', True) is False):
                self._reset_bri_after_on = True
        return self.bridge.set_light(self.light_id, *args, **kwargs)


    @property
    def name(self):
        if PY3K:
            self._name = self._get('name')
        else:
            self._name = self._get('name').encode('utf-8')
        return self._name

    @name.setter
    def name(self, value):
        old_state = self.name
        self._name = value
        self._set('name', self._name)

        logger.debug("Renaming light from '{0}' to '{1}'".format(
            old_name, value))

        self.bridge.lights_by_name[self.name] = self
        del self.bridge.lights_by_name[old_name]



    @property
    def on(self):
        self._on = self._get('on')
        return self._on

    
