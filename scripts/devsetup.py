#!/usr/local/bin/python
import os, subprocess, sys, tempfile, urllib

root = os.path.join(os.path.dirname(__file__), '..')
if sys.version_info <= (2, 6):
    requirements = os.path.abspath(os.path.join(root, 'oldpython-requirements.txt'))
else:
    requirements = os.path.abspath(os.path.join(root, 'requirements.txt'))

print "Installing requirements:\n"
subprocess.call(('pip', 'install', '-r', requirements))
subprocess.call(('git', 'clone', 'https://github.com/wlanslovenija/nodewatcher.git', os.path.abspath(os.path.join(root, 'nodewatcher'))))

print "Setting up the database:\n"
subprocess.call(('python', os.path.abspath(os.path.join(root, 'mainpage', 'manage.py')), 'syncdb'))
subprocess.call(('python', os.path.abspath(os.path.join(root, 'mainpage', 'manage.py')), 'migrate'))

print "Loading initial data from live site:\n"
tempFile = tempfile.NamedTemporaryFile(delete=False)
webFile = urllib.urlopen('http://bindist.wlan-si.net/data/dumpcms.yaml.bz2')
tempFile.write(webFile.read())
webFile.close()
tempFile.close()
os.rename(tempFile.name, tempFile.name + '.yaml.bz2')
subprocess.call(('python', os.path.abspath(os.path.join(root, 'mainpage', 'manage.py')), 'loaddata', tempFile.name))
os.remove(tempFile.name + '.yaml.bz2')

print "All done!\ncd into mainpage and run \"python manage.py runserver\" to test it out."