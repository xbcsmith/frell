
import logging
logger = logging.getLogger(__name__)

import os
import ConfigParser as configparser


class Config(object):

    _paths = ( '/etc/onepm/onepm.conf', 
                '~/.onepmrc',
                './.onepmrc'
            )

    def __init__(self, cfgfile=None):
        self._cfgfile = cfgfile
        self._cfg = configparser.ConfigParser()    
        self._cfg.add_section('defaults')
        self._cfg.set('defaults', 'templates_dir', 'templates')
        self._cfg.set('defaults', 'logger_ini', 'logger.ini')
        self._cfg.set('defaults', 'debug', 'False')
        self._getConfig(cfgfile)

    @property
    def templates_dir(self):
        return self._get_value('templates_dir')

    @property
    def logger_ini(self):
        return self._get_value('logger_ini')

    @property
    def debug(self):
        return self._cfg.getboolean('defaults', 'debug')

    def _get_value(self, value, section='defaults'):
        if self._cfg.getboolean(section, 'debug'):
            section = 'debug'
        return self._cfg.get(section, value)

    def _getPaths(self):
        return self._paths

    def _getConfig(self, cfgfile=None):
        for path in self._getPaths():
            if os.path.exists(path):
                self._cfg.read(path) 
        if cfgfile and os.path.exists(cfgfile):
            self._cfg.read(cfgfile)
        return self._cfg

    def writeConfigFile(self, path=None):
        if not path:
            path = self._cfgfile or self._paths[-1]
        with open(path, 'wb') as configfile:
            self._cfg.write(configfile)

    def _readConfigFile(self, cfgfile=None):
        if cfgfile:
            self._cfgfile = cfgfile
        if self._cfgfile:
            self._cfg.read(cfgfile)

