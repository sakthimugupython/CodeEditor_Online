from django.contrib import admin
from .models import CodeSnippet, ExecutionHistory, UserProfile

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'language', 'created_at', 'is_public')
    list_filter = ('language', 'is_public', 'created_at')
    search_fields = ('title', 'user__username', 'code')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'title', 'description', 'language')}),
        ('Code', {'fields': ('code',)}),
        ('Settings', {'fields': ('is_public',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(ExecutionHistory)
class ExecutionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'status', 'execution_time', 'created_at')
    list_filter = ('language', 'status', 'created_at')
    search_fields = ('user__username', 'code')
    readonly_fields = ('created_at', 'code', 'stdin', 'stdout', 'stderr')
    fieldsets = (
        ('Execution Info', {'fields': ('user', 'snippet', 'language', 'status')}),
        ('Code & Input', {'fields': ('code', 'stdin')}),
        ('Output', {'fields': ('stdout', 'stderr', 'returncode')}),
        ('Performance', {'fields': ('execution_time', 'created_at')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_executions', 'total_snippets', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_executions', 'total_snippets')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile', {'fields': ('bio', 'avatar')}),
        ('Statistics', {'fields': ('total_executions', 'total_snippets')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
