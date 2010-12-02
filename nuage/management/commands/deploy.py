import os
import tempfile
import tarfile
import base64
import urllib
import urllib2
from getpass import getpass
from django.core.management.base import BaseCommand
# from optparse import make_option
from django.conf import settings


class Command(BaseCommand):

    help = 'Deploy an application in nuage infrastructure'

    def handle(self, *args, **options):
        print "Start deploying."

        # User's email
        if hasattr(settings, 'NUAGE_EMAIL'):
            email = settings.NUAGE_EMAIL
        else:
            email = raw_input("Please enter your email: ")

        # User's deployment key
        if hasattr(settings, 'NUAGE_KEY'):
            key = settings.NUAGE_KEY
        else:
            key = getpass("Please enter your deployment key: ")

        # Application's name
        if hasattr(settings, 'NUAGE_APPLICATION'):
            application = settings.NUAGE_APPLICATION
        else:
            application = raw_input("Please enter the application's name: ")

        # application's version
        if hasattr(settings, 'NUAGE_VERSION'):
            version = settings.NUAGE_VERSION
        else:
            version = raw_input("Please enter the application's version: ")

        # Prepare
        print "Preparing to deploy in %(version)s."\
              "%(application)s.apps.cenuage.com ..." % {
            'version': version,
            'application': application,
            }

        # Import settings.
        settings_module = __import__(settings.SETTINGS_MODULE)
        dirname = os.path.dirname(settings_module.__file__)

        # Start compressing
        tempfd = tempfile.NamedTemporaryFile()

        # Create tar.
        tar = tarfile.open(tempfd.name, mode='w:gz')

        def exclude_file(name):
            for ends in ['.pyc', '#', '~']:
                if name.endswith(ends):
                    return True
            return False

        tar.add(dirname, application, exclude=exclude_file)

        # Write to file.
        tar.close()

        # Send file
        # SSH or POST ?
        payload = base64.encodestring(tempfd.read())
        data = urllib.urlencode({
            'email': email,
            'key': key,
            'application': application,
            'version': version,
            'payload': payload,
            })

        # Make request.
        url = 'http://test.cenuage.com/upload'
        request = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e
            print e.read()
