#!/usr/bin/env python

# Copyright (c) 2019, Michael Boyle
# See LICENSE file for details: <https://github.com/moble/quaternion/blob/master/LICENSE>

from distutils.core import setup
from os import getenv

# Construct the version number from the date and time this python version was created.
from os import environ
from sys import platform
on_windows = ('win' in platform.lower() and not 'darwin' in platform.lower())
if "package_version" in environ:
    version = environ["package_version"]
    print("Setup.py using environment version='{0}'".format(version))
else:
    print("The variable 'package_version' was not present in the environment")
    try:
        # For cases where this is being installed from git.  This gives the true version number.
        from subprocess import check_output
        if on_windows:
            version = check_output("""git log -1 --format=%cd --date=format:'%Y.%m.%d.%H.%M.%S'""", shell=False)
            version = version.decode('ascii').strip().replace('.0', '.').replace("'", "")
        else:
            try:
                from subprocess import DEVNULL as devnull
                version = check_output("""git log -1 --format=%cd --date=format:'%Y.%-m.%-d.%-H.%-M.%-S'""", shell=True, stderr=devnull)
            except AttributeError:
                from os import devnull
                version = check_output("""git log -1 --format=%cd --date=format:'%Y.%-m.%-d.%-H.%-M.%-S'""", shell=True, stderr=devnull)
            version = version.decode('ascii').rstrip()
        print("Setup.py using git log version='{0}'".format(version))
    except Exception:
        # For cases where this isn't being installed from git.  This gives the wrong version number,
        # but at least it provides some information.
        #import traceback
        #print(traceback.format_exc())
        try:
            from time import strftime, gmtime
            try:
                version = strftime("%Y.%-m.%-d.%-H.%-M.%-S", gmtime())
            except ValueError:  # because Windows
                version = strftime("%Y.%m.%d.%H.%M.%S", gmtime()).replace('.0', '.')
            print("Setup.py using strftime version='{0}'".format(version))
        except:
            version = '0.0.0'
            print("Setup.py failed to determine the version; using '{0}'".format(version))
with open('_version.py', 'w') as f:
    f.write('__version__ = "{0}"'.format(version))


long_description = """\
This package collects a number of functions for constructing and manipulating gravitational
waveforms, including rotating, determining the angular velocity, finding the co-precessing and
co-rotating frames, and applying boosts, translations, and supertranslations.
"""

if __name__ == "__main__":
    from setuptools import setup
    setup(name='scri',
          version=version,
          description='Manipulating time-dependent functions of spin-weighted spherical harmonics',
          long_description=long_description,
          url='https://github.com/moble/scri',
          author='Michael Boyle',
          author_email='mob22@cornell.edu',
          package_dir={'scri': '.'},
          packages=['scri', 'scri.pn', 'scri.SpEC', 'scri.LVC'],
          requires=['numpy', 'scipy', 'quaternion>=2019.5.24.11.54.47', 'spinsfast', 'spherical_functions', 'sxs'],
    )
