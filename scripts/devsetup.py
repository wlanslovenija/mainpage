#!/usr/bin/env python

import os, subprocess, sys, tempfile, urllib

root = os.path.join(os.path.dirname(__file__), '..')

if sys.version_info <= (2, 6):
    requirements = os.path.abspath(os.path.join(root, 'requirements-python26.txt'))
else:
    requirements = os.path.abspath(os.path.join(root, 'requirements.txt'))

manage_script = os.path.abspath(os.path.join(root, 'mainpage', 'manage.py'))

print "Installing requirements:\n"
subprocess.check_call(('pip', 'install', '-r', requirements))

print "\nSetting up the database:\n"
subprocess.check_call(('python', manage_script, 'syncdb'))
subprocess.check_call(('python', manage_script, 'migrate'))

print "\nDownloading and importing database dump:\n"
tempFile = tempfile.NamedTemporaryFile(delete=False)
webFile = urllib.urlopen('http://bindist.wlan-si.net/data/dumpcms.yaml.bz2')
tempFile.write(webFile.read())
webFile.close()
tempFile.close()
os.rename(tempFile.name, tempFile.name + '.yaml.bz2')
subprocess.check_call(('python', manage_script, 'loaddata', tempFile.name))
os.remove(tempFile.name + '.yaml.bz2')

print "\nAll done!"
