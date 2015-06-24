#!/usr/bin/python
#
# Copyright (c) SAS Institute, Inc.
#

import os
import logging


logger = logging.getLogger(__name__)


from jinja2 import PackageLoader
from jinja2 import Environment

import time
import datetime
import json
import yaml
import  zipfile
from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from tarfile import TarFile
from collections import namedtuple

class AbstractConverter(object):

    def __init__(self, data, destination, location=None, filetype=None):
        self._data = data
        self._dest = destination
        self._filetype = filetype
        self._location = location
        self._index = {}

    def convert(self):
        for pkgname, pkg in self._data.iteritems():
            dest, data = self._convert(pkgname, pkg)
            self._index.setdefault(dest, set()).add(data)
        return self._index

    def _indexPkg(self, pkgname, results):
        self._index.setdefault(pkgname, set()).add(results)

    def _getDestination(self, filename):
        return os.path.join(self._dest, filename)

    def _getLocation(self, filename):
        return os.path.join(self._location, filename)

    def _convert(self, pkgname, pkg):
        return pkgname, pkg

class AbstractFileWriter(AbstractConverter):

    def writeFiles(self):
        for pkgname, pkg in self._data.iteritems():
            dest, data = self._convert(pkgname, pkg)
            result = self._write(dest, data)
            self._indexPkg(pkgname, result)
        return self._index

    def _write(self, dest, data):
        result = self.writeFile(dest, data)
        return result

    def writeFile(self, path, data):
        '''write plan text (blob) to filename'''
        dirs = os.path.dirname(path)
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)
        try:
            with open(path, 'a') as fobj:
                fobj.write(data)
        except Exception, e:
            raise Exception, e
        finally:
            result = (path, 0)
        return result

class WriteYamlFiles(AbstractFileWriter):

    def _convert(self, pkgname, pkg):
        dest = self._getDestination('%s.yaml' % pkgname)
        blob = yaml.load(pkg.asJSON(), Loader=Loader)
        data = yaml.dump(blob, default_flow_style=False, Dumper=Dumper)
        return dest, data

class WriteJsonFiles(AbstractFileWriter):

    def _convert(self, pkgname, pkg):
        dest = self._getDestination('%s.json' % pkgname)
        data = json.dumps(pkg._expanded(), sort_keys=True, 
                                indent=4, separators=(',', ': ')) 
        return dest, data

class AbstractArchiver(AbstractConverter):

    def createArchives(self):
        for pkgname, pkg in self._data.iteritems():
            dest, data = self.archive(pkgname, pkg)
            self._indexPkg(dest, data)
        return self._index
        
    def archive(self, pkgname, pkg):
        dest, data = self._archive(pkgname, pkg)
        return dest, data

    def _archive(self, pkgname, pkg):
        return pkgname, pkg
    
class CreateZips(AbstractArchiver):

    def _archive(self, pkgname, pkg):
        results = []
        for source in pkg.sources:
            description = "%s\n%s\nas part of %s\n" % (source.archive, pkg.description, pkg.nvr)
            files = [ x.name for x in source.files ]
            path = self._getDestination(source.archive)
            result = self._createZip(path, files, desc=description)
            results.append((source.archive, result))
        return pkgname, tuple(results)

    def _createZip(self, path, files, msg=None, desc=None):
        if not msg:
            msg = "Created by Crufter Automation %s" % time.strftime('%Y-%d-%m')
        if not desc:
            desc = "%s" % os.path.basename(path)
        info = zipfile.ZipInfo('from_string.txt', 
                           date_time=time.localtime(time.time()),
                           )
        info.compress_type=zipfile.ZIP_DEFLATED
        info.comment=desc or msg
        info.create_system=3
        try:
            zf = zipfile.ZipFile(path, 'w', allowZip64=True)
            for fn in files:
                zipname = fn #fn.replace(source.destination, basedir)
                # FIXME
                # I know this is going to bite me in the ass at some point
                if self._location:
                    fn = self._getLocation(fn)
                assert os.path.exists(fn)
                zf.write(fn, arcname=zipname)
            zf.writestr(info, msg)
        finally:
            result = self._zipInfo(zf)
            zf.close()
        return result

    def _zipInfo(self, zf):
        data = []
        fields = ('Name', 'Comment', 'Uncompressed', 
                    'Compressed', 'ZipVersion', 'Modified', 'System') 
        zinfo = namedtuple('ZInfo', fields)
        for info in zf.infolist():
            data.append(zinfo(info.filename, info.comment,
                    info.date_time, info.create_system,
                    info.create_version, info.compress_size,
                    info.file_size,)
                    )
        return tuple(data)


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


