import os
import tempfile
import tarfile
import base64
import urllib
import urllib2
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.conf import settings


class Command(BaseCommand):

    help = 'Deploy an application in nuage infrastructure'

#    option_list = BaseCommand.option_list + (
#        make_option('--email',
#                    action='store',
#                    dest='email',
#                    help='email'),
#        )

    def handle(self, *args, **options):
        print "Start deploying."

        # Name of application.
        application = settings.NUAGE_APPLICATION
        email = settings.NUAGE_EMAIL
        key = settings.NUAGE_KEY

        # Prepare
        print "Prepare application %s." % (application, )

        # Import settings.
        settings_module = __import__(settings.SETTINGS_MODULE)
        dirname = os.path.dirname(settings_module.__file__)

        # Start compressing
        print "Create compress file with %s" % (os.path.abspath(dirname), )
        tempfd = tempfile.NamedTemporaryFile(suffix='.tar.gz')

        # Create tar.
        tar = tarfile.open(tempfd.name, mode='w:gz')

        def exclude_file(name):
            for ends in ['.pyc', '#', '~']:
                if name.endswith(ends):
                    return True
            return False

        tar.add(dirname, 'tutorial', exclude=exclude_file)

        # Write to file.
        tar.close()
        print "Compressed file %s" % (tempfd.name, )

        # Send file
        # SSH or POST ?
        payload = base64.encodestring(tempfd.read())
        data = urllib.urlencode({
            'email': email,
            'key': key,
            'application': application,
            'payload': payload,
            })

        # Make request.
        url = 'http://localhost:8000/deploy'
        request = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e
