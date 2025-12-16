from rest_framework import serializers
from editor.models import CodeSnippet, ExecutionHistory

class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = ['id', 'title', 'description', 'code', 'language', 'created_at', 'updated_at', 'is_public']
        read_only_fields = ['created_at', 'updated_at']

class ExecutionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionHistory
        fields = ['id', 'code', 'language', 'stdin', 'stdout', 'stderr', 'returncode', 'status', 'execution_time', 'created_at']
        read_only_fields = ['stdout', 'stderr', 'returncode', 'status', 'execution_time', 'created_at']

class ExecutionRequestSerializer(serializers.Serializer):
    """Serializer for code execution requests."""
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=['python', 'java', 'javascript'])
    stdin = serializers.CharField(required=False, allow_blank=True)
    snippet_id = serializers.IntegerField(required=False, allow_null=True)
