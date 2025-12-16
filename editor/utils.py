"""Utility functions for the editor app."""

from django.utils import timezone
from datetime import timedelta
from .models import ExecutionHistory, CodeSnippet

def get_user_statistics(user):
    """Get user statistics."""
    return {
        'total_snippets': CodeSnippet.objects.filter(user=user).count(),
        'total_executions': ExecutionHistory.objects.filter(user=user).count(),
        'successful_executions': ExecutionHistory.objects.filter(
            user=user, status='success'
        ).count(),
        'failed_executions': ExecutionHistory.objects.filter(
            user=user, status='error'
        ).count(),
        'timeout_executions': ExecutionHistory.objects.filter(
            user=user, status='timeout'
        ).count(),
    }

def get_execution_stats(user, days=7):
    """Get execution statistics for last N days."""
    start_date = timezone.now() - timedelta(days=days)
    executions = ExecutionHistory.objects.filter(
        user=user,
        created_at__gte=start_date
    )
    
    stats_by_language = {}
    for execution in executions:
        lang = execution.language
        if lang not in stats_by_language:
            stats_by_language[lang] = {
                'count': 0,
                'success': 0,
                'error': 0,
                'timeout': 0,
                'avg_time': 0,
            }
        
        stats_by_language[lang]['count'] += 1
        if execution.status == 'success':
            stats_by_language[lang]['success'] += 1
        elif execution.status == 'error':
            stats_by_language[lang]['error'] += 1
        elif execution.status == 'timeout':
            stats_by_language[lang]['timeout'] += 1
    
    return stats_by_language

def cleanup_old_executions(days=30):
    """Delete execution history older than N days."""
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count, _ = ExecutionHistory.objects.filter(
        created_at__lt=cutoff_date
    ).delete()
    return deleted_count

def get_popular_snippets(limit=10):
    """Get most used snippets."""
    from django.db.models import Count
    return CodeSnippet.objects.annotate(
        execution_count=Count('executionhistory')
    ).order_by('-execution_count')[:limit]

def get_language_statistics():
    """Get statistics by programming language."""
    from django.db.models import Count
    stats = {}
    
    for execution in ExecutionHistory.objects.values('language').annotate(
        count=Count('id')
    ):
        stats[execution['language']] = execution['count']
    
    return stats

def validate_code_snippet(code, max_length=50000):
    """Validate code snippet."""
    if not code or not code.strip():
        return False, "Code cannot be empty"
    
    if len(code) > max_length:
        return False, f"Code exceeds maximum length of {max_length} characters"
    
    return True, "Valid"

def format_execution_time(seconds):
    """Format execution time for display."""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f}µs"
    elif seconds < 1:
        return f"{seconds*1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"

def truncate_output(text, max_length=10000):
    """Truncate output to maximum length."""
    if len(text) > max_length:
        return text[:max_length] + f"\n... (truncated, {len(text) - max_length} more characters)"
    return text
