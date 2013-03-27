import logging
import subprocess

from os import walk
from os.path import join, normpath

log = logging.getLogger('vdt.versionplugin.puppetmodule.shared')

def _build_config_files(name):
    list_of_files = []
    for (dirpath, dirnames, filenames) in walk('.'):
        dirpath = normpath(dirpath)
        for filename in filenames:
            if dirpath.startswith('.') or filename.startswith('.'):
                continue
            list_of_files.append('--config-files=%s' % join('/etc/puppet/modules/', name, dirpath, filename))
    
    return list_of_files

def create_package(puppetmodule_name, version, extra_args):
    config_files = _build_config_files(puppetmodule_name)
    cmd = ['fpm', '-s', 'dir',
           '--depends=puppet-common',
           '--prefix=/etc/puppet/modules',
           '--architecture=all',
           '--name=%s' % puppetmodule_name,
           '--version=%s' % version] + config_files + extra_args + ['.']
    log.debug("Running command %s" % " ".join(cmd))
    subprocess.check_call(cmd)
    