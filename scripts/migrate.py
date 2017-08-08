import os, subprocess, tempfile, urllib, tarfile, sqlite3

root = os.path.join(os.path.dirname(__file__), '..')

manage_script = os.path.abspath(os.path.join(root, 'manage.py'))
database_file = os.path.abspath(os.path.join(root, 'mainpage', 'db.sqlite'))

print "\nSetting up the database:\n"
if os.path.isfile(database_file):
    print "Removing old database.\n"
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

(filename, _) = urllib.urlretrieve('http://bindist.wlan-si.net/data/dumpcms-nodewatcher.tar.bz2')
file = tarfile.open(filename)
file.extract('data.json')
subprocess.check_call(('python', manage_script, 'loaddata', 'data.json'))
os.remove('data.json')

connection = sqlite3.connect(database_file)
cursor = connection.cursor()
cursor.execute("""UPDATE cmsplugin_blog_entrytitle SET author_id=1""")
connection.commit()
cursor.close()

print "\nPreparing directories."

for path in (('media', 'files'), ('media', 'thumbnails'), ('smedia', 'files'), ('smedia', 'thumbnails')):
    try:
        os.makedirs(os.path.join(root, 'mainpage', *path))
    except OSError:
        pass

print "\nAll done!"