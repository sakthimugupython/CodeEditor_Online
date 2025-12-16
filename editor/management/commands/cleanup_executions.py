from django.core.management.base import BaseCommand
from editor.utils import cleanup_old_executions

class Command(BaseCommand):
    help = 'Clean up old execution history'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete executions older than N days (default: 30)'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        deleted_count = cleanup_old_executions(days)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {deleted_count} execution records older than {days} days'
            )
        )
