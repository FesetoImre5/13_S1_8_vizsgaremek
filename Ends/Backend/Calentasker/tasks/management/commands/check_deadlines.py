from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from tasks.models import Task
from datetime import timedelta

class Command(BaseCommand):
    help = 'Checks for missed deadlines and upcoming tasks to send notifications'

    def handle(self, *args, **options):
        now = timezone.now().date()
        today = now
        tomorrow = today + timedelta(days=1)

        # 1. Handle Missed Tasks
        # Filter: Due date is in the past, status is not 'done'/'archived'/'missed'
        missed_tasks = Task.objects.filter(
            due_date__lt=today,
            active=True
        ).exclude(
            status__in=['done', 'archived', 'missed']
        )

        for task in missed_tasks:
            self.stdout.write(self.style.WARNING(f'Task "{task.title}" skipped deadline ({task.due_date})'))
            
            # Update status
            task.status = 'missed'
            task.save()

            # Notify User
            if task.assigned_to_userid and task.assigned_to_userid.email:
                subject = f"MISSED: {task.title}"
                message = f"Task '{task.title}' was due on {task.due_date} and is now marked as missed."
                
                try:
                    send_mail(
                        subject,
                        message,
                        'system@calentasker.com',
                        [task.assigned_to_userid.email],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f'  Notification sent to {task.assigned_to_userid.email}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Failed to send email: {e}'))

        # 2. Handle Upcoming Tasks (Due Tomorrow)
        # Filter: Due date is exactly tomorrow, status is active/todo/in_progress
        upcoming_tasks = Task.objects.filter(
            due_date=tomorrow,
            active=True,
            status__in=['todo', 'in_progress', 'missed'] # Typically notify for todo/in_progress, maybe missed if re-activated
        )

        for task in upcoming_tasks:
            if task.assigned_to_userid and task.assigned_to_userid.email:
                self.stdout.write(self.style.NOTICE(f'Task "{task.title}" is due tomorrow ({task.due_date})'))
                
                subject = f"REMINDER: {task.title} is due tomorrow"
                message = f"Task '{task.title}' is due on {task.due_date}. Please ensure it is completed."
                
                try:
                    send_mail(
                        subject,
                        message,
                        'system@calentasker.com',
                        [task.assigned_to_userid.email],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f'  Notification sent to {task.assigned_to_userid.email}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Failed to send email: {e}'))
            else:
                 self.stdout.write(self.style.NOTICE(f'Task "{task.title}" is due tomorrow but has no assigned user email.'))

        self.stdout.write(self.style.SUCCESS('Check complete.'))
