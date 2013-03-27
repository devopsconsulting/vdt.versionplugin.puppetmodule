import logging
import subprocess
import glob

from os import getcwd, walk
from os.path import basename, join, normpath

log = logging.getLogger('vdt.versionplugin.puppetmodule.package')

def _build_config_files(name):
    list_of_files = []
    for (dirpath, dirnames, filenames) in walk('.'):
        dirpath = normpath(dirpath)
        for filename in filenames:
            if dirpath.startswith('.') or filename.startswith('.'):
                continue
            list_of_files.append('--config-files=%s' % join('/etc/puppet/modules/', name, dirpath, filename))
    
    return list_of_files

def build_package(version):
    """
    Build package out of a puppet module.
    """
    log.debug("Building puppet module version {0} with fpm.".format(version))
    with version.checkout_tag:
        puppetmodule_name = basename(getcwd())
        config_files = _build_config_files(puppetmodule_name)
        cmd = ['fpm', '-s', 'dir',
               '--depends=puppet-common',
               '--prefix=/etc/puppet/modules',
               '--architecture=all',
               '--name=%s' % puppetmodule_name,
               '--version=%s' % version] + config_files + version.extra_args + ['.']
        log.debug("Running command %s" % " ".join(cmd))
        subprocess.check_call(cmd)


def set_package_version(version):
    """
    If there need to be modifications to source files before a
    package can be built (changelog, version written somewhere etc.)
    that code should go here
    """
    log.debug("set_package_version is not implemented for puppetmodule")
