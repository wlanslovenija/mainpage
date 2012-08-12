#!/usr/bin/env python

import os, subprocess, sys, tempfile, urllib

root = os.path.join(os.path.dirname(__file__), '..')
database_file = os.path.abspath(os.path.join(root, 'mainpage', 'db.sqlite'))

if sys.version_info <= (2, 6):
    requirements = os.path.abspath(os.path.join(root, 'requirements-python26.txt'))
else:
    requirements = os.path.abspath(os.path.join(root, 'requirements.txt'))

manage_script = os.path.abspath(os.path.join(root, 'manage.py'))

print "Installing requirements:\n"
subprocess.check_call(('pip', 'install', '-r', requirements))

print "\nSetting up the database:\n"
if os.path.isfile(database_file):
    os.remove(database_file)
subprocess.check_call(('python', manage_script, 'syncdb'))
subprocess.check_call(('python', manage_script, 'migrate'))
subprocess.check_call(('python', manage_script, 'reset', '--noinput', 'contenttypes'))

print "\nDownloading and importing database dump:\n"
tempFile = tempfile.NamedTemporaryFile(delete=False)
webFile = urllib.urlopen('http://bindist.wlan-si.net/data/dumpcms.yaml.bz2')
tempFile.write(webFile.read())
webFile.close()
tempFile.close()
os.rename(tempFile.name, tempFile.name + '.yaml.bz2')
subprocess.check_call(('python', manage_script, 'loaddata', tempFile.name))
os.remove(tempFile.name + '.yaml.bz2')

subprocess.check_call(('sqlite3', database_file, """UPDATE cmsplugin_blog_entrytitle SET author_id=1"""))

print "\nPreparing directories."

for path in (('media', 'files'), ('media', 'thumbnails'), ('smedia', 'files'), ('smedia', 'thumbnails')):
    try:
        os.makedirs(os.path.join(root, 'mainpage', *path))
    except OSError:
        pass

print "\nAll done!"
