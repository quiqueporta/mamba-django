import argparse

from django.core.management import call_command
from django.db import transaction, connections
from django.test.utils import (
    setup_databases,
    setup_test_environment,
    teardown_databases,
    teardown_test_environment
)
from mamba import (
    __version__,
    application_factory
)


MAMBA_ARGUMENTS = 0


class MambaRunner:

    def __init__(self, keepdb=False, *args, **kwargs):
        self.keepdb = keepdb

    def run_tests(self, test_labels=None, extra_tests=None, **kwargs):
        old_config = self._setup_environment()

        run_failed = False

        arguments = self._parse_mamba_arguments()
        arguments.specs = test_labels or ['./spec', './specs']
        if arguments.version:
            print(__version__)
            return

        factory = application_factory.ApplicationFactory(arguments)
        runner = factory.runner()

        try:
            runner.run()
        except Exception:
            run_failed = True
            raise
        finally:
            try:
                self._teardown_environment(old_config)
            except Exception:
                # Silence teardown exceptions if an exception was raised during
                # runs to avoid shadowing it.
                if not run_failed:
                    raise

        if runner.has_failed_examples:
            return 1

    def _setup_environment(self):
        setup_test_environment()
        old_config = setup_databases(
            verbosity=1, interactive=True, keepdb=self.keepdb, debug_sql=False, parallel=0,
            aliases=None
        )
        return old_config

    def _teardown_environment(self, old_config):
        teardown_databases(old_config=old_config, verbosity=1, parallel=0, keepdb=self.keepdb)
        teardown_test_environment()

    def _parse_mamba_arguments(self):
        parser = argparse.ArgumentParser()

        MambaRunner.add_mamba_arguments(parser)
        # Added this here due to a conflict with Django test parameters.
        parser.add_argument(
            '--no-color',
            default=False,
            action='store_true',
            help='turn off all output coloring (default: %(default)s)'
        )

        return parser.parse_known_args()[MAMBA_ARGUMENTS]

    @classmethod
    def add_mamba_arguments(cls, parser):
        parser.add_argument(
            '--mamba-version',
            '-mv',
            default=False,
            action='store_true',
            help='display the version',
            dest='version'
        )
        parser.add_argument(
            '--slow',
            '-s',
            default=0.075,
            type=float,
            help='slow test threshold in seconds (default: %(default)s)'
        )
        parser.add_argument(
            '--enable-coverage',
            default=False,
            action='store_true',
            help='enable code coverage measurement (default: %(default)s)'
        )
        parser.add_argument(
            '--coverage-file',
            default='.coverage',
            action='store',
            help='name of coverage data file (default: %(default)s)'
        )
        parser.add_argument(
            '--format',
            '-f',
            default='progress',
            action='store',
            help='output format (default: %(default)s)'
        )
        parser.add_argument(
            'specs',
            default=['./spec', './specs'],
            nargs='*',
            help='paths to specs to run or directories with specs to run (default: %(default)s)'
        )
        parser.add_argument(
            '--tags',
            '-t',
            default=None,
            type=lambda x: [tag.strip() for tag in x.split(',')],
            action='store',
            help='run examples with specified tags (example: -t unit,integration)'
        )

    @classmethod
    def add_arguments(cls, parser):
        # We need to create this method to add Mamba arguments to the Django test command.
        cls.add_mamba_arguments(parser)
        parser.add_argument(
            '-k',
            '--keepdb',
            action='store_true',
            help='Preserves the test DB between runs.'
        )


def start_django_transactions():
    transactions = {}

    for alias in connections:
        transactions[alias] = transaction.atomic(using=alias)
        transactions[alias].__enter__()

    return transactions


def rollback_django_transactions(transactions):
    for alias, db_transaction in transactions.items():
        transaction.set_rollback(True, using=alias)
        db_transaction.__exit__(None, None, None)


def load_fixtures(fixtures):
    for alias in connections:
        call_command('loaddata', *fixtures, **{'verbosity': 0, 'database': alias})
