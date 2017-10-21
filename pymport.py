#!/usr/bin/env python

from distutils.sysconfig import get_python_lib
import platform
import re
import sys

if __name__ == "__main__":
    raise StandardError("Can't be used as main");

__old_excepthook__ = sys.excepthook

"""These are modules that can simply be installed with pip"""
pymport_modules_pip_simple = [
    "requests",
    "schedule",
]

"""These are modules that can be installed with pip but the name of the package needs to be changed"""
pymport_modules_pip_mapped = {
    "bs4":         "beautifulsoup4",
    "prettytable": "PrettyTable",
}

"""These are modules that might require some special installation"""
pymport_modules_by_name = {
  "glib": """
Try:
    sudo yum install pygobjects2
If you use a non-standard Python, try copying files there, e.g.
    cp -r /usr/lib64/python2.6/site-packages/gtk-2.0/glib %(site_packages)s/
""",
  "gnomekeyring": """
Try:
    sudo yum install gnome-python2-gnomekeyring.x86_64
If you use a non-standard Python, try copying files there, e.g.
    cp -r /usr/lib64/python2.6/site-packages/gtk-2.0/gobject %(site_packages)s/
    cp -r /usr/lib64/python2.6/site-packages/gtk-2.0/gnomekeyring.so %(site_packages)s/
""",
  "snowflake.connector": """
        Try:
            sudo %(pip)s install snowflake-connector-python prettytable
        You might also need to install 
            %(python)s-python-devel
""",
}


def log(s):
    sys.stderr.write("=== PYMPORT ===: " + s + "\n")


def pymport_excepthook(exctype, value, traceback):
    """Our custom exception handler, will print help for known failures. """
    subs = {
        "site_packages": get_python_lib(),
        "pip": "pip{0}.{1}".format(platform.python_version_tuple()[0],
                                   platform.python_version_tuple()[1]),
        "python": "python{0}{1}".format(platform.python_version_tuple()[0],
                                   platform.python_version_tuple()[1])
    }
    if (exctype == ImportError):
        msg = str(value)
        match = re.match("No module named (.*)", msg)
        if (match):
            name = match.group(1)
            hint = None
            if name in pymport_modules_pip_simple:
                hint = "Try:\n    sudo {0} install {1}".format(subs["pip"], name)
            if hint is None and name in pymport_modules_pip_mapped:
                name = pymport_modules_pip_mapped[name]
                hint = "Try:\n    sudo {0} install {1}".format(subs["pip"], name)
            if hint is None and name in pymport_modules_by_name:
                hint = pymport_modules_by_name[name] % subs
            if hint is not None:
                log(hint)
            else:
                log("No hint for module {0}, try using pip".format(name))
    __old_excepthook__(exctype, value, traceback)


sys.excepthook = pymport_excepthook
