import os
import subprocess
# from importlib import import_module

# from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Can be run as a cronjob or directly to clean out expired sessions "
        "(only with the database backend at the moment)."
    )

    OUTDATED = 'outdated.txt'
    UPGRADE = 'upgrade.txt'

    def clear_temp_file(self):
        """clear temp file"""
        for file in [self.OUTDATED, self.UPGRADE]:
            if os.path.isfile(file):
                os.remove(file)

    def handle(self, **options):
        """upgrade outdated package"""
        outdated, upgrade = self.OUTDATED, self.UPGRADE

        print('pip list outdated package starting...', '\n', '-' * 50)
        freeze_outdated = "pip list --outdated --format=freeze"
        status, result = subprocess.getstatusoutput(freeze_outdated)
        print(result, '\n', '-' * 50, '\n' * 2)

        echo_outdated = "pip list --outdated --format=freeze > {}".format(outdated)
        status, result = subprocess.getstatusoutput(echo_outdated)

        if os.path.getsize(outdated):
            cut_outdated = "cut -f1 -d\'=\' {} > {}".format(outdated, upgrade)
            status, result = subprocess.getstatusoutput(cut_outdated)

            print('pip upgrade package start...')
            pip_upgrade = 'pip install -r {} -U'.format(upgrade)
            status, result = subprocess.getstatusoutput(pip_upgrade)
            print(result)

        self.clear_temp_file()
