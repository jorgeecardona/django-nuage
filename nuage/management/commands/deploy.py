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

    help = 'Deploy an application in nuage infraestructure'

#    option_list = BaseCommand.option_list + (
#        make_option('--username',
#                    action='store',
#                    dest='username',
#                    help='username'),
#        )

    def handle(self, *args, **options):
        print "Start deploying."

        # Name of application.
        application = settings.NUAGE_APPLICATION
        username = settings.NUAGE_USERNAME
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

        tar.add(dirname, 'tutorial', exclude=lambda f: f.endswith('.pyc'))

        # Write to file.
        tar.close()
        print "Compressed file %s" % (tempfd.name, )

        # Send file
        # SSH or POST ?
        payload = base64.encodestring(tempfd.read())
        data = urllib.urlencode({
            'username': username,
            'key': key,
            'payload': payload,
            })

        urllib2.urlopen('http://nuage.aleph.co/deploy',
                        data=data)
