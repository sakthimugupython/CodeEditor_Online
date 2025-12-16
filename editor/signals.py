"""Django signals for editor app."""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, CodeSnippet, ExecutionHistory

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved."""
    instance.profile.save()

@receiver(post_save, sender=CodeSnippet)
def update_snippet_count(sender, instance, created, **kwargs):
    """Update user's snippet count."""
    if created:
        profile = instance.user.profile
        profile.total_snippets += 1
        profile.save()

@receiver(post_delete, sender=CodeSnippet)
def decrement_snippet_count(sender, instance, **kwargs):
    """Decrement user's snippet count."""
    profile = instance.user.profile
    profile.total_snippets = max(0, profile.total_snippets - 1)
    profile.save()

@receiver(post_save, sender=ExecutionHistory)
def update_execution_count(sender, instance, created, **kwargs):
    """Update user's execution count."""
    if created:
        profile = instance.user.profile
        profile.total_executions += 1
        profile.save()
