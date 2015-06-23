#!/usr/bin/python
#
# Copyright (c) SAS Institute, Inc.
#

import os
import logging


logger = logging.getLogger(__name__)


from jinja2 import PackageLoader
from jinja2 import Environment

import json
import yaml
import ZipFile
from yaml import CDumper as Dumper

class AbstractConverter(object):

    def __init__(self, data, destination, filetype=None):
        self._data = data
        self._dest = destination
        self._filetype = filetype

    def convert(self):
        results = []
        for pkgname, pkg in self._data.iteritems():
            dest, data = self._convert(pkgname, pkg)
            results.append(self._write(dest, data))
        return results

    def _convert(self, pkgname, pkg):
        pass

    def _write(self, dest, data):
        pass

    def writeFile(self, path, data):
        '''write plan text (blob) to filename'''
        dirs = os.path.dirname(path)
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(path, 'a') as fobj:
            fobj.write(data)

class ConvertToFiles(AbstractConverter):

    def _convert(self, pkgname, pkg):
        dest = os.path.join(self._destination, '%s.yaml' % pkgname)
        self._write(dest, pkg.asJSON()) 

    def _write(self, dest, data):
        blob = yaml.dump(data, default_flow_style=False, Dumper=Dumper)
        self.writeFile(dest, blob)

class CreateZips(AbstractConverter):

    def getFilesForSource(self):
        return [ [y.name for y in x.files ] for x in 
                    self._data._index.get(self._data._index.keys()[1]).sources ]



class ConvertToSpecs(AbstractConverter):
    pass

class ConvertPyDictToFiles(AbstractConverter):

    def __init__(self, data, destination):
        self._data = data
        self._dest = destination
        self.env = Environment(loader=PackageLoader('specs', 'templates'))
        self.spec_template = self.env.get_template('spectemplate')
        self.tar_template = self.env.get_template('tartemplate')
        self.zip_template = self.env.get_template('ziptemplate')

    def asSpecFiles(self):
        for name, plan in self.data.iteritems():
            path = os.path.join(self.dest, name + '.spec')
            spec = self.asSpecFile(plan)
            self.writePlan(path, spec)

    def asZipScripts(self):
        for name, plan in self.plans.iteritems():
            path = os.path.join(self.dest, name + '-to_zip.sh')
            script = self.asZipScript(plan)
            self.writePlan(path, script)

    def asSpecFile(self, plan):
        return self.spec_template.render(data=plan)

    def asTarScript(self, plan):
        return self.tar_template.render(data=plan)

    def asZipScript(self, plan):
        return self.zip_template.render(data=plan)        

    def writePlan(self, path, blob):
        '''write plan text (blob) to filename'''
        dirs = os.path.dirname(path)
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(path, 'a') as fobj:
            fobj.write(blob)


