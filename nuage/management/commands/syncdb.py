import sys
from optparse import make_option
from django.core.management.commands import syncdb


class Command(NoArgsCommand):
    option_list = syncdb.Command.option_list + (
        make_option('--nuage', action='store_true', dest='nuage',
                    default=False, help='Tells django to run this '\
                    'command in nuage infrastructure.'),
        )
